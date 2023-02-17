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
    try:
        output = []
        for task in mongo.db.tasks.find():
            output.append({'id': str(task['_id']), 'description': task['description'], 'completed': task['completed']})
        return jsonify({'tasks': output}), 200
    except:
        return jsonify({'error': 'An error occurred'}), 500



# API to get a particular task
@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            output = {'id': str(task['_id']), 'description': task['description'], 'completed': task['completed']}
            return jsonify({'task': output}), 200
        else:
            return jsonify({'error': 'No such task exist'}), 404
    except:
        return jsonify({'error': 'An error occurred'}), 500


# API to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        description = request.json.get('description', '')
        task_id = mongo.db.tasks.insert_one({'description': description, 'completed': False}).inserted_id
        new_task = mongo.db.tasks.find_one({'_id': task_id})
        output = {'id': str(new_task['_id']), 'description': new_task['description'], 'completed': new_task['completed']}
        return jsonify({'task': output}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# API to update an existing task
@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            description = request.json.get('description', task['description'])
            mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': { 'description': description}})
            updated_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
            output = {'id': str(updated_task['_id']), 'description': updated_task['description'], 'completed': updated_task['completed']}
            return jsonify({'task': output}), 200
        else:
            return jsonify({'error': 'No such task exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Mark a task as complete
@app.route('/tasks/<string:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        if task['completed']:
            return jsonify({'message': 'Task is already completed'}), 200
        else:
            mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': True}})
            updated_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
            output = {'id': str(updated_task['_id']), 'description': updated_task['description'], 'completed': updated_task['completed']}
            return jsonify({'task': output}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
