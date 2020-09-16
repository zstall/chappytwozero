import chap
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
