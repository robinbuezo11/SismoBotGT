import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
                    leading-relaxed
                    text-[15px]

                    ${
                        isUser
                            ? 'bg-gray-300 text-gray-800'
                            : 'bg-sky-500 text-white'
                    }
                `}
            >
                <div
                    className={
                        isUser
                            ? `
                                prose
                                max-w-none

                                prose-p:my-2
                                prose-headings:my-3

                                prose-headings:text-gray-900
                                prose-p:text-gray-800
                                prose-strong:text-gray-900

                                prose-li:text-gray-800
                                prose-ul:text-gray-800
                                prose-ol:text-gray-800

                                prose-a:text-blue-700

                                prose-code:text-pink-700
                                prose-code:bg-gray-200
                                prose-code:px-1
                                prose-code:py-0.5
                                prose-code:rounded

                                prose-pre:bg-gray-200
                                prose-pre:text-gray-900
                              `
                            : `
                                prose
                                prose-invert
                                max-w-none

                                prose-p:my-2
                                prose-headings:my-3

                                prose-headings:text-white
                                prose-p:text-white
                                prose-strong:text-white

                                prose-li:text-white
                                prose-ul:text-white
                                prose-ol:text-white

                                prose-a:text-sky-200

                                prose-code:text-yellow-200
                                prose-code:bg-sky-800
                                prose-code:px-1
                                prose-code:py-0.5
                                prose-code:rounded

                                prose-pre:bg-sky-900
                                prose-pre:text-white
                              `
                    }
                >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content.replace(/\\n/g, '\n')}
                    </ReactMarkdown>
                </div>
            </div>
        </div>
    );
}