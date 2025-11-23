let form = document.getElementById("loginForm"); 
form.addEventListener('submit', function(event){
    event.preventDefault();
    //gets the value from the form then send it to the server 
    let username = document.forms["loginForm"]["usernameinput"].value; 
    let password = document.forms["loginForm"]["passwordinput"].value; 
    if(username == "" || password == ""){
        window.alert("Enter something bitch")
    }
    else {
        //using socketio to have real-time updates with the server


        let loginInformation = {    //This is the json that will be sent to flask 
            username:username,
            password:password
        }
        
        const socket = io("http://localhost:5000");  //sending to flask 
        socket.on("connect", () => {

            socket.emit("login", loginInformation);
            
        }); 
        //receiver of message from server 
        socket.on("message", (msg) => {
            if (msg == "True"){
                window.alert("Routing to Dashboard"); 
                window.location.href("/dashboard");
                
            }
            else{
                window.alert("User does not exist")
            };
        });
    } 
});



