import ChatInterface from "@/components/chat-interface"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <div className="w-full max-w-4xl mx-auto h-screen flex flex-col">
        <header className="border-b p-4">
          <h1 className="text-xl font-semibold">Angel One Support Assistant</h1>
        </header>
        <ChatInterface />
      </div>
    </main>
  )
}
