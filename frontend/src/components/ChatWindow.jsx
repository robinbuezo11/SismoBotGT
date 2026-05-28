import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

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
            <div ref={bottomRef} />
        </div>
    );
}