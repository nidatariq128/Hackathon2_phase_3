// Task: T-313 - Professional Chat Page
// Spec: specs/ai-chatbot/spec.md

"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { Spinner } from "@/components/ui/spinner";

export default function ChatPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  // Redirect if not authenticated
  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="py-2">
      <ChatInterface userId={user.id} />
    </div>
  );
}
