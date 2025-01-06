import React from 'react';
import { LightAsync as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vs2015 } from 'react-syntax-highlighter/dist/cjs/styles/hljs';
import ReactMarkdown from 'react-markdown';

interface Message {
    id: number;
    text: string;
    sender: 'user' | 'bot';
}

interface MessagePart {
    type: 'text' | 'code';
    content: string;
    language?: string;
}

interface ChatMessageProps {
    message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
    // Helper function to parse code blocks and text
    const parseMessage = (text: string): MessagePart[] => {
        const parts: MessagePart[] = [];
        const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
        let lastIndex = 0;
        let match: RegExpExecArray | null;

        while ((match = codeBlockRegex.exec(text)) !== null) {
            // Add text before code block
            if (match.index > lastIndex) {
                parts.push({
                    type: 'text',
                    content: text.slice(lastIndex, match.index)
                });
            }

            // Add code block
            parts.push({
                type: 'code',
                language: match[1] || 'plaintext',
                content: match[2].trim()
            });

            lastIndex = match.index + match[0].length;
        }

        // Add remaining text
        if (lastIndex < text.length) {
            parts.push({
                type: 'text',
                content: text.slice(lastIndex)
            });
        }

        return parts;
    };

    const renderContent = (part: MessagePart, index: number): React.ReactNode => {
        const isUserMessage = message.sender === 'user'; // Determine if the message is from the user

        if (part.type === 'code') {
            return (
                <div key={index} className="mt-4 mb-4">
                    <div className="bg-[#1E1E1E] rounded-lg overflow-hidden">
                        <div className="flex justify-between items-center px-4 py-2 bg-[#2D2D2D] border-b border-[#404040]">
                            <span className="text-gray-400 text-sm">{part.language}</span>
                            <button
                                className="text-gray-400 hover:text-white text-sm"
                                onClick={() => {
                                    navigator.clipboard.writeText(part.content);
                                }}
                            >
                                Copy code
                            </button>
                        </div>
                        <SyntaxHighlighter
                            language={part.language}
                            style={vs2015}
                            customStyle={{
                                margin: 0,
                                padding: '1rem',
                                background: '#1E1E1E',
                            }}
                        >
                            {part.content}
                        </SyntaxHighlighter>
                    </div>
                </div>
            );
        }

        return (
            <div key={index} className={`prose prose-invert max-w-none ${isUserMessage ? 'text-white' : 'text-gray-800'}`}>
                <ReactMarkdown>
                    {part.content}
                </ReactMarkdown>
            </div>
        );
    };

    const parts = parseMessage(message.text);

    return (
        <div className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`p-6 rounded-lg max-w-[90%] ${message.sender === 'user'
                    ? 'bg-blue-600 rounded-br-none'
                    : 'bg-white rounded-bl-none'
                    }`}
            >
                {parts.map((part, index) => renderContent(part, index))}
            </div>
        </div>
    );
};

export default ChatMessage;