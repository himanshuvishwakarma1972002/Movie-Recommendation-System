const mongoose = require('mongoose')
const otpschema = mongoose.Schema({
    User_id:
    {
        type: String,
        required:true
    },
    Otp:
    {
        type: Number,
        required:true
    }
})
module.exports=mongoose.model('otp_data',otpschema)