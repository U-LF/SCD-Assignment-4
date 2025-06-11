from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulated in-memory "database"
users = {}
games = {}
game_sessions = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')

    if not user_id or not name:
        return jsonify({'message': 'Missing user_id or name'}), 400

    if user_id in users:
        return jsonify({'message': 'User already exists'}), 400

    users[user_id] = {'name': name}
    print(f"[DB SIM] Registered user: {user_id} -> {name}")
    return jsonify({'message': f'Registration successful for {name}'}), 200

@app.route('/submit_board', methods=['POST'])
def submit_board():
    data = request.get_json()
    user_id = data.get('user_id')
    board = data.get('board')

    if user_id not in users:
        return jsonify({'message': 'User not registered'}), 400

    game_sessions[user_id] = {'board': board}
    print(f"[DB SIM] Board submitted by {user_id}: {board}")
    return jsonify({'message': 'Board submitted successfully'}), 200

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player1 = data.get('player1')
    player2 = data.get('player2')

    if player1 not in users or player2 not in users:
        return jsonify({'message': 'One or both users not registered'}), 400

    game_id = f"{player1}_vs_{player2}"
    games[game_id] = {
        'players': [player1, player2],
        'turn': player1,
        'moves': []
    }

    print(f"[DB SIM] Game started: {game_id}")
    return jsonify({'message': f'Game started between {player1} and {player2}'}), 200

@app.route('/mark_number', methods=['POST'])
def mark_number():
    data = request.get_json()
    game_id = data.get('game_id')
    user_id = data.get('user_id')
    number = data.get('number')

    game = games.get(game_id)
    if not game or user_id not in game['players']:
        return jsonify({'message': 'Invalid game or user'}), 400

    if game['turn'] != user_id:
        return jsonify({'message': 'Not your turn'}), 400

    game['moves'].append({'user': user_id, 'number': number})
    game['turn'] = game['players'][1] if game['turn'] == game['players'][0] else game['players'][0]
    print(f"[DB SIM] {user_id} marked {number} in {game_id}")
    return jsonify({'message': f'{user_id} marked number {number}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
