import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot, ExternalLink } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ message }) => {
    const isUser = message.role === 'user';
    const timestamp = new Date(message.timestamp).toLocaleTimeString();

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
        >
            <div className={`flex items-start space-x-2 max-w-xs lg:max-w-md ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-apple-600' : 'bg-gray-200'
                    }`}>
                    {isUser ? (
                        <User size={16} className="text-white" />
                    ) : (
                        <Bot size={16} className="text-gray-600" />
                    )}
                </div>

                {/* Message Content */}
                <div className={`message-bubble ${isUser ? 'message-user' : 'message-assistant'}`}>
                    <div className="prose prose-sm max-w-none">
                        <ReactMarkdown
                            components={{
                                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                                a: ({ href, children }) => (
                                    <a
                                        href={href}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-apple-600 hover:text-apple-700 underline inline-flex items-center"
                                    >
                                        {children}
                                        <ExternalLink size={12} className="ml-1" />
                                    </a>
                                ),
                                code: ({ children }) => (
                                    <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">
                                        {children}
                                    </code>
                                ),
                                pre: ({ children }) => (
                                    <pre className="bg-gray-100 p-2 rounded text-sm overflow-x-auto">
                                        {children}
                                    </pre>
                                ),
                            }}
                        >
                            {message.content}
                        </ReactMarkdown>
                    </div>

                    {/* Timestamp */}
                    <div className={`text-xs mt-1 ${isUser ? 'text-apple-100' : 'text-gray-500'}`}>
                        {timestamp}
                    </div>

                    {/* Confidence indicator for assistant messages */}
                    {!isUser && message.confidence !== undefined && (
                        <div className="mt-2">
                            <div className="flex items-center space-x-2">
                                <span className="text-xs text-gray-500">Confidence:</span>
                                <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                                    <div
                                        className={`h-1.5 rounded-full transition-all duration-300 ${message.confidence >= 0.7
                                                ? 'bg-green-500'
                                                : message.confidence >= 0.4
                                                    ? 'bg-yellow-500'
                                                    : 'bg-red-500'
                                            }`}
                                        style={{ width: `${message.confidence * 100}%` }}
                                    />
                                </div>
                                <span className={`text-xs ${message.confidence >= 0.7
                                        ? 'text-green-600'
                                        : message.confidence >= 0.4
                                            ? 'text-yellow-600'
                                            : 'text-red-600'
                                    }`}>
                                    {Math.round(message.confidence * 100)}%
                                </span>
                            </div>
                        </div>
                    )}

                    {/* Sources indicator */}
                    {!isUser && message.sources && message.sources.length > 0 && (
                        <div className="mt-2">
                            <div className="text-xs text-gray-500">
                                Sources: {message.sources.length}
                            </div>
                        </div>
                    )}

                    {/* Guardrail indicator */}
                    {message.guardrail_triggered && (
                        <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                            ⚠️ This message was flagged by safety filters
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default ChatMessage; 