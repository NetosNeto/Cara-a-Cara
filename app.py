from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Lista de 40 personagens com URLs de imagens
characters = [
    {"name": "Alex", "features": ["male", "hat", "glasses", "blond"], "image": "static\img\Alex.jpg"},
    {"name": "Alfred", "features": ["male", "no_hat", "no_glasses", "red_hair"], "image": "static/img/Alfred.jpg"},
    {"name": "Anita", "features": ["female", "no_hat", "glasses", "white_hair"], "image": "static/img/Anita.jpg"},
    {"name": "Barbara", "features": ["female", "hat", "no_glasses", "black_hair"], "image": "static/img/Barbara.jpg"},
    {"name": "Charles", "features": ["male", "no_hat", "glasses", "brown_hair"], "image": "static/img/Charles.jpg"},
    {"name": "David", "features": ["male", "no_hat", "no_glasses", "blond"], "image": "static/img/David.jpg"},
    {"name": "Eric", "features": ["male", "hat", "no_glasses", "brown_hair"], "image": "static/img/Eric.jpg"},
    {"name": "Frances", "features": ["female", "no_hat", "glasses", "red_hair"], "image": "static/img/Frances.jpg"},
    {"name": "George", "features": ["male", "no_hat", "glasses", "black_hair"], "image": "static/img/George.jpg"},
    {"name": "Hannah", "features": ["female", "hat", "no_glasses", "white_hair"], "image": "static/img/Hannah.jpg"},
    {"name": "Ivy", "features": ["female", "no_hat", "no_glasses", "blond"], "image": "static/img/Ivy.JPG"},
    {"name": "Jack", "features": ["male", "hat", "no_glasses", "black_hair"], "image": "static/img/Jack.JPG"},
    {"name": "Karen", "features": ["female", "no_hat", "glasses", "brown_hair"], "image": "static/img/Karen.JPG"},
    {"name": "Louis", "features": ["male", "no_hat", "no_glasses", "red_hair"], "image": "static/img/Louis.jpg"},
    {"name": "Maria", "features": ["female", "hat", "glasses", "black_hair"], "image": "static/img/Maria.jpg"},
    {"name": "Nancy", "features": ["female", "no_hat", "no_glasses", "white_hair"], "image": "static/img/Nancy.jpg"},
    {"name": "Oscar", "features": ["male", "hat", "glasses", "blond"], "image": "static/img/Oscar.jpg"},
    {"name": "Paul", "features": ["male", "no_hat", "no_glasses", "brown_hair"], "image": "static/img/Paul.jpg"},
    {"name": "Quincy", "features": ["male", "hat", "no_glasses", "black_hair"], "image": "static/img/Quincy.jpg"},
    {"name": "Rachel", "features": ["female", "no_hat", "glasses", "red_hair"], "image": "static/img/Rachel.jpg"},
    {"name": "Sarah", "features": ["female", "hat", "no_glasses", "blond"], "image": "static/img/Sarah.jpg"}
]

rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST'])
def game():
    player_name = request.form.get('player_name')
    room = request.form.get('room')

    session['player_name'] = player_name
    session['room'] = room

    if room not in rooms:
        rooms[room] = {'players': [player_name], 'state': 'waiting', 'selected_characters': {}}
    else:
        rooms[room]['players'].append(player_name)

    return render_template('game.html', player_name=player_name, room=room, characters=characters)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f"{session['player_name']} entrou na sala."}, room=room)

@socketio.on('select_character')
def select_character(data):
    room = session.get('room')
    character = data['character']
    if room in rooms:
        rooms[room]['selected_characters'][session['player_name']] = character
        emit('character_selected', {'player': session['player_name'], 'character': character}, room=room)
        if len(rooms[room]['selected_characters']) == 2:
            rooms[room]['state'] = 'playing'

@socketio.on('ask_question')
def ask_question(data):
    room = session.get('room')
    question = data['question']
    emit('question_asked', {'player': session['player_name'], 'question': question}, room=room)

@socketio.on('eliminate_character')
def eliminate_character(data):
    room = session.get('room')
    character = data['character']
    emit('character_eliminated', {'player': session['player_name'], 'character': character}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
