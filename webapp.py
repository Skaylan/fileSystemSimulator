from flask import Flask, render_template, request
from flask_socketio import SocketIO
from .main import FileSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
file_system = FileSystem()

commands = ['cd', 'ls', 'mkdir', 'touch', 'rm', 'tree']


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('terminal_command')
def handle_terminal_command(data):
    command = data['command']
    if command in commands:
        if command == 'cd':
            file_system.cd(data['parameter'])
        elif command == 'ls':
            file_system.ls()
        elif command == 'mkdir':
            file_system.mkdir(data['parameter'])
        elif command == 'touch':
            file_system.touch(data['parameter'])
        elif command == 'rm':
            file_system.rm(data['parameter'])
        elif command == 'tree':
            file_system.tree()
    socketio.emit('terminal_output', {'output': output})


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)