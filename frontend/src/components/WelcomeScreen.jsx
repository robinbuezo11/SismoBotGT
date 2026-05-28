const suggestions = [
    "¿Hubo sismos hoy en Guatemala?",
    "¿Dónde fue el último sismo?",
    "¿Qué hacer durante un sismo?",
    "¿Qué es un sismo?"
];

export default function WelcomeScreen({ onSelect }) {
    return (
        <div
            className="
                flex
                flex-col
                items-center
                justify-center
                h-full
                text-center
                px-6
            "
        >
            <h2
                className="
                    text-4xl
                    font-bold
                    mb-10
                "
            >
                Hola 👋 soy SismoBotGT.
            </h2>

            <div
                className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    gap-4
                    max-w-2xl
                "
            >
                {
                    suggestions.map((item) => (
                        <button
                            key={item}
                            onClick={() => onSelect(item)}
                            className="
                                border
                                border-gray-300
                                rounded-full
                                px-6
                                py-4
                                hover:bg-gray-100
                                transition
                            "
                        >
                            {item}
                        </button>
                    ))
                }
            </div>
        </div>
    );
}