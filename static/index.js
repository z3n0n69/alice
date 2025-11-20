let form = document.getElementById("loginForm"); 
form.addEventListener('submit', function(event){
    event.preventDefault();
    let username = document.forms["loginForm"]["usernameinput"].value; 
    let password = document.forms["loginForm"]["passwordinput"].value; 
    if(username == "" || password == ""){
        window.alert("Enter something bitch")
    }
    else {

    } 
});
s