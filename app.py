from flask import Flask, redirect, render_template, request, jsonify
from flask_socketio import SocketIO, send
app = Flask('__name__')
socketio = SocketIO(app)



#===================
# GET REQUEST
#===================


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/dashboard')    
def dashboard():
    return render_template('dashboard.html')





#===================
# POST REQUEST
#===================

#This will validate the login
@socketio.on("login")

def loginValidation(info): 
    print("received something from the server")
    print(f"Recevied: {type(info)}")
    usernameInput = info.get("username")
    passwordInput = info.get("password") 
    #authenticate in the database
    print(f"Data: \nUsername = {usernameInput}\nPassword = {passwordInput}")
    send(f"authenticated" , broadcast = True); 

    

if __name__ == '__main__':
    socketio.run(app, debug = True , host="0.0.0.0")