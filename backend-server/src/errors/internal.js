module.exports = (err, req, res, next) => {
    console.log(err)
    res.status(500)
    res.send('Internal Error')
}