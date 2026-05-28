export default function Header() {
    return (
        <header
            className="
                sticky
                top-0
                z-50

                bg-sky-500/90
                backdrop-blur-md

                text-white
                text-center
                py-4

                shadow-2xl
                border-b
                border-white/10
            "
        >
            <h1 className="text-3xl font-bold">
                SismoBotGT
            </h1>
        </header>
    );
}