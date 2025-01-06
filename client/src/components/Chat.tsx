import { useState, useRef, useEffect } from 'react'
import ChatMessage from './ChatMessage'

interface Message {
    id: number
    text: string
    sender: 'user' | 'bot'
}

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([])
    const [inputText, setInputText] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!inputText.trim()) return

        const userMessage: Message = {
            id: Date.now(),
            text: inputText,
            sender: 'user'
        }
        setMessages(prev => [...prev, userMessage])
        setInputText('')

        const response = await sendMessage(inputText)
        const botMessage: Message = {
            id: Date.now() + 1,
            text: response,
            sender: 'bot'
        }
        setMessages(prev => [...prev, botMessage])
    }

    const sendMessage = async (text: string) => {
        try {
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
            const response = await fetch(`${apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: text }),
            })
            const data = await response.json()
            return data.response
        } catch (error) {
            console.error('Error:', error)
            return 'Sorry, there was an error processing your request.'
        }
    }

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow-sm py-4 px-6 border-b">
                <h1 className="text-xl font-semibold text-gray-800">Crustdata Chat Assistant</h1>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto px-4 py-6">
                <div className="max-w-3xl mx-auto space-y-6">
                    {messages.map((message) => (
                        <ChatMessage key={message.id} message={message} />
                    ))}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Form */}
            <div className="bg-white border-t p-4">
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-4">
                    <input
                        type="text"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <button
                        type="submit"
                        className="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    )
} 