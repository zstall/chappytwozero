import chap
from flask import Flask, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello():

    chores = chap.query_db("select name, chore from chores")
    names = chap.query_db("select fname from users")
    dic = {}
    for nm in names:
        dic[nm[0]]=[]

    for nm in chores:
        dic[nm[0]]+=[nm[1]]

    return render_template('index.html', chrs=dic)

class choreDone(Resource):
    def get(self, chr_name):
        return {'data': chap.chore_done(chr_name)}

class resetChores(Resource):
    def get(self, sched):
        return {'data': chap.reset_chores(sched)}

api.add_resource(choreDone, '/choredone/<chr_name>')
api.add_resource(resetChores, '/resetchores/<sched>')

if __name__ == '__main__':
     app.run()
