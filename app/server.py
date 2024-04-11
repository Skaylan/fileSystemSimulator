import json
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from file_system import FileSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    print(data)
    _data = {
        'message': "estou conectado"
    }
    socketio.emit('conectado', _data)
    
    
@socketio.on('terminalInput')
def handle_terminal_input(data):
    file_system = FileSystem()
    file_system.load_from_json(path_to_file='filesystem_data.json')
    print(data)
    if data == 'ls':
        result = file_system.ls()
        print(result)
    elif data == 'tree':
        result = file_system.tree()
        socketio.emit('terminalOutput', result)
        
    else:
        print("Comando inválido")


if __name__ == '__main__':
    socketio.run(app, debug=True)