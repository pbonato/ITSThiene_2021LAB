const schema = require('./schema')
const moment = require('moment')

module.exports.store = async (mac, data) => {
    data.date = moment(new Date()).utcOffset(0, true)
    if (await schema.findOne(mac)) {
        return schema.findOneAndUpdate(mac, data, {returnOriginal: false})
    }
    return schema.create(data)
}

module.exports.find = async () => {
    return await schema.find().sort({ date: 'desc' });
}

module.exports.findByMac = async (query) => {
    const q = {}
    q.mac = query
    return await schema.findOne(q).sort({date: 'desc'})
}