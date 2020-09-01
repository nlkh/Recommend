import numpy as np
import DB_Connection as dbc
import os
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def arrayAppend(index, array):
    if (index <= array.shape[0]):
        return array
    newArray = np.zeros([index + 1, index + 1], dtype=int)
    newArray[:array.shape[0], :array.shape[0]] = array
    return newArray

class Register(Resource) :
    def get(self) :
        sql = 'select max(member_no) from member'
        dbc.cursor.execute(sql)
        member_no = dbc.cursor.fetchone()['max(member_no)']
        similarity = np.load(os.getcwd() + '\\..\\Recommend.npy')
        similarity = arrayAppend(member_no, similarity)
        np.save(os.getcwd(), similarity)
        return {'status': 'success'}

api.add_resource(Register, '/register')

if __name__ == '__main__' :
    app.run(debug=True)