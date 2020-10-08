import chap
import os
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
            return redirect(url_for('chores'))

    return render_template('login.html')


@app.route("/chores", methods=['GET', 'POST'])
def chores():

    if g.user == 'admin':
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

        print(done_chores)
        print(dic_done)
        for nm in done_chores:
            if nm[0] == 'admin':
                pass
            else:
                dic_done[nm[0]]+=[nm[1]]
        return render_template('chores.html', chrs=dic_login, dchrs=dic_done, user=session['user'])

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
            print(c)
            chap.chore_done(c)
        return redirect(url_for('chores'))

    return redirect(url_for('chores'))

@app.route("/incomplete", methods=['GET', 'POST'])
def incomplete_chores():
    if request.method == 'POST':
        chores = (request.form.getlist('chr'))
        for c in chores:
            chap.chore_done(c)
        return redirect(url_for('chores'))

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
