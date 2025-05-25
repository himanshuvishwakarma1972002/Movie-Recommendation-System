const express=require("express");
const app=express();
const {database}=require("./dbconnect/DBconnect")
const cors = require("cors");

app.use(cors());

port=3000
database();
app.use(express.json());
app.use("/", require("./usr/user"));

app.listen(port, () => {
    console.log('server started !');
})