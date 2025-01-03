from flask import Flask,render_template
from flask_socketio import SocketIO,send


app=Flask(__name__)
socketio=SocketIO(app,cors_allowed_origins="*")


@socketio.on("message")
def sendMessage(message):
    send(message, broadcast=True)  # Send message to all connected clients


@app.route("/")
def index():
    return render_template('index.html')


app.run(debug=True)