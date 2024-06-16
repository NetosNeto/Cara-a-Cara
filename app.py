from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Lista de 40 personagens com URLs de imagens
characters = [
    {"name": "Alex", "features": ["male", "hat", "glasses", "blond"], "image": "https://example.com/alex.jpg"},
    {"name": "Alfred", "features": ["male", "no_hat", "no_glasses", "red_hair"], "image": "https://example.com/alfred.jpg"},
    {"name": "Anita", "features": ["female", "no_hat", "glasses", "white_hair"], "image": "https://example.com/anita.jpg"},
    {"name": "Barbara", "features": ["female", "hat", "no_glasses", "black_hair"], "image": "https://example.com/barbara.jpg"},
    {"name": "Charles", "features": ["male", "no_hat", "glasses", "brown_hair"], "image": "https://example.com/charles.jpg"},
    {"name": "David", "features": ["male", "no_hat", "no_glasses", "blond"], "image": "https://example.com/david.jpg"},
    {"name": "Eric", "features": ["male", "hat", "no_glasses", "brown_hair"], "image": "https://example.com/eric.jpg"},
    {"name": "Frances", "features": ["female", "no_hat", "glasses", "red_hair"], "image": "https://example.com/frances.jpg"},
    {"name": "George", "features": ["male", "no_hat", "glasses", "black_hair"], "image": "https://example.com/george.jpg"},
    {"name": "Hannah", "features": ["female", "hat", "no_glasses", "white_hair"], "image": "https://example.com/hannah.jpg"},
    {"name": "Ivy", "features": ["female", "no_hat", "no_glasses", "blond"], "image": "https://example.com/ivy.jpg"},
    {"name": "Jack", "features": ["male", "hat", "no_glasses", "black_hair"], "image": "https://example.com/jack.jpg"},
    {"name": "Karen", "features": ["female", "no_hat", "glasses", "brown_hair"], "image": "https://example.com/karen.jpg"},
    {"name": "Louis", "features": ["male", "no_hat", "no_glasses", "red_hair"], "image": "https://example.com/louis.jpg"},
    {"name": "Maria", "features": ["female", "hat", "glasses", "black_hair"], "image": "https://example.com/maria.jpg"},
    {"name": "Nancy", "features": ["female", "no_hat", "no_glasses", "white_hair"], "image": "https://example.com/nancy.jpg"},
    {"name": "Oscar", "features": ["male", "hat", "glasses", "blond"], "image": "https://example.com/oscar.jpg"},
    {"name": "Paul", "features": ["male", "no_hat", "no_glasses", "brown_hair"], "image": "https://example.com/paul.jpg"},
    {"name": "Quincy", "features": ["male", "hat", "no_glasses", "black_hair"], "image": "https://example.com/quincy.jpg"},
    {"name": "Rachel", "features": ["female", "no_hat", "glasses", "red_hair"], "image": "https://example.com/rachel.jpg"},
    {"name": "Sarah", "features": ["female", "hat", "no_glasses", "blond"], "image": "https://example.com/sarah.jpg"},
    {"name": "Tom", "features": ["male", "no_hat", "glasses", "white_hair"], "image": "https://example.com/tom.jpg"},
    {"name": "Uma", "features": ["female", "no_hat", "no_glasses", "brown_hair"], "image": "https://example.com/uma.jpg"},
    {"name": "Victor", "features": ["male", "hat", "no_glasses", "blond"], "image": "https://example.com/victor.jpg"},
    {"name": "Wendy", "features": ["female", "no_hat", "glasses", "black_hair"], "image": "https://example.com/wendy.jpg"},
    {"name": "Xander", "features": ["male", "no_hat", "no_glasses", "red_hair"], "image": "https://example.com/xander.jpg"},
    {"name": "Yara", "features": ["female", "hat", "glasses", "blond"], "image": "https://example.com/yara.jpg"},
    {"name": "Zane", "features": ["male", "no_hat", "no_glasses", "black_hair"], "image": "https://example.com/zane.jpg"},
    {"name": "Aiden", "features": ["male", "hat", "glasses", "brown_hair"], "image": "https://example.com/aiden.jpg"},
    {"name": "Bella", "features": ["female", "no_hat", "no_glasses", "blond"], "image": "https://example.com/bella.jpg"},
    {"name": "Catherine", "features": ["female", "hat", "glasses", "red_hair"], "image": "https://example.com/catherine.jpg"},
    {"name": "Derek", "features": ["male", "no_hat", "no_glasses", "white_hair"], "image": "https://example.com/derek.jpg"},
    {"name": "Ella", "features": ["female", "no_hat", "glasses", "brown_hair"], "image": "https://example.com/ella.jpg"},
    {"name": "Finn", "features": ["male", "hat", "no_glasses", "blond"], "image": "https://example.com/finn.jpg"},
    {"name": "Grace", "features": ["female", "no_hat", "no_glasses", "black_hair"], "image": "https://example.com/grace.jpg"},
    {"name": "Henry", "features": ["male", "hat", "glasses", "red_hair"], "image": "https://example.com/henry.jpg"},
    {"name": "Isabella", "features": ["female", "no_hat", "no_glasses", "blond"], "image": "https://example.com/isabella.jpg"},
    {"name": "James", "features": ["male", "no_hat", "glasses", "brown_hair"], "image": "https://example.com/james.jpg"},
    {"name": "Katherine", "features": ["female", "hat", "no_glasses", "black_hair"], "image": "https://example.com/katherine.jpg"}
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
