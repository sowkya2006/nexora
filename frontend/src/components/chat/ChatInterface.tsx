"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import {
  Bot, Send, Trash2, FileText, Sparkles, Loader2,
  Download, ExternalLink, ChevronRight,
} from "lucide-react";
import { SUGGESTED_QUESTIONS } from "@/lib/constants";
import { sendChatMessage, type ChatMessage, type ChatSource } from "@/lib/mockChat";

/* ------------------------------------------------------------------ */
/* Simple Markdown renderer — no extra dependency needed               */
/* ------------------------------------------------------------------ */
function renderMarkdown(text: string): string {
  let html = text
    // Escape HTML entities first
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    // Headers
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold + italic
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Horizontal rule
    .replace(/^---+$/gm, '<hr>')
    // Unordered list items — collect them below
    .replace(/^[\-\*] (.+)$/gm, '<li>$1</li>')
    // Ordered list items
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // Wrap consecutive <li> in <ul>
    .replace(/(<li>[\s\S]*?<\/li>)(\n(?!<li>)|$)/g, (match) => `<ul>${match}</ul>`)
    // Double newlines → paragraph break
    .replace(/\n\n+/g, '</p><p>')
    // Single newlines within paragraphs → <br>
    .replace(/\n/g, '<br>');

  // Wrap in paragraph if not already
  if (!html.startsWith('<')) html = `<p>${html}</p>`;
  return html;
}

function MarkdownMessage({ content }: { content: string }) {
  return (
    <div
      className="markdown-body"
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
    />
  );
}

/* ------------------------------------------------------------------ */
/* Session / storage helpers                                           */
/* ------------------------------------------------------------------ */
function getSessionId(): string {
  if (typeof window === "undefined") return crypto.randomUUID();
  let id = localStorage.getItem("unisphere_session_id");
  if (!id) { id = crypto.randomUUID(); localStorage.setItem("unisphere_session_id", id); }
  return id;
}

interface StoredChat {
  id: string;
  title: string;
  messages: ChatMessage[];
  timestamp: number;
}

/* ------------------------------------------------------------------ */
/* Source citation card                                                */
/* ------------------------------------------------------------------ */
function CitationCard({ source, index }: { source: ChatSource; index: number }) {
  // view_url and download_url are fully resolved by mockChat.ts
  const viewUrl = source.view_url || source.download_url || "#";
  const downloadUrl = source.download_url || source.view_url || "#";

  const handleDownload = (e: React.MouseEvent) => {
    e.preventDefault();
    // Create a temporary <a> and trigger download
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = source.file_name || source.document_name + ".pdf";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="rounded-xl border border-[#E7E0D4] bg-[#FFFDF8] p-3.5 text-xs space-y-2 transition hover:border-[#D9B97A] hover:shadow-sm">
      {/* Title row */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-1.5 font-bold text-[#3E3A34] min-w-0">
          <FileText className="h-3.5 w-3.5 shrink-0 text-[#44563E]" />
          <span className="truncate">{source.document_name}</span>
        </div>
        <div className="flex items-center gap-1.5 shrink-0">
          <span className="rounded-full bg-[#F0EAE1] px-2 py-0.5 text-[10px] font-bold text-[#44563E]">
            Src {index + 1}
          </span>
          {source.page && (
            <span className="rounded-full bg-[#44563E] px-2 py-0.5 text-[10px] font-bold text-white">
              P.{source.page}
            </span>
          )}
        </div>
      </div>

      {/* Snippet */}
      {source.snippet && (
        <p className="text-[11px] text-[#8C857C] italic leading-relaxed border-l-2 border-[#D9B97A] pl-2.5 line-clamp-3">
          &ldquo;{source.snippet}&rdquo;
        </p>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3 pt-1.5 border-t border-[#E7E0D4]">
        <a
          href={viewUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-[11px] font-bold text-[#44563E] hover:underline"
        >
          <ExternalLink className="h-3 w-3" /> View PDF
        </a>
        <span className="text-[#D9D2C5]">•</span>
        <button
          onClick={handleDownload}
          className="inline-flex items-center gap-1 text-[11px] font-bold text-[#44563E] hover:underline"
        >
          <Download className="h-3 w-3" /> Download
        </button>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Main ChatInterface component                                        */
/* ------------------------------------------------------------------ */
export function ChatInterface() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q");

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<StoredChat[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false); // reserved for mobile sidebar toggle
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const initialQueryFired = useRef(false);

  useEffect(() => {
    const stored = localStorage.getItem("unisphere_chat_history");
    if (stored) { try { setChatHistory(JSON.parse(stored)); } catch { /* ignore */ } }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (initialQuery && !initialQueryFired.current) {
      initialQueryFired.current = true;
      handleSend(initialQuery);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialQuery]);

  const saveHistory = (history: StoredChat[]) => {
    setChatHistory(history);
    localStorage.setItem("unisphere_chat_history", JSON.stringify(history));
  };

  const handleSend = useCallback(async (text?: string) => {
    const message = (text ?? input).trim();
    if (!message || loading) return;

    const userMsg: ChatMessage = { role: "user", content: message };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await sendChatMessage(message, getSessionId(), messages);
      const assistantMsg: ChatMessage = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };
      const finalMessages = [...newMessages, assistantMsg];
      setMessages(finalMessages);

      const chatId = activeChatId ?? crypto.randomUUID();
      const title = message.slice(0, 55) + (message.length > 55 ? "…" : "");
      const updatedHistory = chatHistory.filter((c) => c.id !== chatId);
      updatedHistory.unshift({ id: chatId, title, messages: finalMessages, timestamp: Date.now() });
      saveHistory(updatedHistory.slice(0, 25));
      setActiveChatId(chatId);
    } catch {
      setMessages([...newMessages, {
        role: "assistant",
        content: "I could not find this information in the uploaded university documents.",
      }]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [input, loading, messages, activeChatId, chatHistory]);

  const handleClear = () => { setMessages([]); setActiveChatId(null); };

  const loadChat = (chat: StoredChat) => {
    setMessages(chat.messages);
    setActiveChatId(chat.id);
    setSidebarOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 animate-fade-in">
      <div className="grid gap-6 lg:grid-cols-12">

        {/* ── Left sidebar: History + AI info ── */}
        <div className="hidden lg:flex lg:col-span-3 flex-col gap-5">
          {/* History */}
          <div className="storybook-card p-5 flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-[#E7E0D4] pb-3">
              <span className="text-[10px] font-bold uppercase tracking-widest text-[#8C857C]">History</span>
              <button onClick={handleClear}
                className="flex items-center gap-1 rounded-lg px-2 py-1 text-[10px] font-bold text-[#8C857C] hover:bg-[#F0EAE1] hover:text-[#3E3A34] transition">
                <Trash2 className="h-3 w-3" /> Clear
              </button>
            </div>
            <div className="space-y-1.5 max-h-80 overflow-y-auto pr-1">
              {chatHistory.length === 0 ? (
                <p className="py-6 text-center text-xs text-[#8C857C]">No conversations yet</p>
              ) : (
                chatHistory.map((chat) => (
                  <button key={chat.id} onClick={() => loadChat(chat)}
                    className={`w-full rounded-xl px-3 py-2.5 text-left text-xs transition ${
                      activeChatId === chat.id
                        ? "bg-[#44563E] text-white font-bold shadow-sm"
                        : "text-[#3E3A34] hover:bg-[#F0EAE1]"
                    }`}>
                    <p className="truncate font-semibold leading-tight">{chat.title}</p>
                    <p className={`text-[10px] mt-0.5 ${activeChatId === chat.id ? "text-[#D9B97A]" : "text-[#8C857C]"}`}>
                      {new Date(chat.timestamp).toLocaleDateString(undefined, { month: "short", day: "numeric" })}
                      {" · "}{chat.messages.length / 2 | 0} Q&As
                    </p>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* AI persona card */}
          <div className="storybook-card p-5 bg-gradient-to-br from-[#44563E] to-[#2b3927] text-white space-y-2.5">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[#D9B97A] animate-pulse" />
              <span className="text-xs font-extrabold text-[#D9B97A]">UniSphere AI</span>
            </div>
            <p className="text-[11px] text-[#D9E3D4] leading-relaxed">
              Trained on official university PDFs — answers admissions, fees, hostel, placement, and academic queries with exact page citations.
            </p>
            <div className="flex items-center gap-1.5 pt-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-[10px] text-emerald-300 font-semibold">Knowledge base active</span>
            </div>
          </div>
        </div>

        {/* ── Main chat area ── */}
        <div className="lg:col-span-9 storybook-card flex flex-col" style={{ height: "calc(100vh - 10rem)", minHeight: "600px" }}>

          {/* Chat header */}
          <div className="flex items-center justify-between border-b border-[#E7E0D4] px-6 py-4 shrink-0">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#44563E] shadow-sm">
                <Bot className="h-6 w-6 text-[#D9B97A]" />
              </div>
              <div>
                <h1 className="font-extrabold text-[#3E3A34] text-base">UniSphere AI Counselor</h1>
                <p className="text-[11px] text-[#8C857C] font-semibold">Nexora University RAG Assistant</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="hidden sm:flex items-center gap-1.5 rounded-full bg-emerald-50 border border-emerald-200 px-3 py-1 text-[11px] font-bold text-emerald-700">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                RAG Active
              </span>
              {messages.length > 0 && (
                <button onClick={handleClear}
                  className="rounded-xl border border-[#E7E0D4] px-3 py-1.5 text-[11px] font-bold text-[#8C857C] hover:bg-[#F0EAE1] transition">
                  New Chat
                </button>
              )}
            </div>
          </div>

          {/* Messages stream */}
          <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5">
            {messages.length === 0 && (
              <div className="py-10 text-center space-y-5 max-w-lg mx-auto">
                <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-[#F0EAE1] mx-auto">
                  <Bot className="h-8 w-8 text-[#44563E]" />
                </div>
                <div>
                  <h2 className="text-xl font-extrabold text-[#3E3A34]">How may I assist you?</h2>
                  <p className="mt-1 text-xs text-[#8C857C] leading-relaxed">
                    Ask about admissions, fees, hostel regulations, placements, or academic programs.
                  </p>
                </div>
                <div className="flex flex-wrap justify-center gap-2 pt-1">
                  {SUGGESTED_QUESTIONS.map((q) => (
                    <button key={q} onClick={() => handleSend(q)}
                      className="rounded-2xl border border-[#E7E0D4] bg-[#F8F4EC] px-4 py-2 text-[11px] font-bold text-[#3E3A34] hover:border-[#D9B97A] hover:bg-[#F0EAE1] transition flex items-center gap-1.5">
                      <ChevronRight className="h-3 w-3 text-[#44563E]" /> {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                {msg.role === "assistant" && (
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-[#44563E] text-[#D9B97A] text-[10px] font-extrabold mt-0.5">
                    AI
                  </div>
                )}

                <div className={`max-w-[85%] space-y-3 ${msg.role === "user" ? "" : ""}`}>
                  <div className={`rounded-2xl px-4 py-3 text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "bg-[#44563E] text-white font-medium shadow-sm"
                      : "bg-[#F8F4EC] border border-[#E7E0D4] text-[#3E3A34]"
                  }`}>
                    {msg.role === "user"
                      ? <p className="whitespace-pre-wrap">{msg.content}</p>
                      : <MarkdownMessage content={msg.content} />
                    }
                  </div>

                  {msg.sources && msg.sources.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-[#8C857C] px-1">
                        Verified Sources ({msg.sources.length})
                      </p>
                      <div className="grid gap-2 sm:grid-cols-2">
                        {msg.sources.map((src, si) => (
                          <CitationCard key={si} source={src} index={si} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {msg.role === "user" && (
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-[#D9B97A] text-[#3E3A34] text-[10px] font-extrabold mt-0.5">
                    YOU
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 justify-start">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-[#44563E] text-[#D9B97A] text-[10px] font-extrabold">
                  AI
                </div>
                <div className="rounded-2xl bg-[#F8F4EC] border border-[#E7E0D4] px-4 py-3 flex items-center gap-2">
                  <Loader2 className="h-3.5 w-3.5 animate-spin text-[#44563E]" />
                  <span className="text-xs text-[#8C857C] font-medium">Searching university documents…</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input bar */}
          <div className="border-t border-[#E7E0D4] px-6 py-4 shrink-0">
            <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-2.5 items-end">
              <textarea
                ref={inputRef}
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about admissions, fees, hostel, placements…"
                disabled={loading}
                className="flex-1 resize-none rounded-2xl border border-[#E7E0D4] bg-[#F8F4EC] px-4 py-3 text-xs font-medium text-[#3E3A34] placeholder-[#B8B0A2] focus:border-[#D9B97A] focus:bg-white focus:outline-none transition max-h-28 overflow-y-auto"
                style={{ lineHeight: "1.5" }}
              />
              <button type="submit" disabled={loading || !input.trim()}
                className="rounded-2xl bg-[#44563E] px-5 py-3 text-xs font-bold text-white hover:bg-[#384833] disabled:opacity-50 flex items-center gap-2 shadow-sm transition shrink-0 self-end">
                <Send className="h-4 w-4 text-[#D9B97A]" />
                <span>Send</span>
              </button>
            </form>
            <p className="mt-1.5 text-center text-[10px] text-[#B8B0A2]">
              Press <kbd className="rounded bg-[#F0EAE1] px-1 py-0.5 font-mono text-[9px]">Enter</kbd> to send · <kbd className="rounded bg-[#F0EAE1] px-1 py-0.5 font-mono text-[9px]">Shift+Enter</kbd> for new line
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
