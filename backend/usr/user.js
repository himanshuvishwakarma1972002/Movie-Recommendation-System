const express=require('express')
const route=express.Router();
const {Register,Login,otpveify,forgtpass,verifyotp,changepass,resendforgtpass,resendotp}=require("../controllers/controls")

// *********---------Register
route.post('/save',Register)
route.post('/otp_verify',otpveify)
route.post('/resendotp',resendotp)

// *********---------Login
route.post('/check',Login)
route.post('/forgotp',forgtpass)
route.post('/forgotpverify',verifyotp)
route.patch('/updatepass',changepass)
route.post('/resendforgtpass',resendforgtpass)
module.exports=route;