import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        sand: {
          50: "#faf6f1",
          100: "#f5ede3",
          200: "#e8d5be",
          300: "#d4b896",
          400: "#c19a6b",
          500: "#b08b5b",
          600: "#a17a4a",
          700: "#86613d",
          800: "#6d4f35",
          900: "#5a422c",
        },
        terracotta: {
          50: "#fef6f3",
          100: "#fde8e1",
          200: "#fad0c2",
          300: "#f5ae99",
          400: "#ee876a",
          500: "#e66847",
          600: "#d44d2d",
          700: "#b13a23",
          800: "#91301f",
          900: "#782a1d",
        },
        primary: {
          50: "#fef6f3",
          100: "#fde8e1",
          200: "#fad0c2",
          300: "#f5ae99",
          400: "#ee876a",
          500: "#e66847",
          600: "#d44d2d",
          700: "#b13a23",
          800: "#91301f",
          900: "#782a1d",
        },
      },
      fontFamily: {
        serif: ["Georgia", "Cambria", "Times New Roman", "serif"],
      },
    },
  },
  plugins: [],
};
export default config;
