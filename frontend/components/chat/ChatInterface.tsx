// Task: T-312 - TaskFlow Style Chat UI
// Spec: specs/ai-chatbot/spec.md

"use client";

import * as React from "react";
import {
  Send,
  Bot,
  User,
  Loader2,
  Sparkles,
  ListTodo,
  CheckCircle2,
  Trash2,
  PenLine,
  MessageSquare,
  Mic,
  Image,
  Zap,
  Brain,
  Eye,
  Volume2
} from "lucide-react";
import { sendMessage } from "@/lib/api/chat";
import type { Message, ToolCall } from "@/lib/types/chat";

interface ChatInterfaceProps {
  userId: string;
}

// Quick action suggestions
const QUICK_ACTIONS = [
  { icon: ListTodo, label: "Show tasks", message: "Show all my tasks" },
  { icon: CheckCircle2, label: "Pending", message: "Show my pending tasks" },
  { icon: Sparkles, label: "Add task", message: "Add a task to " },
];

// Feature badges
const FEATURES = [
  { icon: MessageSquare, label: "Text", color: "bg-amber-100 text-amber-700" },
  { icon: Mic, label: "Voice", color: "bg-blue-100 text-blue-700" },
  { icon: Image, label: "Image", color: "bg-purple-100 text-purple-700" },
];

// Capabilities
const CAPABILITIES = [
  { icon: Brain, label: "Context Awareness", desc: "Understands your tasks" },
  { icon: Zap, label: "Instant Actions", desc: "Quick task management" },
  { icon: Eye, label: "Visual Understanding", desc: "Smart responses" },
  { icon: Volume2, label: "Voice Commands", desc: "Speak naturally" },
];

export function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = React.useState<Message[]>([]);
  const [input, setInput] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  const [conversationId, setConversationId] = React.useState<number | undefined>();
  const [error, setError] = React.useState<string | null>(null);
  const [toolCalls, setToolCalls] = React.useState<ToolCall[]>([]);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    await sendChatMessage(input.trim());
  };

  const sendChatMessage = async (message: string) => {
    setInput("");
    setError(null);
    setToolCalls([]);

    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendMessage(userId, message, conversationId);
      setConversationId(response.conversation_id);

      if (response.tool_calls.length > 0) {
        setToolCalls(response.tool_calls);
      }

      const assistantMsg: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.response,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setError(err.message);
      setMessages((prev) => prev.filter((m) => m.id !== userMsg.id));
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action: typeof QUICK_ACTIONS[0]) => {
    if (action.message.endsWith(" ")) {
      setInput(action.message);
      inputRef.current?.focus();
    } else {
      sendChatMessage(action.message);
    }
  };

  const getToolIcon = (toolName: string) => {
    switch (toolName) {
      case 'add_task': return <Sparkles className="h-3 w-3" />;
      case 'list_tasks': return <ListTodo className="h-3 w-3" />;
      case 'complete_task': return <CheckCircle2 className="h-3 w-3" />;
      case 'delete_task': return <Trash2 className="h-3 w-3" />;
      case 'update_task': return <PenLine className="h-3 w-3" />;
      default: return <Sparkles className="h-3 w-3" />;
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header Section */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-3">
          <span className="gradient-text">AI-Powered</span> Task Assistant
        </h1>
        <p className="text-gray-600 text-lg">
          Manage your tasks naturally with our intelligent chatbot
        </p>

        {/* Feature Badges */}
        <div className="flex justify-center gap-3 mt-4">
          {FEATURES.map((feature, index) => (
            <div
              key={index}
              className={`flex items-center gap-2 px-4 py-2 rounded-full ${feature.color} text-sm font-medium`}
            >
              <feature.icon className="h-4 w-4" />
              {feature.label}
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Container */}
      <div className="glass rounded-3xl shadow-2xl overflow-hidden">
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-amber-500 to-orange-500 p-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="bg-white/20 backdrop-blur-sm p-3 rounded-2xl">
                  <Bot className="h-7 w-7 text-white" />
                </div>
                <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-green-400 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h2 className="font-bold text-xl text-white">TaskFlow AI</h2>
                <p className="text-sm text-white/80">Always ready to help</p>
              </div>
            </div>
            {conversationId && (
              <div className="text-xs text-white/70 bg-white/20 px-3 py-1.5 rounded-full">
                Session #{conversationId}
              </div>
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div className="h-[450px] overflow-y-auto bg-white/50 p-6 space-y-5">
          {/* Welcome State */}
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center px-4">
              <div className="bg-gradient-to-br from-amber-100 to-orange-100 p-6 rounded-3xl mb-6 animate-float">
                <MessageSquare className="h-14 w-14 text-amber-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">
                Welcome to <span className="gradient-text">TaskFlow AI</span>
              </h3>
              <p className="text-gray-500 mb-6 max-w-md">
                I can help you manage tasks using natural language. Try these quick actions:
              </p>

              {/* Quick Actions */}
              <div className="flex flex-wrap justify-center gap-3 mb-8">
                {QUICK_ACTIONS.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickAction(action)}
                    className="flex items-center gap-2 px-5 py-3 bg-white border border-gray-200 rounded-xl hover:border-amber-300 hover:bg-amber-50 transition-all duration-200 shadow-sm hover:shadow card-hover"
                  >
                    <action.icon className="h-5 w-5 text-amber-500" />
                    <span className="text-gray-700 font-medium">{action.label}</span>
                  </button>
                ))}
              </div>

              {/* Capabilities Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-2xl">
                {CAPABILITIES.map((cap, index) => (
                  <div
                    key={index}
                    className="glass rounded-xl p-4 text-center card-hover"
                  >
                    <cap.icon className="h-6 w-6 text-amber-500 mx-auto mb-2" />
                    <p className="text-sm font-semibold text-gray-800">{cap.label}</p>
                    <p className="text-xs text-gray-500">{cap.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-4 ${
                message.role === "user" ? "justify-end" : "justify-start"
              } animate-fadeIn`}
            >
              {message.role === "assistant" && (
                <div className="flex-shrink-0">
                  <div className="bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 rounded-xl shadow-lg">
                    <Bot className="h-5 w-5 text-white" />
                  </div>
                </div>
              )}

              <div className={`max-w-[75%]`}>
                <div
                  className={`rounded-2xl px-5 py-3.5 shadow-sm ${
                    message.role === "user"
                      ? "bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-br-md"
                      : "glass text-gray-800 rounded-bl-md"
                  }`}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                </div>
                <p className={`text-xs text-gray-400 mt-1.5 ${
                  message.role === "user" ? "text-right" : "text-left"
                }`}>
                  {new Date(message.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>

              {message.role === "user" && (
                <div className="flex-shrink-0">
                  <div className="bg-gray-100 p-2.5 rounded-xl">
                    <User className="h-5 w-5 text-gray-600" />
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Loading State */}
          {isLoading && (
            <div className="flex gap-4 justify-start animate-fadeIn">
              <div className="flex-shrink-0">
                <div className="bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 rounded-xl shadow-lg">
                  <Bot className="h-5 w-5 text-white" />
                </div>
              </div>
              <div className="glass rounded-2xl rounded-bl-md px-5 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                  <span className="text-gray-500">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          {/* Tool Calls Display */}
          {toolCalls.length > 0 && !isLoading && (
            <div className="flex justify-start pl-14 animate-slideIn">
              <div className="flex flex-wrap gap-2">
                {toolCalls.slice(0, 3).map((tc, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-1.5 text-xs bg-amber-50 text-amber-700 px-3 py-1.5 rounded-full border border-amber-200"
                  >
                    {getToolIcon(tc.tool)}
                    <span className="font-medium">{tc.tool.replace('_', ' ')}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="flex justify-center animate-fadeIn">
              <div className="bg-red-50 text-red-600 px-5 py-3 rounded-xl border border-red-200 flex items-center gap-2">
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {error}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions Bar (when in conversation) */}
        {messages.length > 0 && (
          <div className="px-4 py-3 bg-gray-50/80 border-t border-gray-100">
            <div className="flex gap-2 overflow-x-auto">
              {QUICK_ACTIONS.map((action, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickAction(action)}
                  disabled={isLoading}
                  className="flex items-center gap-1.5 px-4 py-2 text-sm bg-white border border-gray-200 rounded-full hover:border-amber-300 hover:bg-amber-50 transition-all whitespace-nowrap disabled:opacity-50"
                >
                  <action.icon className="h-4 w-4 text-amber-500" />
                  <span className="text-gray-600 font-medium">{action.label}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <form
          onSubmit={handleSubmit}
          className="bg-white border-t border-gray-100 p-5"
        >
          <div className="flex gap-3 items-center">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type a message... (e.g., 'Add a task to buy groceries')"
                disabled={isLoading}
                className="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent disabled:bg-gray-100 transition-all placeholder:text-gray-400"
              />
            </div>
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="btn-primary p-4 rounded-2xl shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
            >
              {isLoading ? (
                <Loader2 className="h-6 w-6 animate-spin" />
              ) : (
                <Send className="h-6 w-6" />
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Footer Text */}
      <p className="text-center text-gray-400 text-sm mt-6">
        Powered by AI • Press Enter to send
      </p>
    </div>
  );
}
