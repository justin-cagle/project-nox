export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 🌿 Brand Colors
        shadowmint: '#008777',
        'shadowmint-dark': '#9fffe0',
        cryocore: '#007b99',
        'cryocore-dark': '#00f5ff',

        // 🌌 Project Nox UI Tokens
        background: {
          DEFAULT: '#0e0f11', // Dark background
          light: '#fdfdfc', // Light background
        },
        surface: {
          DEFAULT: '#1a1c1f', // Cards and elevated surfaces
          light: '#f3f3f0',
        },
        text: {
          DEFAULT: '#e0e6ed', // Main text on dark
          muted: '#7a7f87', // Secondary labels
          dark: '#1a1b1d', // Main text on light
        },
        accent: {
          DEFAULT: '#52f2e6', // Cryo Core bright
          muted: '#29c7bb', // Shadowmint soft
          light: '#3ebeb2', // Accent for light mode
        },
        border: {
          DEFAULT: '#2a2d30',
          light: '#d6d6d2',
        },
        reaction: {
          DEFAULT: '#95a2af',
          light: '#7d8892',
        },
      },
    },
  },
  plugins: [],
}
