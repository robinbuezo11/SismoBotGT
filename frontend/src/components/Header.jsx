import { useState } from "react";

export default function Header() {
    const [showAbout, setShowAbout] = useState(false);

    return (
        <>
            <header
                className="
                    sticky
                    top-0
                    z-50
                    bg-sky-500/90
                    backdrop-blur-md
                    text-white
                    shadow-2xl
                    border-b
                    border-white/10
                "
            >
                <div
                    className="
                        relative
                        w-full
                        px-4
                        sm:px-6
                        py-3
                        flex
                        items-center
                        justify-center
                    "
                >
                    <div className="flex items-center gap-3">
                        <img
                            src="/icon.svg"
                            alt="SismoBotGT"
                            className="w-10 h-10 sm:w-11 sm:h-11"
                        />

                        <h1 className="text-2xl sm:text-3xl font-bold">
                            SismoBotGT
                        </h1>
                    </div>
                    
                    <button
                        onClick={() => setShowAbout(true)}
                        className="
                            absolute
                            right-4
                            sm:right-6
                            lg:right-8
                            xl:right-10

                            top-1/2
                            -translate-y-1/2

                            w-10
                            h-10
                            sm:w-11
                            sm:h-11

                            rounded-full

                            bg-white/10
                            hover:bg-white/25

                            border
                            border-white/30

                            flex
                            items-center
                            justify-center

                            transition-all
                            duration-200

                            hover:scale-110
                            hover:rotate-3

                            shadow-md
                        "
                        aria-label="Información sobre SismoBotGT"
                        title="Acerca de SismoBotGT"
                    >
                        <span className="text-2xl leading-none">
                            ⓘ
                        </span>
                    </button>
                </div>
            </header>

            {/* Modal */}
            {showAbout && (
                <div
                    className="
                        fixed
                        inset-0
                        z-[100]
                        bg-black/50
                        backdrop-blur-sm
                        flex
                        items-center
                        justify-center
                        p-4
                    "
                    onClick={() => setShowAbout(false)}
                >
                    <div
                        className="
                            bg-white
                            text-gray-800
                            w-full
                            max-w-lg
                            rounded-2xl
                            shadow-2xl
                            p-6
                            sm:p-8
                            relative
                        "
                        onClick={(e) => e.stopPropagation()}
                    >
                        {/* Botón cerrar */}
                        <button
                            onClick={() => setShowAbout(false)}
                            className="
                                absolute
                                top-4
                                right-4
                                w-8
                                h-8
                                rounded-full
                                bg-gray-100
                                hover:bg-gray-200
                                text-gray-600
                                transition
                            "
                            aria-label="Cerrar"
                        >
                            ✕
                        </button>

                        {/* Logo */}
                        <div className="flex flex-col items-center text-center">
                            <img
                                src="/icon.svg"
                                alt="SismoBotGT"
                                className="w-20 h-20 mb-4"
                            />

                            <h2 className="text-2xl font-bold text-sky-600">
                                SismoBotGT
                            </h2>

                            <p className="text-gray-500 mt-2">
                                Asistente conversacional para información
                                sísmica en Guatemala.
                            </p>
                        </div>

                        <div className="mt-6 space-y-5">
                            {/* Proyecto */}
                            <div>
                                <h3 className="font-semibold text-gray-800">
                                    Proyecto de tesis
                                </h3>

                                <p className="text-sm text-gray-600 mt-1 leading-relaxed">
                                    Sistema desarrollado como parte de un
                                    proyecto de tesis, orientado a facilitar
                                    la consulta de información sobre actividad
                                    sísmica en Guatemala mediante una interfaz
                                    conversacional.
                                </p>
                            </div>

                            {/* Autor */}
                            <div>
                                <h3 className="font-semibold text-gray-800">
                                    Autor
                                </h3>

                                <p className="text-sm text-gray-600 mt-1">
                                    Robin Omar Buezo Díaz
                                </p>
                            </div>

                            {/* Año */}
                            <div className="pt-3 border-t border-gray-200 text-center">
                                <p className="text-sm text-gray-500">
                                    Proyecto académico · 2026
                                </p>
                            </div>
                        </div>

                        {/* Cerrar */}
                        <button
                            onClick={() => setShowAbout(false)}
                            className="
                                mt-6
                                w-full
                                bg-sky-500
                                hover:bg-sky-600
                                text-white
                                py-2.5
                                rounded-xl
                                font-medium
                                transition
                            "
                        >
                            Cerrar
                        </button>
                    </div>
                </div>
            )}
        </>
    );
}