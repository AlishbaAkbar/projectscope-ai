import json
import logging
import re
from typing import Optional
from pydantic import ValidationError

from app.ai.providers.base import LLMProvider
from app.ai.providers.factory import LLMProviderFactory
from app.ai.prompts.requirement_analysis import SYSTEM_PROMPT, build_analysis_prompt
from app.schemas.analysis import RawAIAnalysisResponse
from app.utils.config import get_settings
from app.utils.error_handlers import LLMValidationException, LLMProviderException

logger = logging.getLogger(__name__)


class RequirementAnalyzer:
    """
    Orchestrates LLM interaction, JSON extraction, Pydantic validation, and retry recovery.
    """

    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or LLMProviderFactory.get_provider()
        self.settings = get_settings()

    def _extract_json_string(self, raw_text: str) -> str:
        """
        Strips markdown code blocks, HTML tags, or surrounding whitespace from raw LLM output.
        """
        text = raw_text.strip()

        # Handle ```json ... ``` or ``` ... ```
        json_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if json_block_match:
            text = json_block_match.group(1).strip()

        # If text still contains non-JSON prefix/suffix, find the first '{' and last '}'
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            text = text[start_idx : end_idx + 1]

        return text

    async def analyze(
        self,
        project_name: str,
        description: str,
        platform: str = "Web"
    ) -> RawAIAnalysisResponse:
        """
        Execute requirement analysis on project input, with automatic validation and retry.
        """
        if not description or len(description.strip()) < 5:
            raise LLMValidationException("Project description must be at least 5 characters long.")

        prompt = build_analysis_prompt(project_name=project_name, description=description, platform=platform)
        max_retries = self.settings.AI_MAX_RETRIES

        last_raw_response = ""
        last_error = ""

        for attempt in range(max_retries + 1):
            try:
                if attempt == 0:
                    current_prompt = prompt
                else:
                    # Retry with targeted instruction containing previous validation error
                    current_prompt = (
                        f"{prompt}\n\n"
                        f"IMPORTANT: Your previous output failed schema validation with error: {last_error}\n"
                        f"Please output strictly valid JSON matching the exact schema."
                    )

                logger.info(f"Invoking LLM requirement analyzer (attempt {attempt + 1}/{max_retries + 1})...")
                raw_response = await self.provider.analyze(current_prompt, SYSTEM_PROMPT)
                last_raw_response = raw_response

                cleaned_json_str = self._extract_json_string(raw_response)
                parsed_dict = json.loads(cleaned_json_str)

                # Validate against Pydantic schema
                validated_data = RawAIAnalysisResponse.model_validate(parsed_dict)
                logger.info(
                    f"Successfully analyzed project '{project_name}': "
                    f"{len(validated_data.requirements)} requirements, {len(validated_data.features)} features."
                )
                return validated_data

            except json.JSONDecodeError as json_err:
                last_error = f"Malformed JSON: {str(json_err)}"
                logger.warning(f"Attempt {attempt + 1} produced malformed JSON: {json_err}")
                if attempt == max_retries:
                    raise LLMValidationException(
                        message=f"Failed to parse LLM response as valid JSON: {str(json_err)}",
                        raw_output=last_raw_response
                    )

            except ValidationError as val_err:
                last_error = f"Schema validation error: {str(val_err)}"
                logger.warning(f"Attempt {attempt + 1} failed schema validation: {val_err}")
                if attempt == max_retries:
                    raise LLMValidationException(
                        message=f"LLM response violated required schema: {str(val_err)}",
                        raw_output=last_raw_response,
                        details=val_err.errors()
                    )

            except LLMProviderException:
                # Direct provider errors shouldn't be blindly retried if they are API auth or config issues
                raise

            except Exception as e:
                last_error = str(e)
                logger.error(f"Unexpected error during analysis attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise LLMValidationException(
                        message=f"Analysis pipeline failed: {str(e)}",
                        raw_output=last_raw_response
                    )

        raise LLMValidationException("Analysis failed after maximum retries.", raw_output=last_raw_response)
