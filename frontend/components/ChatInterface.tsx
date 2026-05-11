"use client";

import { useState, useRef, useEffect } from "react";
import { SendHorizonal, RefreshCw, Loader2, ImageIcon } from "lucide-react";
import clsx from "clsx";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  imageBase64?: string;
  isStreaming?: boolean;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [generateImageEnabled, setGenerateImageEnabled] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [input]);

  const suggestedQuestions = [
    "What was the drainage system like?",
    "Tell me about the Great Bath",
    "How did people live in Mohenjo-daro?",
    "What caused the decline of the civilization?",
  ];

  const cleanMarkdown = (text: string) => {
    return text
      .replace(/\n#/g, '\n\n#')
      .replace(/\n(\d+\.)/g, '\n\n$1')
      .replace(/\n\*/g, '\n\n*');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const streamResponse = await fetch("http://localhost:8000/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content }),
      });

      const reader = streamResponse.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6);
              if (data === "[DONE]" || data.startsWith("Error:")) break;
              fullContent += data;
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMessage.id
                    ? { ...m, content: fullContent }
                    : m
                )
              );
            }
          }
        }
      }

      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMessage.id
            ? { ...m, isStreaming: false }
            : m
        )
      );

      if (generateImageEnabled) {
        await generateImage(fullContent);
      }
    } catch (error) {
      setMessages((prev) => {
        const updated = prev.filter((m) => m.id !== assistantMessage.id);
        return [
          ...updated,
          {
            id: (Date.now() + 1).toString(),
            role: "assistant" as const,
            content: "Sorry, I encountered an error. Please make sure the backend server is running.",
            isStreaming: false,
          },
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  const generateImage = async (prompt?: string) => {
    const imagePrompt = prompt || input;
    if (!imagePrompt.trim()) return;

    setIsLoading(true);

    const imageMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "Generating image...",
      isStreaming: true,
    };
    setMessages((prev) => [...prev, imageMessage]);

    try {
      const response = await fetch("http://localhost:8000/image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: imagePrompt }),
      });

      if (!response.ok) throw new Error("API error");

      const data = await response.json();
      setMessages((prev) =>
        prev.map((m) =>
          m.id === imageMessage.id
            ? {
                ...m,
                content: data.image_base64 ? "" : "Image generation failed. Please try again.",
                imageBase64: data.image_base64 || undefined,
                isStreaming: false,
              }
            : m
        )
      );
    } catch (error) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === imageMessage.id
            ? { ...m, content: "Image generation failed. Please try again.", isStreaming: false }
            : m
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto chat-scrollbar p-6 space-y-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center">
            <div className="text-center max-w-md">
              <div className="text-6xl mb-4">🏛️</div>
              <h2 className="text-2xl font-serif font-bold text-sand-800 mb-2">
                Explore Mohenjo-daro
              </h2>
              <p className="text-sand-500 mb-6">
                Ask me anything about the ancient Indus Valley Civilization. I can also
                generate images to help visualize this fascinating civilization.
              </p>
              <div className="grid grid-cols-2 gap-2">
                {suggestedQuestions.map((q) => (
                  <button
                    key={q}
                    onClick={() => setInput(q)}
                    className="text-left px-4 py-2.5 bg-white border border-sand-200 rounded-xl text-sm text-sand-700 hover:bg-sand-50 hover:border-sand-300 transition-all duration-200 shadow-sm"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              "flex",
              message.role === "user" ? "justify-end" : "justify-start"
            )}
          >
            <div
              className={clsx(
                "max-w-[80%] lg:max-w-[70%] rounded-2xl px-5 py-4 shadow-sm",
                message.role === "user"
                  ? "bg-primary-600 text-white"
                  : "bg-white border border-sand-200 text-sand-800"
              )}
            >
              <div className="text-sm leading-relaxed">
                {message.role === "assistant" ? (
                  <div className="text-sm text-sand-800">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({ children }) => <p className="text-lg font-bold mt-3 mb-1">{children}</p>,
                        h2: ({ children }) => <p className="text-base font-semibold mt-2 mb-1">{children}</p>,
                        h3: ({ children }) => <p className="text-sm font-semibold mt-2 mb-0.5">{children}</p>,
                        p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                        ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                        ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                        li: ({ children }) => <li className="mb-1">{children}</li>,
                        strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                        em: ({ children }) => <em className="italic">{children}</em>,
                        code: ({ children }) => <code className="bg-sand-100 px-1 rounded text-xs">{children}</code>,
                      }}
                    >
                      {cleanMarkdown(message.content)}
                    </ReactMarkdown>
                  </div>
                ) : (
                  message.content
                )}
              </div>

              {message.imageBase64 && (
                <div className="mt-3 rounded-lg overflow-hidden">
                  <img
                    src={message.imageBase64}
                    alt="Generated"
                    className="max-w-full h-auto rounded-lg"
                  />
                </div>
              )}
            </div>
          </div>
        ))}

        {/* {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-sand-200 rounded-2xl px-5 py-4 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-sand-400 rounded-full animate-bounce [animation-delay:0ms]" />
                  <span className="w-2 h-2 bg-sand-400 rounded-full animate-bounce [animation-delay:150ms]" />
                  <span className="w-2 h-2 bg-sand-400 rounded-full animate-bounce [animation-delay:300ms]" />
                </div>
                <span className="text-sm text-sand-500">Thinking...</span>
              </div>
            </div>
          </div>
        )} */}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-sand-200 bg-white/50 backdrop-blur-md p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex items-end gap-3">
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                placeholder="Ask about Mohenjo-daro..."
                className="w-full resize-none rounded-xl border border-sand-300 bg-white px-4 py-3 text-sand-800 placeholder-sand-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
                rows={1}
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="mb-2 p-3 bg-primary-600 hover:bg-primary-700 disabled:bg-sand-200 disabled:cursor-not-allowed text-white rounded-xl transition-all duration-200 shadow-sm"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <SendHorizonal className="w-5 h-5" />
              )}
            </button>
          </div>

          <div className="flex items-center justify-between mt-3 text-xs text-sand-400">
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={generateImageEnabled}
                  onChange={(e) => setGenerateImageEnabled(e.target.checked)}
                  className="w-4 h-4 rounded border-sand-300 text-primary-600 focus:ring-primary-500"
                />
                <span>Generate Image</span>
              </label>
            </div>
            <span>Powered by FastAPI + Hugging Face</span>
          </div>
        </form>
      </div>
    </div>
  );
}
