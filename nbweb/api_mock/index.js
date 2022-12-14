module.exports = (req, res) => {
  const { faker } = require('@faker-js/faker')

  console.log('aaaaaaaa', res?.query)

  const TOTAL = 30
  const SKIP = 0
  const LIMIT = 10

  const data = {
    jobs: [],
  }

  for (let i = 0; i < TOTAL; i++) {
    data.jobs.push({
      id: faker.datatype.uuid(),
      title: `job-${i}-${faker.name.firstName()}`,
    })
  }
  return data
}
