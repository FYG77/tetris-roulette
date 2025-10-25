/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        neon: {
          blue: "#00f6ff",
          pink: "#ff00f6",
          purple: "#8a2be2"
        }
      },
      boxShadow: {
        neon: "0 0 10px rgba(0, 246, 255, 0.7)"
      }
    }
  },
  plugins: []
};
