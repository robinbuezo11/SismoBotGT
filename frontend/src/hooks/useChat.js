import { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import api from '../services/api';

const sessionId = localStorage.getItem('session_id') || uuidv4();

localStorage.setItem('session_id', sessionId);

export function useChat() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    async function sendMessage(text) {
        if (!text.trim()) return;

        const userMessage = {
            role: 'user',
            content: text,
        };

        setMessages((prev) => [...prev, userMessage]);
        setLoading(true);

        try {
            const response = await api.post('/chat', {
                message: text,
                user_id: sessionId,
            });

            const botMessage = {
                role: 'assistant',
                content: typeof response.data.answer === 'string' 
                    ? response.data.answer 
                    : JSON.stringify(response.data.answer, null, 2),
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Ocurrió un error al procesar la solicitud.',
                },
            ]);
        } finally {
            setLoading(false);
        }
    }

    return { messages, loading, sendMessage };
}