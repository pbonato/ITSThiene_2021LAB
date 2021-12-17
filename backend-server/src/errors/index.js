const notFound = require('./not-found')
const internalError = require('./internal')
const validationError = require('./validation-error')

module.exports = [notFound, validationError, internalError]