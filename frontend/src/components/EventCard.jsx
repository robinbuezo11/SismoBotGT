function formatDate(dateString) {
    if (!dateString) return "No disponible";

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) return dateString;

    return date.toLocaleString("es-GT", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function magnitudeColor(magnitude = 0) {
    if (magnitude >= 7) return "bg-red-700";
    if (magnitude >= 6) return "bg-red-500";
    if (magnitude >= 5) return "bg-orange-500";
    if (magnitude >= 4) return "bg-yellow-500";
    if (magnitude >= 3) return "bg-lime-500";

    return "bg-green-500";
}

export default function EventCard({ event }) {
    return (
        <div
            className="
                bg-white
                text-gray-800
                rounded-xl
                border
                border-gray-200
                shadow-sm
                hover:shadow-lg
                transition
                p-4
            "
        >
            <div className="flex flex-col gap-3 sm:flex-row sm:justify-between sm:items-start">
                <div className="flex gap-3 items-center">
                    <span
                        className={`
                            ${magnitudeColor(event.magnitude)}
                            text-white
                            rounded-full
                            px-3
                            py-1
                            text-sm
                            font-bold
                            shrink-0
                        `}
                    >
                        M {event.magnitude}
                    </span>

                    <div>
                        <h4 className="text-sm font-semibold text-gray-900 leading-5 break-words">
                            {event.place}
                        </h4>

                        {event.id && (
                            <p className="text-xs text-gray-500 mt-1">
                                ID: {event.id}
                            </p>
                        )}
                    </div>
                </div>

                <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold shrink-0 ${
                        event.source === "USGS"
                            ? "bg-blue-100 text-blue-700"
                            : "bg-green-100 text-green-700"
                    }`}
                >
                    {event.source}
                </span>
            </div>

            <div className="mt-5 space-y-3 text-sm">
                <div>
                    <div className="text-gray-500 text-xs uppercase">
                        Fecha
                    </div>

                    <div className="font-medium text-gray-900">
                        {formatDate(event.time)}
                    </div>
                </div>

                <div>
                    <div className="text-gray-500 text-xs uppercase">
                        Profundidad
                    </div>

                    <div className="font-medium text-gray-900">
                        {event.depth} km
                    </div>
                </div>

                <div>
                    <div className="text-gray-500 text-xs uppercase">
                        Coordenadas
                    </div>

                    <div className="font-mono text-xs break-all text-gray-700">
                        <p className="text-xs text-gray-500 truncate">
                            📍 {event.latitude}, {event.longitude}
                        </p>
                    </div>
                </div>
            </div>

            <div className="flex flex-wrap gap-2 mt-5">
                {event.maps_url && (
                    <a
                        href={event.maps_url}
                        target="_blank"
                        rel="noreferrer"
                        className="
                            flex-1
                            text-center
                            bg-sky-600
                            hover:bg-sky-700
                            text-white
                            rounded-lg
                            py-2
                            px-3
                            text-xs
                            font-medium
                        "
                    >
                        📍 Maps
                    </a>
                )}

                {event.detail_url && (
                    <a
                        href={event.detail_url}
                        target="_blank"
                        rel="noreferrer"
                        className="
                            flex-1
                            text-center
                            bg-gray-700
                            hover:bg-gray-800
                            text-white
                            rounded-lg
                            py-2
                            px-3
                            text-xs
                            font-medium
                        "
                    >
                        🔗 Detalle
                    </a>
                )}
            </div>
        </div>
    );
}