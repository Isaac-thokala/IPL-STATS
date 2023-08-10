from flask import Flask, render_template, request,redirect




#from flask_mysqldb import MySQL
import mariadb
from datetime import datetime

from flask_bcrypt import Bcrypt






app = Flask(__name__)




users = {'user1':{'pw':'pass1'},
         'user2':{'pw':'pass2'},
         'user3':{'pw':'pass3'}}





bcrypt = Bcrypt(app)




class User :
    def __init__(self, name, pswd, authenticated):
        self.name = name
        self.pswd = pswd
        self.authentictaed = False



connection = mariadb.connect(
         host='127.0.0.1',
         port= 3306,
         user='root',
         password='we5great',
         database='sys')
cur = connection.cursor()






@app.route('/')
def index():

    cur.execute('SELECT * FROM Team ORDER BY pos');
    print(cur)
    teams = cur.fetchall()
    connection.commit()
    for team in teams:
        print(team)
    return render_template("home.html", teams=teams, i = 0);

@app.route('/team/t_id=<int:t_id>')
def team(t_id):
    cur.execute(f'SELECT * FROM Player WHERE Player.team_id={t_id} ORDER BY runs DESC ')
    players = cur.fetchall();

    return render_template("player.html", players=players);



@app.route('/matches')
def matches():
    cur.execute('SELECT * FROM Match_ ORDER BY time DESC')
    matches = cur.fetchall()
    connection.commit()
    print(matches[0])
    return render_template("matches.html", matches=matches, abs=abs);

@app.route('/match/mid=<int:m_id>')
def match(m_id):
    cur.execute(f'SELECT * FROM Match_ WHERE match_id={m_id}')
    match = cur.fetchall();
    print(match[0][3])
    cur.execute(f'SELECT batsman,batting_team, SUM(batsman_runs) AS runs,COUNT(delivery_id) AS balls FROM Delivery WHERE extra_runs=0 AND match_id={m_id} GROUP BY batsman ORDER BY runs DESC;')
    players = cur.fetchall()
    cur.execute(f'SELECT bowler,bowling_team,SUM(is_wicket) AS wickets,SUM(total_runs) AS runs, COUNT(delivery_id) AS balls FROM Delivery WHERE match_id={m_id} GROUP BY bowler ORDER BY runs DESC; ')
    bowlers=cur.fetchall()
    print(match)
    print(len(match))
    return render_template("match.html", match=match[0], abs=abs, players=players, bowlers=bowlers, int=int);

@app.route('/players')
def players():
    cur.execute('SELECT * FROM Player ORDER BY player_name')
    players = cur.fetchall()
    print(players[0])
    return render_template("players.html", players=players);

@app.route('/player/pid=<int:pid>')
def player(pid):
    cur.execute(f'SELECT * FROM Player WHERE player_id={pid}')
    player = cur.fetchall()[0]
    print(player)
    return render_template("stat.html", player=player,int=int);


@app.route('/deliveries/mid=<int:m_id>')
def deliveries(m_id):
    cur.execute(f'SELECT * FROM Delivery WHERE match_id={m_id}')
    deliveries = cur.fetchall()
    for delivery in deliveries :
        print(delivery)
    return render_template("delivery.html", deliveries=deliveries, int=int);


user = User('xxxxx', 'xxxx',False)

@app.route('/login',methods =["GET", "POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    if(request.method != "POST") :
        return render_template("login.html", mesg="")
    form = request.form
    print(request.values)
    pw_hash = bcrypt.generate_password_hash('hello')
    global user
    print(user.name, user.pswd, user.authentictaed, pw_hash)
    user_name = form.get("username")
    user.name = user_name
    user.pwsd = bcrypt.generate_password_hash('hello')
    print(user.name, user.pswd, user.authentictaed, pw_hash)
    if user_name == 'ebenezer':
        print(bcrypt.check_password_hash(pw_hash, form.get("password")))
        if bcrypt.check_password_hash(pw_hash, form.get("password")):
            user.authentictaed = True
            print(user.name, user.pswd, user.authentictaed, pw_hash)
            return redirect("/admin")
        else :
            return render_template("login.html", mesg="password is wrong")
    else :
        return render_template("login.html", mesg="username is wrong")



@app.route('/admin')
def admin():
    global user
    print(user.authentictaed, user.name, user.pswd)
    if(not(user.authentictaed)) :
        return redirect("/login")
    return render_template("admin.html")


@app.route('/mvp')
def mvp():
    return render_template("login.html")


if __name__ == ' __main__':
    app.run(debug=True, port=80)
