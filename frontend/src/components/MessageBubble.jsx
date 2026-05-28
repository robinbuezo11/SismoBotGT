export default function MessageBubble({ role, content }) {
    const isUser = role === 'user';

    return (
        <div
            className={`
                flex
                mb-4
                ${isUser ? 'justify-end' : 'justify-start'}
            `}
        >
            <div
                className={`
                    max-w-[80%]
                    px-5
                    py-4
                    rounded-3xl
                    shadow-md
                    whitespace-pre-wrap
                    leading-relaxed
                    text-[15px]

                    ${isUser ? 'bg-gray-300 text-gray-800' : 'bg-sky-500 text-white'}
                `}
            >
                {content}
            </div>
        </div>
    );
}