import express from "express";
import mongoose from "mongoose";
import Jwt from "jsonwebtoken";
// import multer from "multer";
import send_email from "./utils.js";
import "dotenv/config";

const app = express();

const port = process.env.PORT;
const url = process.env.DB_URL;
const secret_key = process.env.SECRET_KEY

app.use(express.json());
app.use(express.urlencoded({extended: true}));

mongoose.connect(url).then(() =>{
    console.log('Database connected sucesssfully');
}).catch(()=>{
    console.log('Unable to connect database');
});

// schemas and models
const Subscribe = mongoose.model("Subscribe", new mongoose.Schema({
  email: {type: String, default: null, unique: true}
}));
const Users = mongoose.model("Users", new mongoose.Schema({
  password: {type: String, default: null},
  email: {type: String, default: null, unique: true},
  mobile: {type: Number, default: null, unique: true},
  createdDate: { type: Date, default: Date.now()}
}));
const Blog = mongoose.model("blog", new mongoose.Schema({
  title: {type: String, default: null},
  description: {type: String, default: null},
  upload_file_path: {type: String, default: null},
  attached_file_path: {type: String, default: null},
  category: {type: String, default: null},
  published: {type: Boolean, default: false},
  user_id: {type: String, default: null}
}));
const Contact = mongoose.model("contact", new mongoose.Schema({
  userName: {type: String, default: null},
  email: {type: String, default: null},
  mobile: {type: String, default: null},
  subject: {type: String, default:null},
  message: {type: String, default: null}  
}));
const Commnet = mongoose.model("Comment", new mongoose.Schema({
  blog_id: {type: String, required: true},
  user_id: {type: String, required: true},
  message: {type: String, default: null},
  createdDate: {type: Date, default: Date.now()}
}));
const Reply = mongoose.model("Reply", new mongoose.Schema({
  blog_id: {type: String, required: true},
  user_id: {type: String, required: true},
  comment_id: {type: String, required: true},
  message: {type: String, default: null},
  createdDate: {type: Date, default: Date.now()}
}));
const Review = mongoose.model("Review", new mongoose.Schema({
  user_id: {type: String, required: true},
  blog_id: {type: String, required: true},
  likes: {type: Number, default: null},
  dislikes: {type: Number, default: null},
  ratings: {type: Number, default: null},
  createdDate: {type: Date, default: Date.now()}
}));
const CommentReview = mongoose.model("CommentReview", new mongoose.Schema({
  user_id: {type: String, required: true},
  blog_id: {type: String, required: true},
  comment_id: {type: String, required: true},
  likes: {type: Number, default: null},
  dislikes: {type: Number, default: null},
  ratings: {type: Number, default: null},
  createdDate: {type: Date, default: Date.now()}
}));
const ReplyReview = mongoose.model("ReplyReview", new mongoose.Schema({
  user_id: {type: String, required: true},
  blog_id: {type: String, required: true},
  comment_id: {type: String, required: true},
  reply_id: {type: String, required: true},
  likes: {type: Number, default: null},
  dislikes: {type: Number, default: null},
  ratings: {type: Number, default: null},
  createdDate: {type: Date, default: Date.now()}
}));
const Notification = mongoose.model("Notification", new mongoose.Schema({
}));


// auth api's
app.post('/regestration', (req, res)=>{

  // const email = req.body.email;
  // const mobile = req.body.mobile;

  // const checkUser = Users.find({email: email, mobile: mobile});
  // if (checkUser){
  //     res.send(`User is already exist with this ${email}`).status(400);
  // }

  const user = new Users(req.body);
  user.save().then(()=>{
      const token = Jwt.sign(user, secret_key)
      res.json({
          message: 'User has been created sucessfully',
          token
      }).status(200);
  }).catch((error)=>{
      console.log("error occoured", error);
  });
});
app.post("/login", (req, res)=>{
  const password = req.body.password;
  if (isInteger(req.body.userName)){
      const mobile = req.body.userName;
      const user = Users.findOne({password: password, mobile: mobile});
      if(user){
          const token = Jwt.sign(user, secret_key);
          res.json({
              message: "Loged in sucessfully",
              token
          }).status(200);
      }else{
          res.send("user does not exist").status(400);
      }
  }else{
      const email = req.body.userName;
      const user = Users.findOne({password: password, email: email});
      if(user){
          const token = Jwt.sign(user, secret_key);
          res.json({
              message: "Loged in sucessfully",
              token
          }).status(200);
      }else{
          res.send("user does not exist").status(400);
      }
  }
});
app.post("/send_otp", (req, res)=>{
});
app.post("/verify_otp", (req, res)=>{
});
app.post("/forgot_pass", (req, res)=>{
});
app.put("/change_pass", (req, res)=>{
});

// admin auth api's
app.post("/admin_login", (req, res)=>{
});
app.put("/admin_change_pass", (req, res)=>{
});


// Blog api's
app.post("/create_blog", (req, res)=>{
  const blog = new Blog(req.body);
  blog.save().then(()=>{
      res.json({
          message: "Blog has been save sucessfully",
          blog
      }).status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.get("/get_blog/:id", async(req, res)=>{
  const ID = req.params.id;
  const blog = await Blog.findOne({_id:ID, user_id: req.body.user_id});
  if (blog){
      res.json(blog).status(200);
  }else{
      res.send("There is no blog avilable for given id").status(400);
  }
});
app.get("/get_blogs/:category", async(req, res)=>{
  const blogs = await Blog.find({category: req.params.category, user_id: req.body.user_id, published: true});
  if (blogs){
      res.json(blogs).status(200);
  }else{
      res.send("There is no blog avilable for this category").status(400);
  }
});
app.get("/get_all_blog", async(req, res)=>{
  const blogs = await Blog.find({user_id: req.body.user_id, published: true});
  if (blogs){
      res.json(blogs).status(200);
  }else{
      res.send("There is no blog avilable for the given user id");
  }
});
app.put("/update_blog/:id", async(req, res)=>{
  const blog = await Blog.findByIdAndUpdate(req.params.id, req.body);
  blog.save().then(()=>{
      res.send("Blog updated successfully").status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.delete("/delete_blog/:id", async(req, res)=>{
  await Blog.findByIdAndDelete(req.params.id).then(()=>{
      res.send("Blog has been deleted sucessfully").status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.delete("/delete_many", async(req, res)=>{
  await Blog.deleteMany({_id: {'$in':req.body.array}}).then(()=>{
      res.send("All blogs has been deleted").status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.post("/publish_blog/:id", async(req, res)=>{
  const ID = req.params.id;
  const publish_blog = await Blog.findOne({_id: ID});
  publish_blog.published = true;
  await Blog.findByIdAndUpdate(ID, publish_blog).then(()=>{
      res.send("Blog has been published sucessfully").status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.post("/publish_many", async(req, res)=>{
  const blog = await Blog.find({_id: {'$in': req.body.array}, published: false});
  blog.forEach((elem)=>{
    elem.published = true;
    Blog.findByIdAndUpdate(elem._id, elem).then(()=>{
      console.log("done");
    });
  });
  res.json({message:"All blogs has been published sucessfully", blog}).status(200);

});


// other api
app.post ("/upload_file", (req, res)=>{
});
app.post("/upload_multiple_file", (req, res)=>{
});
app.post("/upload_attached_file", (req, res)=>{
});
app.post("upload_multiple_attached_file", (req, res)=>{
});


app.post("/review", (req, res)=>{
  const review = new Review(req.body);
  review.save().then(()=>{
      res.json(review).status(200)
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.get("/review", async(req, res)=>{
  const review = await Review.find({
      user_id: req.body.user_id,
      blog_id: req.body.blog_id,
  });
  if (review){
      res.json(review).status(200);
  }else{
      res.send("No review found for given input").status(400);
  }
});

app.post("/comment_review", (req, res)=>{
});
app.get("/comment_review", (req, res)=>{
});
app.post("/reply_review", (req, res)=>{
});
app.get("/reply_review", (req, res)=>{
});

app.post("/comments", (req, res)=>{
  const comment = new Commnet(req.body)
  comment.save().then(()=>{
      res.json({
          message: "comment has been saved sucessfully",
          comment
      }).status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.get("/comments", async(req, res)=>{
  const comment = await Commnet.find({
      user_id: req.body.user_id, 
      blog_id: req.body.blog_id
  });
  console.log(comment);
  if (comment){
      res.json(comment).status(200);
  }else{
      res.send('There is no comment avilable of this blog for this user').status(400);
  }
});

app.post("/reply", (req, res)=>{
  const reply = new Reply(req.body);
  reply.save().then(()=>{
      res.json({
          message: "Reply saved sucessfully",
          reply
      }).status(200);
  }).catch((error)=>{
      res.send(error).status(400);
  });
});
app.get("/reply", async(req, res)=>{
  const reply = await Reply.find({
      user_id: req.body.user_id, 
      blog_id: req.body.blog_id, 
      comment_id: req.body.comment_id
  });
  if (reply){
      res.json(reply).status(200);
  }else{
      res.send("No reply found for given details").status(400);
  }
});

app.post("share", (req, res)=>{
});
app.post("/multiple_share", (req, res)=>{
});


// get total no. of blog, total no. of user, total category
app.get("/project_spec", async(req, res)=>{
  const totalBlogs = await Blog.find().count();
  const totalUser = await Users.find().count();
  const category = await Blog.find().select("category").distinct("category").count();
  res.send({"blogs":totalBlogs, "users": totalUser, "categories": category});
});
app.get("/notification", async(req, res)=>{
  const notification = await Notification.find({user_id: req.body.user_id})
  if (notification){
      res.json(notification).status(200);
  }else{
      res.send("There is no notification for this user").status(400);
  }
});
app.post("/subscribe", (req, res)=>{
  const subscribe = new Subscribe(req.body)
  subscribe.save().then(()=>{
      res.send("Subscription has been done sucessfully").status(200);
  }).catch((error)=>{
      res.send(error);
  });
});
app.post("/unsubscribe", async(req, res)=>{
  const subscribe = await Subscribe.findOneAndRemove({email: req.body.email});
  if (subscribe){
      res.send("You have sucessfully unsubscribe").status(200);
  }
  else{
      res.send("Unable to unsubscribe now. Please try again later").status(400);
  }
});
app.post("/contact", (req, res)=>{
  const contact = new Contact(req.body);
  contact.save().then(()=>{
      send_email(req.body.email, req.body.subject, req.body.message);
      res.send("Contact has been save and send sucessfully").status(200)  
  }).catch((error)=>{
      console.log(error)
      res.send(error);
  });
});


app.listen(port, ()=>{
    console.log(`Server is running on Localhost:${port}`);
});
