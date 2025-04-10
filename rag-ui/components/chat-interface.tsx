"use client"

import type React from "react"

import { useRef, useEffect } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import ChatMessage from "@/components/chat-message"
import { useChat } from "@ai-sdk/react"

export default function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() === "") return
    handleSubmit(e)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-4">
              <h2 className="text-2xl font-semibold">Welcome to Angel One Support</h2>
              <p className="text-gray-500">Ask me anything about Angel One's services and support.</p>
            </div>
          </div>
        ) : (
          messages.map((message) => <ChatMessage key={message.id} role={message.role} content={message.content} />)
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t p-4">
        <form onSubmit={onSubmit} className="flex space-x-2">
          <Textarea
            value={input}
            onChange={handleInputChange}
            placeholder="Ask a question..."
            className="flex-1 resize-none"
            rows={1}
            maxRows={5}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                onSubmit(e)
              }
            }}
          />
          <Button
            type="submit"
            size="icon"
            disabled={isLoading || input.trim() === ""}
            className="h-full aspect-square"
          >
            <Send className="h-5 w-5" />
          </Button>
        </form>
      </div>
    </div>
  )
}
