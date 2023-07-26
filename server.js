
const user = mongoose.Schema({
    userName: {type: String},
    password: {type: String},
    email: {type: String, unique: true},
    mobileNo: {type: Number, unique: true},
    createdDate: {type: Date, default: Date.now()}
});

const Users = mongoose.model("Users", user);

app.post("/regester", (req, res)=>{
  const newUser = new Users(req.body);
  newUser.save().then(()=>{
    jwt.sign(newUser, secretkey, {expiresIn:'3600s'}, (err, token)=>{
      res.json({
        messsage: "User has been create sucessfully",
        token
      }).status(200);
    });
  }).catch((error)=>{
    console.log('error occur', error);
  })
});

app.get("/login", (req, res)=>{
  const user = req.body
  const secretkey = "secretkey"
  jwt.sign({user}, secretkey, {expiresIn: '300s'}, (err, token)=>{
    res.json({token})
  });
});

app.post("/profile", verifyToken, (req, res)=>{
  const secretkey = "secretkey";
  jwt.verify(req.token, secretkey, (err, authData)=>{
    if (err){
      res.send("error occoured");
    }else{
      res.json({
        messsage: "login sucessfull",
        authData
      });
    }
  })
});

function verifyToken(req, res, next){
  const bearerToken = req.headers.auth;
  if (typeof(bearerToken) !== "undefined"){
    const bearer = bearerToken.split(" ")
    const token = bearer[1];
    req.token = token;
    next();
  }
  else{
    res.send({
      result: "Invalid token"
    })
  }
}

const upload = multer({
  storage: multer.diskStorage({
    destination: function (req, file, callBack){
      callBack(null, "upload")
    },
    filename: function (req, file, callBack){
      callBack(null, file.fieldname+"_"+Date.now()+".pdf")
    }
  })
}).single("user_file");

app.post("/upload", upload, (req, res)=>{
  res.send('file uploaded sucessfully').status(200)
});
