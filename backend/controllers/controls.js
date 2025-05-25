const user = require("../Model/schema")
const otpvalue = require("../Model/otpschema")
const speakeasy = require("speakeasy")
const helpers = require("../helper/common")
// ########################------------Register
const nodemailer = require('nodemailer');
require('dotenv').config(); // Load environment variables

exports.Register = async (req, res) => {
    try {
        const { Name, Email, Password, Confirm_password } = req.body;
        console.log("sgjsda",req.body)

        // Validation
        if (!Name || !Email || !Password || !Confirm_password) {
            return res.status(400).json({ error: 'All fields are required' });
        }
        if (Password !== Confirm_password) {
            return res.status(400).json({ error: 'Passwords do not match' });
        }

        // Check if Email already exists
        const presence = await user.findOne({ Email: Email });
        if (presence) {
            return res.status(400).json({ error: "Email is already taken" });
        }

        // Hash password
        // const hashedPassword = await bcrypt.hash(String(Password), 10);


        // Save user
        const userData = await user.create({
            Name,
            Email,
            Password
        });

        // Generate OTP
        const otpSecret = speakeasy.generateSecret({ length: 20 });
        const otp = speakeasy.totp({
            secret: otpSecret.base32,
            encoding: 'base32'
        });

        // Save OTP
        await otpvalue.create({
            User_id: userData._id,
            Otp: otp
        });

        // Send OTP via Email
        const transporter = nodemailer.createTransport({
            service: "gmail",
            secure: true,
            port: 465,
            auth: {
                user: "himanshu1972002@gmail.com",
                pass: "uwhq xeag rvcx uwns"
            }
        });

        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: Email,
            subject: "OTP Verification",
            text: `Your OTP is: ${otp}`
        };

        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.error("Error sending email:", error);
                return res.status(500).json({ error: "Failed to send otp to email.Please check your email" });
            }
            console.log("Email sent: " + info.response);
            return res.status(201).json({message: "User registered successfully! OTP sent to email.", User_id: userData._id,status:true });
        });

    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({
            status: false,
            message: "Registration failed due to an error.",
            error: error.message
        });
    }
};

exports.resendotp = async (req, res) => {
    try {
        const { User_id } = req.body;
        console.log("body sentresend")

        const Data = await user.findOne({ _id: User_id })
        // console.log(Data);
        const dletes = await otpvalue.deleteMany()
        if (Data) {
            const otpSecret = speakeasy.generateSecret({ length: 20 });
            const otp = speakeasy.totp({
                secret: otpSecret.base32,
                encoding: 'base32',

            });
            // console.log("Otp", otp)
            const otpPaylod = {
                User_id: Data._id,
                Otp: otp
            };
            const otpData = await otpvalue.create(otpPaylod);
            // console.log(otpData);
            
            // res.status(201).json({Mesage:"hello bsdk ji"})
            const transporter = nodemailer.createTransport({
                service: "gmail",
                secure: true,
                port: 465,
                auth: {
                    user: "himanshu1972002@gmail.com",
                    pass: "uwhq xeag rvcx uwns"
                }
            });

            const mailOptions = {
                from: "himanshu1972002@gmail.com",
                to: Data.Email,
                subject: "OTP Verification",
                text: `Your Resend OTP is: ${otp}`
            };
            console.log(mailOptions);
            

            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error("Error sending email:", error);
                    return res.status(500).json({ error: "Failed to send OTP email" });
                }
                console.log("Email sent: " + info.response);
                return res.status(201).json({ message: " OTP resent to email.",status:true });
            });
        } else {
            res.json("Input id is not correct")
        }
    } catch (error) {
        console.log(error);
        res.status(400).json({
            status: false,
            message: "Not successfully ",
            data: []
        })
    }
}
exports.otpveify = async (req, res) => {
    try {
        const { User_id, Otp } = req.body;
        let change = Number(Otp)
        const userdata = await otpvalue.findOne({ User_id: User_id })
        if (!userdata) {
            return res.json({error:"ID not matched"})
        }
        if (userdata.Otp !== change) {
            return res.json({error:"otp not matched "})
        }
        const dletes = await otpvalue.deleteMany({ User_id: User_id })
        return res.status(200).json({
            status: true,
            message: " Otp verify successfully",
        });


    } catch {
        console.error('Error during login:', error)
        res.status(400).json({
            status: false,
            message: "Iternal server error",
            data: []
        })
    }
}
// ########################------------LOGIN

exports.Login = async (req, res) => {
    try {
        const { Email, Password } = req.body;
        var change = Number(Password)

        user.findOne({ Email })
            .then(user => {
                if (user) {
                    if (user.Password === change) {
                        res.status(200).json({
                            status: true,
                            statuscode: 200,
                            message: "login successfully"
                        })
                    } else {
                        res.json("password is not matched")
                    }
                } else {
                    res.json("Email is not valid")
                }
            })
    } catch (error) {
        console.error('Error during login:', error); // Log the error for debugging
        res.status(500).json({
            status: false,
            message: "An error occurred during login"
        });
    }
}
exports.forgtpass = async (req, res) => {
    try {
        const { Email } = req.body;
        const Data = await user.findOne({ Email: Email })
        if (Data) {
            const otpSecret = speakeasy.generateSecret({ length: 20 });
            const otp = speakeasy.totp({
                secret: otpSecret.base32,
                encoding: 'base32',

            });
            // console.log("Otp", otp)
            const otpPaylod = {
                User_id: Data._id,
                Otp: otp
            };

            // Save OTP data
            const otpData = await otpvalue.create(otpPaylod);
            // Send OTP via Email
            const transporter = nodemailer.createTransport({
                service: "gmail",
                secure: true,
                port: 465,
                auth: {
                    user: "himanshu1972002@gmail.com",
                    pass: "uwhq xeag rvcx uwns"
                }
            });

            const mailOptions = {
                from: "himanshu1972002@gmail.com",
                to: Email,
                subject: "OTP Verification for Forgotten Password",
                text: `Your OTP is: ${otp}`
            };
             console.log(mailOptions)
            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error("Error sending email:", error);
                    return res.status(500).json({ error: "Failed to send OTP email" });
                }
                console.log("Email sent: " + info.response);
                return res.status(201).json({ "status": true,message: "forgot password successfully OTP sent to your  email.", User_id: Data._id });
            });
        } else {
            res.json("Input Email is not correct")
        }
    } catch {
        res.status(400).json({
            status: false,
            message: "Not successfully forgotp",
            data: []
        })
    }
}
exports.resendforgtpass = async (req, res) => {
    try {
        const { User_id } = req.body;
        console.log("resend body", User_id)

        const Data = await user.findOne({ _id: User_id })
        const dletes = await otpvalue.deleteMany({ User_id: User_id })
        if (Data) {
            const otpSecret = speakeasy.generateSecret({ length: 20 });
            const otp = speakeasy.totp({
                secret: otpSecret.base32,
                encoding: 'base32',

            });
            // console.log("Otp", otp)
            const otpPaylod = {
                User_id: Data._id,
                Otp: otp
            };
            const otpData = await otpvalue.create(otpPaylod);
            const transporter = nodemailer.createTransport({
                service: "gmail",
                secure: true,
                port: 465,
                auth: {
                    user: "himanshu1972002@gmail.com",
                    pass: "uwhq xeag rvcx uwns"
                }
            });

            const mailOptions = {
                from: "himanshu1972002@gmail.com",
                to: Email,
                subject: "OTP Verification",
                text: `Your Resend OTP is: ${otp}`
            };
            console.log(mailOptions)

            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error("Error sending email:", error);
                    return res.status(500).json({ error: "Failed to send OTP email" });
                }
                console.log("Email sent: " + info.response);
                return res.status(201).json({ message: " OTP resent to email." });
            });
        } else {
            res.json("Input id is not correct")
        }
    } catch {
        res.status(400).json({
            status: false,
            message: "Not successfully forgotp",
            data: []
        })
    }
}
exports.verifyotp = async (req, res) => {
    try {
        const { User_id, Otp } = req.body;
        // console.log("Verify data come",req.body)
        const change = Number(Otp);
        const userdata = await otpvalue.findOne({ User_id: User_id })
        if (!userdata) {
            return res.json({error:"ID not matched"})
        }
        if (userdata.Otp !== change) {
            return res.json({error:"otp not matched "})
        }
        const dletes = await otpvalue.deleteMany({ User_id: User_id })
        return res.status(200).json({
            status: true,
            message: "OTP verified and deleted successfully",
            data: userdata.User_id
        });


    } catch (err) {
        console.error("Unexpected error:", err);
        res.status(500).json({
            status: false,
            message: "Internal server error",
            error: err.message
        });
    }
}
exports.changepass = async (req, res) => {
    const { User_id, Password, Confirm_password } = req.body;
    console.log("Reet body ",req.body)
    // Check if passwords match
    if (Password !== Confirm_password) {
        return res.status(400).json({
            success: false,
            message: "Passwords do not match",
        });
    }

    try {
        // Update only the Password field
        const updatedUser = await user.findByIdAndUpdate(
            User_id,
            { Password },
            { new: true }
        );

        if (!updatedUser) {
            return res.status(404).json({
                success: false,
                message: "User not found",
            });
        }

        return res.status(200).json({
            status: true,
            message: "Password updated successfully",
        });
    } catch (error) {
        console.error(error);
        return res.status(500).json({
            success: false,
            message: "Server error",
            error: error.message,
        });
    }
};






// ////exports.Register = async (req, res) => {
//     try {
//         const { Name, Email, Password, Confirm_password } = req.body;
//         // let rules={
//         //     Name:'required',
//         //     Email:'required|email',
//         //     Password:'required',
//         //     Confirm_password:'required'
//         // }
//         // const v=await helpers.validators(rules,req.body)
//         // if (!v.status) {
//         //     // data.errors = v.errors;
//         //     return res.status(200).json({ status: "val_error", message: "Validation Error", errors: v.errors });
//         // }

//         if (!Name || !Email || !Password || !Confirm_password) {
//             return res.status(400).json({ error: 'All fields are required' });
//         }

//         if (Password !== Confirm_password) {
//             return res.status(400).json({ error: 'Passwords do not match' });
//         }
//         const userPayload = {
//             Name,
//             Email,
//             Password,
//             Confirm_password
//         };
//         const presence = await user.findOne({ Email: Email })
//         if (!presence) {
//             const userData = await user.create(userPayload);
//             const otpSecret = speakeasy.generateSecret({ length: 20 });
//             const otp = speakeasy.totp({
//                 secret: otpSecret.base32,
//                 encoding: 'base32'
//             });

//             const otpPayload = {
//                 User_id: userData._id,
//                 Otp: otp
//             };
//             const otpData = await otpvalue.create(otpPayload);
//             const server = http.createServer((request, response) => {
//                 const auth = nodemailer.createTransport({
//                     service: "gmail",
//                     secure: true,
//                     port: 465,
//                     auth: {
//                         user: "himanshu1972002@gmail.com",
//                         pass: "uwhq xeag rvcx uwns"

//                     }
//                 });

//                 const receiver = {
//                     from: "himanshu1972002@gmail.com",
//                     to: "morningstarakd@gmail.com",
//                     subject: "Node Js Mail Testing!",
//                     text: otpData
//                 };

//                 auth.sendMail(receiver, (error, emailResponse) => {
//                     if (error)
//                         throw error;
//                     console.log("success!");
//                     response.end();
//                 });

//             });
//         } else {
//             res.json("Email is already taken")
//         }
//     } catch {
//         // console.log("error",error);

//         res.status(400).json({
//             status: false,
//             message: "Not successfully",
//             data: []
//         })
//     }
// }///