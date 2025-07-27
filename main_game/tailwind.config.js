/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{html,svelte,js,ts,}",
        "./electron/**/*.{html,svelte,js,ts,}",
        "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
        "./node_modules/flowbite/**/*.js"
    ],

    theme: {
        extend: {
            fontFamily: {
                fredoka: ['"Fredoka One"', 'cursive'],
                poppins: ['Poppins', 'sans-serif']
            }
        },
    },
    plugins: [],
}