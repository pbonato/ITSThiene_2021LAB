const model = require('./model')

module.exports.store = async (req, res, next) => {
    try {
        const tmp = await model.store(req.params.mac, req.body)
        res.json(tmp)
        res.status(201)
    } catch (err) {
        next(err)
    }
}

module.exports.findAll = async (req, res, next) => {
    try {
        const list = await model.find()
        res.json(list)
    } catch (err) {
        next(err)
    }
}

module.exports.findByMac = async (req, res, next) => {
    try {
        const list = await model.findByMac(req.params.mac)
        res.json(list)
    } catch (err) {
        next(err)
    }
}

module.exports.findAllByMac = async (req, res, next) => {
    try {
        const list = await model.findAllByMac(req.params.mac)
        res.json(list)
    } catch (err) {
        next(err)
    }
}