'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ProjectAnalysisResult, ChatMessage } from '../../types/project';
import { api } from '../../api/client';
import {
  Sparkles,
  Send,
  Bot,
  User,
  BookOpen,
  ArrowRight,
  Lightbulb,
  ShieldCheck,
  RefreshCw,
} from 'lucide-react';

interface ChatTabProps {
  result: ProjectAnalysisResult;
}

const DEFAULT_PROMPTS = [
  'Why is the backend effort estimation so high?',
  'What are the critical security and compliance risks?',
  'How can we reduce delivery time by 2-3 weeks?',
  'What is the recommended MVP scope for fast launch?',
  'Which database and cloud setup is best suited?',
];

export const ChatTab: React.FC<ChatTabProps> = ({ result }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: `Hello! I am your ProjectScope AI Architect. I have analyzed **${result.project?.name || 'your project'}** with **${result.features.length} features** and **${result.tasks.length} tasks** (~${result.total_estimated_hours.toFixed(0)} hours total). How can I help you refine or optimize this scope?`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      suggested_actions: [
        'How to optimize budget?',
        'Suggest MVP core features',
        'Show critical path',
      ],
    },
  ]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSending]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || isSending) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsSending(true);

    try {
      const response = await api.sendChatMessage(
        result.project_id,
        query,
        messages.slice(-4).map((m) => ({ role: m.role, content: m.content }))
      );

      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: response.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        citations: response.citations,
        suggested_actions: response.suggested_actions,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `I encountered an error retrieving architecture details: ${err.message || 'Please try again.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex flex-col h-[700px] bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden animate-in fade-in duration-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 text-white shadow-sm">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
              <span>AI Scope & Architecture Assistant</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                RAG Grounded
              </span>
            </h3>
            <p className="text-[11px] text-slate-500">
              Interactive conversational inquiry into tasks, costs, timeline, and tech stack
            </p>
          </div>
        </div>

        <button
          onClick={() => {
            setMessages([
              {
                id: 'welcome-reset',
                role: 'assistant',
                content: `Chat history cleared. How can I help you scope **${result.project?.name}**?`,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
              },
            ]);
          }}
          className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/60 transition-colors"
          title="Reset Conversation"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Message List */}
      <div className="flex-1 p-6 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start space-x-3 ${msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}
          >
            <div
              className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                msg.role === 'user'
                  ? 'bg-sky-600 text-white'
                  : 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white shadow-sm'
              }`}
            >
              {msg.role === 'user' ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
            </div>

            <div className={`max-w-[80%] space-y-2`}>
              <div
                className={`p-4 rounded-2xl text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-sky-600 text-white rounded-tr-none'
                    : 'bg-slate-100/90 text-slate-800 rounded-tl-none border border-slate-200/60'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Citations if available */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-200/60 text-[11px] space-y-1">
                    <div className="font-semibold text-slate-600 flex items-center space-x-1">
                      <BookOpen className="w-3 h-3 text-sky-600" />
                      <span>Retrieved Knowledge References:</span>
                    </div>
                    {msg.citations.map((c, i) => (
                      <div key={i} className="text-slate-500 bg-white/70 px-2 py-0.5 rounded border border-slate-200/50">
                        {c.title} <span className="text-[10px] text-sky-600 font-medium">({c.category})</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Suggested action pills */}
              {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {msg.suggested_actions.map((act, i) => (
                    <button
                      key={i}
                      onClick={() => handleSendMessage(act)}
                      className="px-2.5 py-1 rounded-lg text-[11px] font-medium bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200/60 transition-colors flex items-center space-x-1"
                    >
                      <span>{act}</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  ))}
                </div>
              )}

              <div className={`text-[10px] text-slate-400 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                {msg.timestamp}
              </div>
            </div>
          </div>
        ))}

        {isSending && (
          <div className="flex items-center space-x-3 text-slate-400 text-xs">
            <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-sky-500 animate-spin" />
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center space-x-2">
              <span className="inline-block w-1.5 h-1.5 bg-sky-500 rounded-full animate-bounce"></span>
              <span className="inline-block w-1.5 h-1.5 bg-sky-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span className="inline-block w-1.5 h-1.5 bg-sky-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              <span className="text-slate-500 text-[11px] font-medium ml-1">Analyzing RAG knowledge and project scope...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Prompts */}
      <div className="px-6 py-2 bg-slate-50/70 border-t border-slate-100 flex items-center space-x-2 overflow-x-auto">
        <Lightbulb className="w-3.5 h-3.5 text-amber-500 shrink-0" />
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider shrink-0">Try:</span>
        {DEFAULT_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(prompt)}
            className="px-2.5 py-1 text-[11px] rounded-lg bg-white border border-slate-200 text-slate-600 hover:text-sky-700 hover:border-sky-300 whitespace-nowrap transition-colors"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-slate-200 bg-white">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center space-x-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything about tasks, timeline, risks, or architecture..."
            className="flex-1 px-4 py-2.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={isSending || !input.trim()}
            className="px-4 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-700 disabled:opacity-40 text-white font-bold text-xs flex items-center space-x-1.5 shadow-md shadow-sky-600/20 transition-all"
          >
            <span>Send</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </div>
    </div>
  );
};
