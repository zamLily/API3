from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)


SERVERS = []
server_id = 0


def find_server(server_id):
    find = 0
    index = 0
    for server in SERVERS:
        if server['id'] == server_id:
            find = 1
            break
        index = index + 1

    if find == 0:
        return -1
    else:
        return index


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('ip')
parser.add_argument('status')

# single server
class Servers(Resource):
    def get(self, server_id):
        if(find_server(server_id) + 1):
            index = find_server(server_id)
            return SERVERS[index]
        else:
            abort(404, message="Server {} doesn't exist".format(server_id))


    def delete(self, server_id):
        if (find_server(server_id) + 1):
            index = find_server(server_id)

            del SERVERS[index]
            return '', 204
        else:
            abort(404, message="Server {} doesn't exist".format(server_id))


    def put(self, server_id):
        args = parser.parse_args()
        task = {'id': args['id'], 'ip': args['ip'], 'status': args['status']}
        if (find_server(server_id) + 1):
            index = find_server(server_id)
            SERVERS[index] = task
        else:
            SERVERS.append(task)
        return task, 201


# serverlist
class ServerList(Resource):
    def get(self):
        return SERVERS

    def post(self):
        args = parser.parse_args()
        server_id = args['id']
        if (find_server(server_id) == -1):
            task = {'id': args['id'], 'ip': args['ip'], 'status': args['status']}
            SERVERS.append(task)
            return SERVERS, 201

        else:
            abort(404, message="Server {} has already existed".format(server_id))



# Actually setup the Api resource
api.add_resource(ServerList, '/servers')
api.add_resource(Servers, '/servers/<server_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    #app.run(debug=True)

