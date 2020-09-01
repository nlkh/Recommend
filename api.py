import os
import numpy as np
import DB_Connection as dbc
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Create_node(Resource) :
    def get(self):
        try :
            # parsing
            parser = reqparse.RequestParser()
            parser.add_argument('member_no', type=str)
            parser.add_argument('content_id', type=str)
            parser.add_argument('content_type', type=str)
            args = parser.parse_args()

            # argv1 : member_no, argv2 : content_id, argv3 : content_type
            member_no = int(args['member_no'])
            content_id = int(args['content_id'])
            content_type = int(args['content_type'])

            # load user who stored the same content from DB
            sql = "select member_no, node_no from node where content_id = %s and content_type = %s order by member_no"
            dbc.cursor.execute(sql, (content_id, content_type))
            rows = dbc.cursor.fetchall()

            sql = "select max(member_no) from member"
            dbc.cursor.execute(sql)
            max_member = dbc.cursor.fetchone()['max(member_no)']

            # make list who have the same content
            having_list = []
            for i in range(0, max_member+1) :
                having_list.append(0)
            for row in rows :
                having_list[row['member_no']] = 1

            # make nparray with having_list
            array = np.array(having_list)

            # add with dataset
            similarity = np.load(os.getcwd()+'\\..\\Recommend.npy')
            similarity[member_no] = similarity[member_no] + array
            np.save(os.getcwd(), similarity)

            return {'status':'success'}
        except Exception as e:
            return {'error':str(e)}

class Drop_node(Resource) :
    def get(self):
        try :
            # parsing
            parser = reqparse.RequestParser()
            parser.add_argument('member_no', type=str)
            parser.add_argument('content_id', type=str)
            parser.add_argument('content_type', type=str)
            args = parser.parse_args()

            # argv1 : member_no, argv2 : content_id, argv3 : content_type
            member_no = int(args['member_no'])
            content_id = int(args['content_id'])
            content_type = int(args['content_type'])

            # load user who stored the same content from DB
            sql = "select member_no, node_no from node where content_id = %s and content_type = %s order by member_no"
            dbc.cursor.execute(sql, (content_id, content_type))
            rows = dbc.cursor.fetchall()

            sql = "select max(member_no) from member"
            dbc.cursor.execute(sql)
            max_member = dbc.cursor.fetchone()['max(member_no)']

            # make list who have the same content
            having_list = []
            for i in range(0, max_member+1) :
                having_list.append(0)
            for row in rows :
                having_list[row['member_no']] = -1

            # make nparray with having_list
            array = np.array(having_list)

            # add with dataset
            similarity = np.load(os.getcwd()+'\\..\\Recommend.npy')
            similarity[member_no] = similarity[member_no] + array
            np.save(os.getcwd(), similarity)

            return {'status':'success'}
        except Exception as e:
            return {'error':str(e)}

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

api.add_resource(Create_node, '/create_node')
api.add_resource(Register, '/register')
api.add_resource(Drop_node, '/drop_node')

if __name__ == "__main__" :
    app.run(debug=True)

