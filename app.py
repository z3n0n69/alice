from flask import Flask, redirect, render_template, request, jsonify, make_response 
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
    
    def fetch_userexist(self):  #checks if username does exist 
        #connect to database 
        dbconn = dbconnection() 
        dbcursor = dbconn.cursor() 
        
        #check if username exist in the database 
        dbcursor.execute(f"SELECT * FROM users WHERE username = %s" , (self.username, ))
        result = dbcursor.fetchall() 

        if result:
            return True
        else:
            return False
    
    def authenticator(self, password): 
        dbconn = dbconnection() 
        dbcursor = dbconn.cursor() 
        dbcursor.execute(f"SELECT * FROM users WHERE username = %s AND userpassword = %s", (self.username, password))
        result = dbcursor.fetchall() 
        if result: 
            result_username = result[0][1]
            result_userpassword = result[0][2]
            if result_username == self.username and result_userpassword == password: 
                return True

        else:
            return False 

    def register(self, password):
        dbconn = dbconnection() 
        dbcursor = dbconn.cursor() 
        #fetch the maximum value of userID in users 
        dbcursor.execute(f"SELECT MAX(userID) FROM users")
        userid = dbcursor.fetchall()
        print(userid[0][0])
        userid = userid[0][0]

        if userid == None:
            userid = 0 
            dbcursor.execute(f"INSERT INTO users (userID, username, userpassword) VALUES (%s, %s, %s)", (userid, self.username, password))
            dbconn.commit() 
        else:
            userid += userid 
            dbcursor.execute(f"INSERT INTO users (userID , username, userpassword) VALUES (%s,%s,%s)", (userid, self.username, password))
            dbconn.commit() 

        
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

#register route
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
    print(f"\nFetched = username: {usernameInput} & password: {passwordInput}\n")
    #check if user is in the database: 
    auth = databaseRequest(usernameInput)
    result =  auth.authenticator(passwordInput)
    print(f"\n[SERVER]: respond = {result} - {type(result)}")
    send(result)



#Client wants to register 
@socketio.on("register")

def registerUser(info):
    usernameInput = str(info.get("username"))
    passwordInput = str(info.get("password"))
    #check if user is already in the database
    auth = databaseRequest(usernameInput)
    result = auth.fetch_userexist()

    if result == True:
        print("[USER EXIST]")
        send(f"userexist")
    else:
        dbupdate = databaseRequest(usernameInput)
        dbupdate.register(passwordInput)
        send("registered")
    
    

if __name__ == '__main__':
    socketio.run(app, debug = True , host="0.0.0.0")