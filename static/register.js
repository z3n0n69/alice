let form = document.getElementById("registerForm");

form.addEventListener('submit', function(event){
    let username = document.forms["registerForm"]["usernameinput"].value;
    let password = document.forms["registerForm"]["passwordinput"].value; 
    

    //check if the form have value
    if (username == "" || password == ""){
        window.alert("Nigga are you dumb?"); 
    } 
    else {
        
        let registerUser = {
            username:username,
            password:password
        }; 

        const socket = io("http://localhost:5000"); //connect to the server
        
        //send the information to attempt to register the user
        socket.on("connect", () => {
            socket.emit("login", registerUser); 
        });

        socket.on()
    }
});