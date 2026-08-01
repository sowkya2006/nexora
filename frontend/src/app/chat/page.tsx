import { Suspense } from "react";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { Loader2 } from "lucide-react";

export const metadata = { title: "UniSphere AI – Nexora University" };

function ChatFallback() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="text-center space-y-3">
        <Loader2 className="h-8 w-8 animate-spin text-nexora-600 mx-auto" />
        <p className="text-sm text-slate-400 font-medium">Loading UniSphere AI…</p>
      </div>
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<ChatFallback />}>
      <ChatInterface />
    </Suspense>
  );
}
