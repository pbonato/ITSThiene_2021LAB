const express = require('express')
const morgan = require('morgan')
const app = express()
const cors = require('cors')
const routes = require('./api/router')
const mongoose = require('mongoose')
const errorHandlers = require('./errors')

mongoose.connect('mongodb://localhost:27017/megaserver', { useNewUrlParser: true, useUnifiedTopology: true })
mongoose.set('debug', true)

app.use(cors())
app.use(express.json({ extended: true }))
app.use(morgan('tiny'))
app.use('/api', routes)

app.use(errorHandlers)

module.exports = app