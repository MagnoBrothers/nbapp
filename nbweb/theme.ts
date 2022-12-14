import { createTheme } from '@mui/material'

const appTheme = createTheme({
  palette: {
    primary: {
      light: '#954646',
      main: '#954646',
      dark: '#954646',
    },
    secondary: {
      light: '#1a7d81',
      main: '#1a7d81',
      dark: '#1a7d81',
    },
    background: {
      default: '#efefef',
    },
    // background: {
    //   main: '#cdcdcd',
    // },
  },
})

appTheme.typography.h1 = {
  fontSize: '2rem',
  '@media (min-width:600px)': {
    fontSize: '3rem',
  },
  '@media (min-width:900px)': {
    fontSize: '5rem',
  },
  '@media (min-width:1200px)': {
    fontSize: '7rem',
  },
}

appTheme.typography.h4 = {
  fontSize: '1rem',
  '@media (min-width:600px)': {
    fontSize: '1.2rem',
  },
  '@media (min-width:900px)': {
    fontSize: '2rem',
  },
  '@media (min-width:1200px)': {
    fontSize: '2.3rem',
  },
}

export default appTheme
