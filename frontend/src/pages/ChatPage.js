import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, RefreshCw, ExternalLink } from 'lucide-react';
import toast from 'react-hot-toast';
import ChatMessage from '../components/ChatMessage';
import SourcesList from '../components/SourcesList';
import { useChat } from '../hooks/useChat';

const ChatPage = () => {
    const {
        messages,
        isLoading,
        sendMessage,
        clearConversation,
        conversationId
    } = useChat();

    const [inputMessage, setInputMessage] = useState('');
    const [showSources, setShowSources] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isLoading) return;

        const message = inputMessage.trim();
        setInputMessage('');

        try {
            await sendMessage(message);
            setShowSources(true);
        } catch (error) {
            toast.error('Failed to send message. Please try again.');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(e);
        }
    };

    const handleClearChat = () => {
        clearConversation();
        setShowSources(false);
        toast.success('Conversation cleared');
    };

    return (
        <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold text-gray-900 dark:text-white mb-2"
                >
                    Apple Support AI Agent
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-gray-600 dark:text-gray-300"
                >
                    Ask me anything about Apple products and services
                </motion.p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Chat Interface */}
                <div className="lg:col-span-2">
                    <div className="card h-[600px] flex flex-col">
                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4">
                            <AnimatePresence>
                                {messages.map((message, index) => (
                                    <motion.div
                                        key={index}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: -20 }}
                                        transition={{ duration: 0.3 }}
                                    >
                                        <ChatMessage message={message} />
                                    </motion.div>
                                ))}
                            </AnimatePresence>

                            {/* Loading indicator */}
                            {isLoading && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex justify-start"
                                >
                                    <div className="message-bubble message-assistant">
                                        <div className="typing-indicator">
                                            <div className="typing-dot"></div>
                                            <div className="typing-dot"></div>
                                            <div className="typing-dot"></div>
                                        </div>
                                    </div>
                                </motion.div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input */}
                        <div className="border-t border-gray-200 p-4">
                            <form onSubmit={handleSendMessage} className="flex space-x-2">
                                <input
                                    ref={inputRef}
                                    type="text"
                                    value={inputMessage}
                                    onChange={(e) => setInputMessage(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder="Ask me about Apple products..."
                                    className="input-field flex-1"
                                    disabled={isLoading}
                                />
                                <button
                                    type="submit"
                                    disabled={!inputMessage.trim() || isLoading}
                                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <Send size={18} />
                                </button>
                            </form>
                        </div>

                        {/* Clear chat button */}
                        {messages.length > 0 && (
                            <div className="px-4 pb-4">
                                <button
                                    onClick={handleClearChat}
                                    className="btn-secondary text-sm"
                                >
                                    <RefreshCw size={16} className="mr-2" />
                                    Clear Chat
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* Sources Panel */}
                <div className="lg:col-span-1">
                    <div className="card h-[600px] flex flex-col">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-semibold text-gray-900">
                                Sources & Information
                            </h3>
                            <button
                                onClick={() => setShowSources(!showSources)}
                                className="text-apple-600 hover:text-apple-700"
                            >
                                {showSources ? 'Hide' : 'Show'}
                            </button>
                        </div>

                        {showSources && (
                            <div className="flex-1 overflow-y-auto">
                                <SourcesList
                                    sources={messages[messages.length - 1]?.sources || []}
                                    confidence={messages[messages.length - 1]?.confidence || 0}
                                />
                            </div>
                        )}

                        {/* Conversation Info */}
                        <div className="border-t border-gray-200 pt-4 mt-4">
                            <div className="text-sm text-gray-600">
                                <p>Conversation ID: {conversationId}</p>
                                <p>Messages: {messages.length}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="mt-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Quick Questions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[
                        "How do I reset my iPhone?",
                        "My Mac is running slowly",
                        "How to backup to iCloud?",
                        "Apple Watch won't pair"
                    ].map((question, index) => (
                        <motion.button
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            onClick={() => {
                                setInputMessage(question);
                                inputRef.current?.focus();
                            }}
                            className="p-3 text-left bg-white border border-gray-200 rounded-lg hover:border-apple-300 hover:bg-apple-50 transition-colors duration-200"
                        >
                            <p className="text-sm text-gray-700">{question}</p>
                        </motion.button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ChatPage; 