import chap
import os
import datetime
from flask import Flask, request, render_template, session, redirect, g,url_for
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        usr = chap.query_db("select username,password from users")
        dic = {}

        for nm in usr:
            dic[nm[0]]=nm[1]

        if request.form['user'] in dic and dic[str(request.form['user'])] == request.form['password']:

        #if request.form['password'] == 'password':

            session['user'] = request.form['user']
            usr = request.form['user']
            return redirect(url_for('chores', user=usr))

    return render_template('login.html')


@app.route("/chores/<user>", methods=['GET', 'POST'])
def chores(user):

    if user == 'admin':
        chores = chap.query_db("select name, chore from chores where done = 'False'")
        names = chap.query_db("select fname from users")
        done_chores = chap.query_db("select name, chore from chores where done = 'True'")
        dic_login = {}
        dic_done = {}
        for nm in names:
            if nm[0] == 'admin':
                pass
            else:
                dic_login[nm[0]]=[]
        for nm in names:
            if nm[0] == 'admin':
                pass
            else:
                dic_done[nm[0]]=[]

        for nm in chores:
            if nm[0] == 'admin':
                pass
            else:
                dic_login[nm[0]]+=[nm[1]]

        for nm in done_chores:
            if nm[0] == 'admin':
                pass
            else:
                dic_done[nm[0]]+=[nm[1]]
        return render_template('chores.html', chrs=dic_login, dchrs=dic_done, user=user)

    else:
        fname = chap.query_db("select fname from users where username = '"+g.user+"'")
        nm = fname[0][0]
        chores = chap.query_db("select chore from chores where done = 'False' and name = '"+nm+"'")
        done_chores = chap.query_db("select chore from chores where done = 'True' and name = '"+nm+"'")
        dic_login = {}
        dic_done = {}
        dic_login[nm]=[]
        dic_done[nm]=[]
        for chr in chores:
            dic_login[nm]+=chr
        for chr in done_chores:
            dic_done[nm]+=chr

        return render_template('chores.html', chrs=dic_login, dchrs=dic_done, user=session['user'])

@app.route("/update", methods=['GET', 'POST'])
def update_chores():
    if request.method == 'POST':
        chores = (request.form.getlist('chr'))
        for c in chores:
            chap.chore_done(c)
        usr = session['user']
        return redirect(url_for('chores', user=usr))

    usr = session['user']
    return redirect(url_for('chores', user=usr))

@app.route("/incomplete", methods=['GET', 'POST'])
def incomplete_chores():
    if request.method == 'POST':
        chores = (request.form.getlist('chr'))
        for c in chores:
            chap.chore_done(c)
        usr = session['user']
        return redirect(url_for('chores', user=usr))

@app.route("/admintools", methods=['GET','POST'])
def run_chappy():
    trace = False

    chap.reset_chores('daily')
    chap.reset_chores('weekly')

    # Get array of users; (id, fname, lname, phone, email)
    usr = chap.query_db("select * from users", trace)
    usr.remove((1, 'admin', 'admin', '5555555555', 'admin@noreply.com', 'admin', 'admin'))
    # Get array of daily chores (id, chores, interval, done (true or false))
    chrs = chap.query_db("select * from chores where schedule = 'daily'")
    # Add names to chores for the Daily
    chap.build_user_chores(chrs, usr)
    # Get day of the week Monday = 0 Sunday = 6
    day = datetime.datetime.today().weekday()
    # Add names to the chores for weekly
    wk_chrs = chap.query_db("select * from chores where schedule = 'weekly'")
    chap.build_user_chores(wk_chrs, usr)

    # message and wk_chrs are dictionaries that hold all daily and weekly chores with the users name as the key
    # There are used in the resetsuccess html template.
    msg = {}
    wk_chrs = {}
    for u in usr:
        chrs = chap.query_db("SELECT * FROM chores where name = '" + str(u[1]) + "' and schedule = 'daily'")
        wk_chr = chap.query_db("SELECT * FROM chores where name = '" + str(u[1]) + "' and schedule = 'weekly'")
        # the last var in this function is debug mode, set to True this will not send sms message
        msg[u[1]]=chrs
        wk_chrs[u[1]]=wk_chr

    '''
    # Below is for testing only
    # Trouble shooting, this is how the loops work in the template:
    for k in msg:
        print(k)
        for c in msg[k]:
            print(c[1])
        for w in wk_chrs[k]:
            print(w[1])
    '''
    return render_template('resetsuccess.html', users = usr, chr = chrs, d = day, wchr = wk_chrs, message = msg)

class choreDone(Resource):
    def get(self, chr_name):
        return {'data': chap.chore_done(chr_name)}

class resetChores(Resource):
    def get(self, sched):
        return {'data': chap.reset_chores(sched)}

api.add_resource(choreDone, '/choredone/<chr_name>')
api.add_resource(resetChores, '/resetchores/<sched>')

if __name__ == '__main__':
    app.run(debug=True)
