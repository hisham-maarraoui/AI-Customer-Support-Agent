import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_URL || (process.env.NODE_ENV === 'production' ? 'https://your-backend-url.railway.app' : 'http://localhost:8000');

export const useChat = () => {
    const [messages, setMessages] = useState([]);
    const [conversationId, setConversationId] = useState(null);
    const queryClient = useQueryClient();

    // Send message mutation
    const sendMessageMutation = useMutation(
        async (message) => {
            const response = await axios.post(`${API_BASE_URL}/api/chat`, {
                message,
                conversation_id: conversationId,
                user_id: 'anonymous', // In production, this would come from auth
            });
            return response.data;
        },
        {
            onSuccess: (data) => {
                // Add assistant response (user message is already added in sendMessage)
                const assistantMessage = {
                    role: 'assistant',
                    content: data.message,
                    timestamp: new Date().toISOString(),
                    confidence: data.confidence,
                    sources: data.sources || [],
                    guardrail_triggered: data.guardrail_triggered || false,
                    guardrail_type: data.guardrail_type,
                    tool_used: data.tool_used,
                    meeting_id: data.meeting_id,
                };

                setMessages(prev => [...prev, assistantMessage]);
                setConversationId(data.conversation_id);

                // Show success toast for tool usage
                if (data.tool_used === 'schedule_meeting') {
                    toast.success('Meeting scheduled successfully!');
                }
            },
            onError: (error) => {
                console.error('Error sending message:', error);
                toast.error('Failed to send message. Please try again.');
            },
        }
    );

    const sendMessage = useCallback(async (message) => {
        // Add user message immediately for optimistic UI
        const userMessage = {
            role: 'user',
            content: message,
            timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, userMessage]);

        // Send to API
        await sendMessageMutation.mutateAsync(message);
    }, [sendMessageMutation, conversationId]);

    const clearConversation = useCallback(() => {
        setMessages([]);
        setConversationId(null);
        queryClient.clear();
    }, [queryClient]);

    const isLoading = sendMessageMutation.isLoading;

    return {
        messages,
        isLoading,
        sendMessage,
        clearConversation,
        conversationId,
    };
}; 