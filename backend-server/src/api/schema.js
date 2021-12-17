const mongoose = require('mongoose')

let schema = mongoose.Schema({
        date: Date,
        mac: {type: String, required: true},
        red: false,
        green: false,
        blue: false,
    }, {
        collection: 'status',
    }
)

module.exports = mongoose.model('status', schema)