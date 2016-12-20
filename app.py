from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "susan": "bye"
}


@auth.get_password
def get_password(username):
    if username in users:
        return users[username]
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def index():
    return "Hello World!"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return make_response(jsonify({'tasks': tasks}))

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_tasks():
    if not request.json or not 'task_type' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return make_response(jsonify({'task': task}), 201)

if __name__ == '__main__':
    app.run(debug=True)
