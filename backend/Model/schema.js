const mongoose = require('mongoose')
const USerschema = mongoose.Schema({
    Name:
    {
        type: String,
        required:true
    }, Email:
    {
        type: String,
        required:true,
        unique:true
    },
    Password:
    {
        type: Number,
        required:true
    },
    Confirm_password:
    {
        type: Number,
        required:false
    },
    status:{
        type:String,
        enum:['active','inactive'],
        required:true,
        default:"inactive"
    }
})
module.exports=mongoose.model('new_data',USerschema)