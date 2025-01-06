from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,send, join_room, leave_room, emit
import random
from string import ascii_uppercase


app=Flask(__name__)
app.config['SECRET_KEY']="abc"
socketio=SocketIO(app,cors_allowed_origins="*")
codes=[]
members=0

@socketio.on("connect")
def connect():
    print("connected")
    return "Connected"

@socketio.on("message1")
def sendMessages(message):
    print(message)
    d={"Message":message,"Name":session['uname']}
    emit("message1",d,room=session.get('code'))
    
@app.route("/")
def index():
    code = session.get('code', None)
    return render_template('room.html', code=code)

@app.route("/createRoom")
def createRoom():
    session.clear()
    code = ''
    for i in range(0,4):
        code += random.choice(ascii_uppercase)
    codes.append(code)  
    session['code'] = code  
    return redirect(url_for('index'))

@socketio.on("leave")
def leaveRoom():
    username = session.get('uname')  # Get the username from session
    code = session.get('code')  # Get the room code from session
    
    if username and code:
        leave_room(code)  # Leave the room
        session.clear()  # Clear the session data     
        # Emit message to all users in the room
        emit('room_message', f"{username} has left the room", room=code)
    else:
        print("Session data missing: username or room code.")

@socketio.on("join")
def handle_join(data):
    uname = data['username']
    code = data['code']
    if code == session.get('code') or members>0:
        join_room(code)
        session['code']=code
        session['uname']=uname
        emit('message', {'msg': uname + ' has entered the room.'}, room=code)
    else:
        emit('message', {'msg':'Please enter valid code'})
def update_room(code):
    for room in room_details:
        if room['code'] == code:  # Check if the room code matches
            room['members'] += 1  # Increase the members count by 1
            break
    else:
        room_details.append({'code': code, 'members': 1})
    
app.run(debug=True)
