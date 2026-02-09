"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Plus, ListTodo, CheckCircle2, Clock } from "lucide-react";
import { Task, TaskStatus } from "@/lib/types/task";
import { getTasks } from "@/lib/api/tasks";
import { configureAuthHeader, getAuthToken } from "@/lib/api/client";
import { TaskCard } from "./TaskCard";
import { clsx } from "clsx";

interface TaskListProps {
  userId: string;
}

export function TaskList({ userId }: TaskListProps) {
  const router = useRouter();
  const [tasks, setTasks] = React.useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = React.useState<Task[]>([]);
  const [statusFilter, setStatusFilter] = React.useState<TaskStatus>("all");
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    loadTasks();
  }, [userId]);

  React.useEffect(() => {
    filterTasks();
  }, [tasks, statusFilter]);

  const loadTasks = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const token = getAuthToken();
      if (token) {
        configureAuthHeader(token);
      }

      const fetchedTasks = await getTasks(userId);
      const sorted = [...fetchedTasks].sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
      setTasks(sorted);
    } catch (err) {
      console.error("Failed to load tasks:", err);
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  };

  const filterTasks = () => {
    switch (statusFilter) {
      case "completed":
        setFilteredTasks(tasks.filter((task) => task.completed));
        break;
      case "pending":
        setFilteredTasks(tasks.filter((task) => !task.completed));
        break;
      case "all":
      default:
        setFilteredTasks(tasks);
        break;
    }
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
    );
  };

  const handleTaskDelete = (taskId: number) => {
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  };

  const handleCreateTask = () => {
    router.push("/dashboard/tasks/new");
  };

  const pendingCount = tasks.filter((t) => !t.completed).length;
  const completedCount = tasks.filter((t) => t.completed).length;
  const completionRate = tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0;

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-gray-500">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass rounded-2xl p-6 border border-red-200 bg-red-50/50">
        <h3 className="text-lg font-semibold text-red-900">Error Loading Tasks</h3>
        <p className="mt-2 text-sm text-red-700">{error}</p>
        <button
          onClick={loadTasks}
          className="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded-xl hover:bg-red-200 transition-all font-medium"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">
          <span className="gradient-text">My Tasks</span>
        </h1>
        <p className="text-gray-600">Manage and track your daily tasks efficiently</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="glass rounded-2xl p-4 text-center card-hover">
          <div className="bg-amber-100 w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-2">
            <ListTodo className="h-6 w-6 text-amber-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">{tasks.length}</p>
          <p className="text-xs text-gray-500">Total Tasks</p>
        </div>
        <div className="glass rounded-2xl p-4 text-center card-hover">
          <div className="bg-orange-100 w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-2">
            <Clock className="h-6 w-6 text-orange-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">{pendingCount}</p>
          <p className="text-xs text-gray-500">Pending</p>
        </div>
        <div className="glass rounded-2xl p-4 text-center card-hover">
          <div className="bg-green-100 w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-2">
            <CheckCircle2 className="h-6 w-6 text-green-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">{completionRate}%</p>
          <p className="text-xs text-gray-500">Completed</p>
        </div>
      </div>

      {/* Create Button & Filter */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <button
          onClick={handleCreateTask}
          className="btn-primary px-6 py-3 rounded-xl font-semibold flex items-center gap-2 shadow-lg"
        >
          <Plus className="h-5 w-5" />
          New Task
        </button>

        {/* Filter Tabs */}
        <div className="flex gap-2 glass rounded-xl p-1.5">
          {(["all", "pending", "completed"] as TaskStatus[]).map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={clsx(
                "px-5 py-2.5 text-sm font-medium rounded-lg transition-all duration-200",
                statusFilter === status
                  ? "bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-md"
                  : "text-gray-600 hover:bg-gray-100"
              )}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
              <span className={clsx(
                "ml-2 px-2 py-0.5 rounded-full text-xs font-bold",
                statusFilter === status ? "bg-white/20" : "bg-gray-200"
              )}>
                {status === "all"
                  ? tasks.length
                  : status === "completed"
                  ? completedCount
                  : pendingCount}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Task List or Empty State */}
      {filteredTasks.length === 0 ? (
        <div className="glass rounded-3xl p-12 text-center">
          <div className="bg-gradient-to-br from-amber-100 to-orange-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 animate-float">
            <Plus className="h-10 w-10 text-amber-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            {statusFilter === "all"
              ? "No tasks yet"
              : statusFilter === "completed"
              ? "No completed tasks"
              : "No pending tasks"}
          </h3>
          <p className="text-gray-500 max-w-sm mx-auto mb-6">
            {statusFilter === "all"
              ? "Get started by creating your first task and boost your productivity!"
              : `No ${statusFilter} tasks to show right now.`}
          </p>
          {statusFilter === "all" && (
            <button
              onClick={handleCreateTask}
              className="btn-primary px-8 py-4 rounded-xl font-semibold text-lg inline-flex items-center gap-2"
            >
              <Plus className="h-5 w-5" />
              Create Your First Task
            </button>
          )}
        </div>
      ) : (
        <div className="grid gap-4">
          {filteredTasks.map((task, index) => (
            <div
              key={task.id}
              className="animate-fadeIn"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <TaskCard
                task={task}
                userId={userId}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
