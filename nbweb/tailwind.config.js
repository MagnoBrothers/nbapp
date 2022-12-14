/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './component/**/*.{js,ts,jsx,tsx}',
    './node_modules/flowbite-react/**/*.js',
  ],
  theme: {
    // extend: {
    //   container: {
    //     center: true,
    //   },
    // },
    colors: {
      basins: {
        primary: '#954646',
        primary2: '#943939',
        primary3: '#6b2626',
        primary4: '#d99494',
        secondary: '#345eeb',
        pattern: {
          dark: '#dfdbe5',
          light: '#9c92ac',
        },
      },
    },
    // fontSize: {
    //   sm: '0.8rem',
    //   base: '1rem',
    //   xl: '1.25rem',
    //   '2xl': '1.563rem',
    //   '3xl': '1.953rem',
    //   '4xl': '2.441rem',
    //   '5xl': '3.052rem',
    //   hero: '6rem',
    // },
    //
    // typography: (theme) => ({
    //   DEFAULT: {
    //     css: {
    //       color: theme('colors.gray.700'),
    //       h2: {
    //         color: theme('colors.gray.800'),
    //       },
    //       h3: {
    //         color: theme('colors.gray.800'),
    //       },
    //       strong: {
    //         color: theme('colors.gray.800'),
    //       },
    //       a: {
    //         color: theme('colors.green.500'),
    //         '&:hover': {
    //           color: theme('colors.green.600'),
    //         },
    //       },
    //     },
    //   },
    // }),
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
    require('flowbite/plugin'),
  ],
}
