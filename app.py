from flask import Flask, redirect, render_template, request, jsonify
from flask_socketio import SocketIO, send
app = Flask('__name__')
socketio = SocketIO(app)
import mysql.connector

#DATABASE CONNECTION 

def dbconnection(): 
    try: 
        mydb = mysql.connector.connect(
            host = "localhost", 
            user = "root", 
            password = "root", 
            database = "alice"
        )
        return mydb
    except mysql.connector.Error as err: 
        print(err)
        return None 


class databaseRequest: 
    def __init__(self, username): 
        self.username = username 
    
    def fetch_userexist(self, userpassword): 
        dbconn = dbconnection() 
        dbcursor = dbconn.cursor() 
        dbcursor.execute(f"SELECT * FROM users WHERE username = %s AND password = %s" , (self.username, userpassword ))
        result = dbcursor.fetchall() 

        print(result)
        if result:
            return True
        else:
            return False
    
    def register(self, password):
        dbconn = dbconnection() 
        dbcursor = dbconn.cursor() 
        #fetch the maximum value of userID in users 
        dbcursor.execute(f"SELECT MAX(userID) FROM users")
        userid = dbcursor.fetchall()
        print(userid[0])

        #dbcursor.execute(f"INSERT INTO users (userID, username, userpassword) VALUES (%s, %s, %s)", (userID, self.username, userpassword)) 
    

#===================
# ROUTES
#===================


@app.route('/')
def index():
    return render_template('index.html')


#dashboard not built yet 
@app.route('/dashboard')    
def dashboard():
    return render_template('dashboard.html')

#register page not built yet 
@app.route('/register') 
def register(): 
    return render_template('register.html')


#===================
# POST REQUEST VIA SOCKET
#===================

#login validation
@socketio.on("login")

def loginValidation(info): 
    usernameInput = info.get("username")
    passwordInput = info.get("password") 
    #check if user is in the database: 
    auth = databaseRequest(usernameInput)
    result = auth.fetch_userexist() 
    print(result)
    send(f"{result}" , broadcast = True)


#Client wants to register
@socketio.on("register")

def registerUser(info):
    usernameInput = info.get("username")
    passwordInput = info.get("password")
    #check if user is already in the database
    auth = databaseRequest(usernameInput)
    result = auth.fetch_userexist() 
    send(f"{result}", broadcast = True)
    

if __name__ == '__main__':
    socketio.run(app, debug = True , host="0.0.0.0")