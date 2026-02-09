"use client";

import * as React from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { LogOut, ListTodo, MessageSquare, CheckSquare } from "lucide-react";
import { useAuth } from "@/lib/auth/auth-context";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, signOut, isLoading } = useAuth();

  React.useEffect(() => {
    if (!isLoading && !user) {
      router.push("/");
    }
  }, [user, isLoading, router]);

  const handleSignOut = async () => {
    signOut();
    router.push("/");
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#FAFAFA]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Navigation Bar */}
      <header className="glass sticky top-0 z-50 border-b border-gray-200/50">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          {/* Logo */}
          <Link href="/dashboard/tasks" className="flex items-center space-x-3 group">
            <div className="bg-gradient-to-r from-amber-500 to-orange-500 p-2 rounded-xl group-hover:shadow-lg transition-all">
              <CheckSquare className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-xl font-bold">
              <span className="gradient-text">TaskFlow</span>
            </h1>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-2">
            <Link
              href="/dashboard/tasks"
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${
                pathname?.startsWith("/dashboard/tasks")
                  ? "bg-amber-100 text-amber-700"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <ListTodo className="h-4 w-4" />
              <span className="font-medium">Tasks</span>
            </Link>
            <Link
              href="/dashboard/chat"
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${
                pathname === "/dashboard/chat"
                  ? "bg-amber-100 text-amber-700"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <MessageSquare className="h-4 w-4" />
              <span className="font-medium">AI Chat</span>
            </Link>
          </nav>

          {/* User Info & Sign Out */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-2 glass px-4 py-2 rounded-full">
              <div className="h-2 w-2 rounded-full bg-green-500"></div>
              <span className="text-sm font-medium text-gray-700">
                {user.email}
              </span>
            </div>
            <button
              onClick={handleSignOut}
              className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:bg-red-50 hover:text-red-600 transition-all rounded-xl"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline font-medium">Sign Out</span>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 glass border-t border-gray-200/50 z-50">
        <div className="flex justify-around py-2">
          <Link
            href="/dashboard/tasks"
            className={`flex flex-col items-center px-6 py-2 rounded-xl transition-all ${
              pathname?.startsWith("/dashboard/tasks")
                ? "text-amber-600 bg-amber-50"
                : "text-gray-500"
            }`}
          >
            <ListTodo className="h-6 w-6" />
            <span className="text-xs mt-1 font-medium">Tasks</span>
          </Link>
          <Link
            href="/dashboard/chat"
            className={`flex flex-col items-center px-6 py-2 rounded-xl transition-all ${
              pathname === "/dashboard/chat"
                ? "text-amber-600 bg-amber-50"
                : "text-gray-500"
            }`}
          >
            <MessageSquare className="h-6 w-6" />
            <span className="text-xs mt-1 font-medium">AI Chat</span>
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 pb-24 md:pb-8">{children}</main>
    </div>
  );
}
