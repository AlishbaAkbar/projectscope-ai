import json
import logging
import re
import time
from typing import Optional

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai.prompts.requirement_analysis import SYSTEM_PROMPT, build_analysis_prompt
from app.ai.providers.base import LLMProvider
from app.ai.providers.factory import LLMProviderFactory
from app.ai.schemas import RawAnalysisResponse
from app.core.config import settings
from app.models.llm_request import LLMRequest
from app.utils.error_handlers import LLMProviderException, LLMValidationException

logger = logging.getLogger(__name__)
RawAIAnalysisResponse = RawAnalysisResponse


class RequirementAnalyzer:
    """
    Orchestrates LLM interaction, JSON extraction, Pydantic validation, and retry recovery.
    """

    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        db: Optional[Session] = None,
        project_id: Optional[int] = None,
    ):
        self.provider = provider or LLMProviderFactory.get_provider()
        self.db = db
        self.project_id = project_id

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

    def _record_request(
        self,
        prompt: str,
        response: Optional[str],
        latency_ms: float,
        error: Optional[Exception],
    ) -> None:
        if self.db is None:
            return

        provider_name = type(self.provider).__name__.removesuffix("Provider").lower()
        if provider_name == "mockllm":
            provider_name = "mock"
        model = getattr(self.provider, "model", None)
        self.db.add(LLMRequest(
            project_id=self.project_id,
            provider=provider_name,
            model=model,
            model_version=getattr(self.provider, "model_version", None),
            prompt_tokens=(len(prompt) + 3) // 4,
            response_tokens=(len(response) + 3) // 4 if response else 0,
            latency_ms=round(latency_ms, 2),
            status="failure" if error else "success",
            error_message=str(error)[:2000] if error else None,
        ))
        self.db.commit()

    async def _generate(self, prompt: str, system_prompt: str) -> str:
        started_at = time.perf_counter()
        response = None
        failure = None
        try:
            logger.info("Calling LLM provider %s", type(self.provider).__name__)
            response = await self.provider.generate(prompt, system_prompt)
            return response
        except Exception as exc:
            failure = exc
            raise
        finally:
            self._record_request(
                prompt,
                response,
                (time.perf_counter() - started_at) * 1000,
                failure,
            )

    async def _fallback_to_mock(
        self,
        current_prompt: str,
        project_name: str,
        failure: Exception,
    ) -> RawAIAnalysisResponse:
        from app.ai.providers.mock_provider import MockLLMProvider

        primary_provider = self.provider
        logger.warning(
            "Primary provider %s failed; falling back to mock provider: %s",
            type(self.provider).__name__,
            failure,
        )
        self.provider = MockLLMProvider()
        try:
            raw_response = await self._generate(current_prompt, SYSTEM_PROMPT)
        except Exception as fallback_error:
            raise LLMProviderException(
                f"Primary and mock providers failed: {fallback_error}",
                provider=type(primary_provider).__name__,
            ) from fallback_error
        finally:
            self.provider = primary_provider

        try:
            parsed_dict = json.loads(self._extract_json_string(raw_response))
            validated_data = RawAnalysisResponse.model_validate(parsed_dict)
        except (json.JSONDecodeError, ValidationError) as fallback_error:
            raise LLMValidationException(
                message=f"Mock fallback returned invalid analysis: {fallback_error}",
                raw_output=raw_response,
            ) from fallback_error

        logger.info(
            "Mock fallback analyzed project '%s': %s requirements, %s features.",
            project_name,
            len(validated_data.requirements),
            len(validated_data.features),
        )
        return validated_data

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
        prompt = prompt[:settings.MAX_PROMPT_LENGTH]
        last_raw_response = ""
        last_error = ""

        for attempt in range(2):
            try:
                if attempt == 0:
                    current_prompt = prompt
                else:
                    # Retry with targeted instruction containing previous validation error
                    current_prompt = (
                        f"{prompt}\n\n"
                        f"IMPORTANT: Your previous output failed validation with error: {last_error}\n"
                        f"Please output strictly valid JSON matching the exact schema."
                    )

                logger.info("Invoking LLM requirement analyzer (attempt %s/2).", attempt + 1)
                raw_response = await self._generate(current_prompt, SYSTEM_PROMPT)
                last_raw_response = raw_response

                cleaned_json_str = self._extract_json_string(raw_response)
                parsed_dict = json.loads(cleaned_json_str)

                # Validate against Pydantic schema
                validated_data = RawAnalysisResponse.model_validate(parsed_dict)
                logger.info(
                    "Successfully analyzed project '%s': %s requirements, %s features.",
                    project_name,
                    len(validated_data.requirements),
                    len(validated_data.features),
                )
                return validated_data

            except json.JSONDecodeError as json_err:
                last_error = f"Malformed JSON: {str(json_err)}"
                logger.warning("Attempt %s produced malformed JSON: %s", attempt + 1, json_err)
                if attempt == 1:
                    from app.ai.providers.mock_provider import MockLLMProvider

                    if not isinstance(self.provider, MockLLMProvider):
                        return await self._fallback_to_mock(current_prompt, project_name, json_err)
                    raise LLMValidationException(
                        message=f"Failed to parse LLM response as valid JSON: {str(json_err)}",
                        raw_output=last_raw_response
                    )

            except ValidationError as val_err:
                last_error = f"Schema validation error: {str(val_err)}"
                logger.warning("Attempt %s failed schema validation: %s", attempt + 1, val_err)
                if attempt == 1:
                    from app.ai.providers.mock_provider import MockLLMProvider

                    if not isinstance(self.provider, MockLLMProvider):
                        return await self._fallback_to_mock(current_prompt, project_name, val_err)
                    raise LLMValidationException(
                        message=f"LLM response violated required schema: {str(val_err)}",
                        raw_output=last_raw_response,
                        details=val_err.errors()
                    )

            except Exception as provider_error:
                from app.ai.providers.mock_provider import MockLLMProvider

                if isinstance(self.provider, MockLLMProvider):
                    raise LLMProviderException(
                        str(provider_error),
                        provider=type(self.provider).__name__,
                    ) from provider_error
                return await self._fallback_to_mock(current_prompt, project_name, provider_error)

        raise LLMValidationException("Analysis failed after maximum retries.", raw_output=last_raw_response)
