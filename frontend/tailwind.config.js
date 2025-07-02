/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        shadowmint: '#008777',
        'shadowmint-dark': '#9fffe0',
        cryocore: '#007b99',
        'cryocore-dark': '#00f5ff',
      },
    },
  },
  plugins: [],
}
