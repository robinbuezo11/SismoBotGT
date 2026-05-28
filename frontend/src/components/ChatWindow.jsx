import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, loading }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    return (
        <div
            className="
                flex-1
                overflow-y-auto
                px-6
                py-6
            "
        >
            {messages.map((msg, idx) => (
                <MessageBubble
                    key={idx}
                    role={msg.role}
                    content={msg.content}
                />
            ))}
            {loading && (
                <div 
                    className="
                        flex
                        items-center
                        gap-2
                        bg-white
                        w-fit
                        px-4
                        py-3
                        rounded-2xl
                        shadow-sm
                    "
                >
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-75"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-150"></div>
                    </div>
                </div>
            )}
            <div ref={bottomRef} />
        </div>
    );
}