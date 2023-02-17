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

if __name__ == '__main__':
    app.run(debug=True)
