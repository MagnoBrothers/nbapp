module.exports = (req, res, next) => {
  res.header('X-Hello', 'World')

  // console.log(req.body)

  console.log(res.write)
  next()
}
