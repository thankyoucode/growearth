module.exports = {
  content: [
    "./templates/**/*.html",
    "./app/**/*.html",
    "./**/*.html",
    "./app/**/*.py",
    "./**/*.py",
    "./static/src/input.css",
    "./static/js/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#A2A915", // apple-green
        secondary: "#547131", // fern-green
        tertiary: "#6C92B6", // blue-gray
        saffron: "#EDC363", // saffron
        darkBrown: "#3F3929", // dark-brown
      },
      backgroundColor: {
        "alert-success": "#48bb78",
        "alert-error": "#f56565",
        "alert-warning": "#ecc94b",
        "alert-info": "#4299e1",
      },
      textColor: {
        "alert-text": "#ffffff",
      },
      animation: {
        "slide-in": "slideIn 0.3s ease-out",
        "slide-out": "slideOut 0.3s ease-in",
      },
      keyframes: {
        slideIn: {
          "0%": { transform: "translateX(100%)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        slideOut: {
          "0%": { transform: "translateX(0)", opacity: "1" },
          "100%": { transform: "translateX(100%)", opacity: "0" },
        },
      },
    },
  },
  plugins: [],
};
