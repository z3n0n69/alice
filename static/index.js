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
        let loginInformation = {
            username:username,
            password:password
        }

        const socket = io("http://localhost:5000"); 
        socket.on("connect", () => {

            socket.emit("login", loginInformation);
            
        }); 
        socket.on("message", (msg) => {
            console.log("Communication from server: ", msg)
        });
    } 
});



