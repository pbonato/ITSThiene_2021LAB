const express = require('express')
const router = express.Router()
const controller = require('./controller')

router.get('/get', controller.findAll)
router.get('/get/:mac', controller.findByMac)
router.post('/set/', controller.store)

module.exports = router