module.exports = {
    root: true,
    env: {
        browser: true,
        es2021: true,
    },
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    plugins: ['react', '@typescript-eslint'],
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:@typescript-eslint/recommended',
        'prettier', // disables formatting rules in favor of Prettier
    ],
    settings: {
        react: {
            version: 'detect',
        },
    },
    rules: {
        // Customize as you go
        'react/react-in-jsx-scope': 'off', // Not needed with Vite/React 17+
    },
}
