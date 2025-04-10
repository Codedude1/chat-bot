import { Avatar } from "@/components/ui/avatar"
import { User, Bot } from "lucide-react"
import { cn } from "@/lib/utils"

interface ChatMessageProps {
  role: "user" | "assistant" | string
  content: string
}

export default function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user"

  return (
    <div className={cn("flex gap-3 items-start", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <Avatar className="h-8 w-8 bg-primary text-primary-foreground">
          <Bot className="h-5 w-5" />
        </Avatar>
      )}

      <div className={cn("rounded-lg p-4 max-w-[80%]", isUser ? "bg-primary text-primary-foreground" : "bg-muted")}>
        <p className="whitespace-pre-wrap">{content}</p>
      </div>

      {isUser && (
        <Avatar className="h-8 w-8 bg-secondary text-secondary-foreground">
          <User className="h-5 w-5" />
        </Avatar>
      )}
    </div>
  )
}
