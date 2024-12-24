from flask import Flask, render_template, request, redirect, flash, url_for, session
from blackjack import Blackjack
from data import create_tables, get_db_connection, get_user_stats, update_user_score
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
create_tables()

game = Blackjack()

@app.route("/")
def home_route():
    return render_template("index.html")
def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM SignUp WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user:
            if user["password"] == password:
                session['username'] = username
                return redirect(url_for("play"))
            else:
                flash("Incorrect password. Please try again.", "error")
        else:
            flash("Username does not exist. Please sign up.", "error")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM SignUp WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("User already exists with that username.", "error")
            return redirect("/signup")
        
        cursor.execute("INSERT INTO SignUp (username, password) VALUES (?, ?)", (username, password))
        cursor.execute("INSERT INTO Score (username, total_matches, total_wins, win_rate) VALUES (?, ?, ?, ?)", (username, 0, 0, 0))
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("signup.html")

@app.route("/play")
@login_required
def play():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    game.start_new_round()
    return render_template("home.html", game_state=game.get_game_state())

@app.route("/hit")
@login_required
def hit_card():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    game.hit_card()
    return render_template("home.html", game_state=game.get_game_state())

@app.route("/stand")
@login_required
def stand():
    result = game.stand_player()
    username = session['username']  
    if result == "win":
        update_user_score(username, user_won=True)
    else:
        update_user_score(username, user_won=False)  

    return render_template("home.html", game_state=game.get_game_state())

@app.route("/new_game")
@login_required
def new_game():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    game.start_new_round()  
    return render_template("home.html", game_state=game.get_game_state())


@app.route("/rules")
@login_required
def rules():
    return render_template("rules.html")

@app.route("/score")
@login_required
def score():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_stats = get_user_stats(username)

    if user_stats:
        return render_template('score.html', stats=user_stats)
    else:
        return "No stats available for this user.", 404

@app.route("/leaderboard")
@login_required
def leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, total_wins, win_rate FROM Score ORDER BY win_rate DESC")
    leaderboard_data = cursor.fetchall()
    conn.close()
    
    return render_template("leaderboard.html", leaderboard=leaderboard_data)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect("/")  

if __name__ == "__main__":
    app.run(port=7000, debug=True)
