import { useState } from 'react';

export default function ChatInput({ onSend, loading }) {
    const [text, setText] = useState('');

    function handleSubmit(e) {
        e.preventDefault();

        if (!text.trim()) return;

        onSend(text);

        setText("");
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="
                flex
                items-center
                gap-4
                p-5
            "
        >
            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Escribe tu consulta..."
                className="
                    flex-1
                    bg-gray-300
                    text-gray-800
                    rounded-full
                    px-6
                    py-4
                    outline-none
                    text-lg
                    shadow-md
                "
            />

            <button
                type="submit"
                disabled={loading}
                className="
                    w-16
                    h-16
                    rounded-full
                    bg-sky-500
                    text-white
                    text-2xl
                    shadow-lg
                    hover:scale-105
                    transition
                "
            >
                ➤
            </button>
        </form>
    );
}