// module.exports = (req, res) => {
//   const { faker } = require('@faker-js/faker')

//   // console.log('aaaaaaaa', res?.query)

//   // const TOTAL = 30
//   // const SKIP = 0
//   // const LIMIT = 10

//   // const data = {
//   //   jobs: [],
//   // }

//   // for (let i = 0; i < TOTAL; i++) {
//   //   data.jobs.push({
//   //     id: faker.datatype.uuid(),
//   //     title: `job-${i}-${faker.name.firstName()}`,
//   //   })
//   // }
//   // return data
// }
const { faker } = require('@faker-js/faker')

const jsonServer = require('json-server')
const { default: next } = require('next')
const server = jsonServer.create()
const router = jsonServer.router('routes.json')
const middlewares = jsonServer.defaults()

const TOTAL = 30

server.use(jsonServer.bodyParser)
server.use(middlewares)

// Custom middleware to access POST methids.
// Can be customized for other HTTP method as well.
server.use((req, res, next) => {
  console.log('POST request listener')
  const body = req.body
  console.log(body)
  if (req.method === 'POST') {
    // If the method is a POST echo back the name from request body
    res.json({ message: 'User created successfully', name: req.body.name })
  } else {
    //Not a post request. Let db.json handle it
    console.log('aaaaaaaaaaaa', req.query)
    next()
  }
})

// server.use(router)

function pagination(req, res, next) {
  console.log('pagination!!!!!!!!!!')
  console.log('query', req.query)
  // console.log(res.locals.data)

  // res.end(JSON.stringify({ a: 1 }))
  res.send(res.locals.data)
  // next()
}

server.get(
  '/jobs',
  function (req, res, next) {
    console.log('vvvvvvvvvvvv')
    res.setHeader('Content-Type', 'application/json')

    const data = {
      jobs: [],
    }

    for (let i = 0; i < TOTAL; i++) {
      data.jobs.push({
        id: faker.datatype.uuid(),
        title: `job-${i}-${faker.name.firstName()}`,
      })
    }

    // res.end(JSON.stringify({ a: 1 }))
    // res.send(data)
    res.locals.data = data
    next()
  },
  pagination,
)

server.listen(4000, () => {
  console.log('JSON Server is running')
})
