import nodemailer from "nodemailer";

export default function send_email(email, subject, message){

    let mailTransport = nodemailer.createTransport({
        service: "gmail",
        auth:{
            user: "ajitpathak0448@gmail.com",
            pass: "fbleuyuafdeypohg"
        }
    });
    
    let mailDetails = {
        from: "ajitpathak0448@gmail.com",
        to: email,
        subject: subject,
        text: message
    }

    console.log(mailDetails);

    mailTransport.sendMail(mailDetails, function(err, data){
        if (err){
            console.log(`error occured ${err}`);
        } else {
            console.log("Email send sucessfully");
        }
    });
}