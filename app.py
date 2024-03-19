from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # It's important for session management; replace with a strong secret key.

# Function to check if the current state of the board has a winner
def check_win(board):
    # Winning combinations can be three rows, three columns, or two diagonals
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] and board[condition[0]] == board[condition[1]] == board[condition[2]]:
            return True
    return False

@app.route('/')
def index():
    # Initialize the game board and turn if not already done
    if 'board' not in session:
        session['board'] = ['' for _ in range(9)]
        session['turn'] = 'X'
        session['winner'] = None  # Track the winner ('X', 'O', or None)
    return render_template('index.html', board=session['board'], turn=session['turn'], winner=session['winner'])

@app.route('/play/<int:index>', methods=['POST'])
def play(index):
    if 0 <= index < 9 and session['board'][index] == '' and not session.get('winner'):
        session['board'][index] = session['turn']  # Mark the cell with the current turn
        if check_win(session['board']):  # Check if this move wins the game
            session['winner'] = session['turn']  # Mark the winner
        else:
            # Switch turns if no winner yet
            session['turn'] = 'O' if session['turn'] == 'X' else 'X'
    return redirect(url_for('index'))

@app.route('/restart', methods=['POST'])
def restart():
    # Clear the game board, reset the turn, and clear the winner
    session.pop('board', None)
    session.pop('turn', None)
    session.pop('winner', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
