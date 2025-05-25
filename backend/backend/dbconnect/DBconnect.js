const mongoose=require("mongoose");

exports.database=async ()=>{
    mongoose
    .connect("mongodb://127.0.0.1:27017/test")
    .then(()=>console.log("data-base connected"))
    .catch((err)=>console.log(err))
}