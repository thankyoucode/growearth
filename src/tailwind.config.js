module.exports = {
  content: [
    "./templates/**/*.html", // Include all HTML templates
    "./apps/**/*.html", // Include app-specific templates
    "./static/js/**/*.js", // Include JavaScript files in static
    "./src/static/**/*.css", // Include CSS files in static/src
    "./**/*.py", // Include Python files for inline classes
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
    },
  },
  plugins: [],
};
