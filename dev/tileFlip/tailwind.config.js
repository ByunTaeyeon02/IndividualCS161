module.exports = {
  content: ["./src/**/*.svelte", "./public/index.html"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  corePlugins: {
    preflight: false, // Disable base styles
  },
};

