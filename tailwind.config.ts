import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#061421",
          900: "#0B1F33",
          800: "#12304A",
          700: "#194563",
        },
        teal: {
          50: "#F0FDFA",
          100: "#CCFBF1",
          500: "#14B8A6",
          600: "#0F766E",
          700: "#115E59",
        },
        slate: {
          25: "#FCFDFE",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      boxShadow: {
        soft: "0 20px 60px rgba(11, 31, 51, 0.08)",
        card: "0 10px 35px rgba(11, 31, 51, 0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
