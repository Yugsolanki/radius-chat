/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.{html,js}","./base/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

