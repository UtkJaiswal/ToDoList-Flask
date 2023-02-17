from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configure the app with MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tasks'
mongo = PyMongo(app)


app = Flask(__name__)

# Configure the app with MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tasks'
mongo = PyMongo(app)


#test api
@app.route('/', methods=['GET'])
def test_API():
    return jsonify({'message': "Your API is working fine"})

# API to Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    output = []
    for task in mongo.db.tasks.find():
        output.append({'id': str(task['_id']), 'description': task['description'], 'completed': task['completed']})
    return jsonify({'tasks': output})


# API to get a particular task
@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        output = {'id': str(task['_id']), 'description': task['description'], 'completed': task['completed']}
        return jsonify({'task': output})
    else:
        return jsonify({'error': 'No such task exist'})

# API to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    description = request.json.get('description', '')
    task_id = mongo.db.tasks.insert_one({ 'description': description, 'completed': False}).inserted_id
    # task_id = str(mongo.db.tasks.insert_one({'title': title, 'description': description, 'completed': False}).inserted_id)
    # print("task_id is",task_id)
    new_task = mongo.db.tasks.find_one({'_id': task_id})
    output = {'id': str(new_task['_id']), 'description': new_task['description'], 'completed': new_task['completed']}
    return jsonify({'task': output})

if __name__ == '__main__':
    app.run(debug=True)
