/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        attila: {
          primary: '#22D3EE',    // Teal/Cyan from logo
          secondary: '#F59E0B',  // Orange/Gold from logo
          dark: '#1F2937',       // Dark background
          darker: '#111827',     // Darker background
          light: '#F9FAFB',      // Light background
          gray: '#6B7280',       // Gray text
        }
      },
      fontFamily: {
        'attila': ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

