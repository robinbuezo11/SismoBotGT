import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import EventCard from "./EventCard";

export default function MessageBubble({
    role,
    content,
    events = [],
    metadata = null,
}) {
    const isUser = role === "user";

    const MAX_EVENTS = 12;
    const visibleEvents = events.slice(0, MAX_EVENTS);

    return (
        <div
            className={`flex mb-4 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >
            <div
                className={`max-w-[90%] rounded-3xl shadow-md px-5 py-4 ${
                    isUser
                        ? "bg-gray-300 text-gray-800"
                        : "bg-sky-500 text-white"
                }`}
            >
                <div
                    className={
                        isUser
                            ? `
                                prose
                                max-w-none
                                prose-p:text-gray-800
                                prose-headings:text-gray-900
                            `
                            : `
                                prose
                                prose-invert
                                prose-p:text-white
                                prose-headings:text-white
                                prose-li:text-white
                                prose-a:text-sky-200
                                max-w-none
                            `
                    }
                >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content.replace(/\\n/g, "\n")}
                    </ReactMarkdown>
                </div>

                {!isUser && events.length > 0 && (
                    <>
                        <hr className="border-white/20 my-6" />

                        <div className="bg-sky-600/40 rounded-xl p-5 mb-6">
                            <h3 className="text-lg font-semibold">
                                Eventos encontrados en las últimas 24 horas
                            </h3>

                            <p className="text-sm mt-2">
                                Se encontraron{" "}
                                <strong>{metadata?.cantidad}</strong> eventos.
                            </p>

                            <p className="text-sm">
                                País:{" "}
                                <strong>{metadata?.pais}</strong>
                            </p>

                            {metadata?.fuentes?.length > 0 && (
                                <div className="flex gap-2 flex-wrap mt-3">
                                    {metadata.fuentes.map((fuente) => (
                                        <span
                                            key={fuente}
                                            className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                                fuente === "USGS"
                                                    ? "bg-blue-100 text-blue-800"
                                                    : "bg-green-100 text-green-800"
                                            }`}
                                        >
                                            {fuente}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div
                            className="
                                max-h-[650px]
                                overflow-y-auto
                                pr-2
                            "
                        >
                            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                                {visibleEvents.map((event, index) => (
                                    <EventCard
                                        key={`${event.source}-${event.id ?? index}`}
                                        event={event}
                                    />
                                ))}
                            </div>
                        </div>

                        {events.length > MAX_EVENTS && (
                            <div className="mt-6 text-center text-sm text-white">
                                Mostrando únicamente los primeros{" "}
                                <strong>{MAX_EVENTS}</strong> eventos más
                                fuertes.
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}