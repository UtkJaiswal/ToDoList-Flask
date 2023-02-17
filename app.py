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


# API to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        output = []
        for task in mongo.db.tasks.find():
            output.append({'id': str(task['_id']), 'description': task['description'], 'completed': task['completed']})
        return jsonify({'tasks': output}), 200
    except:
        # If an error occurs, return a 500 error response with an error message
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
            # If no task is found, return a 404 error response with an error message
            return jsonify({'error': 'No such task exists'}), 404
    except:
        # If an error occurs, return a 500 error response with an error message
        return jsonify({'error': 'An error occurred'}), 500



# API to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        # Get the description of the new task from the request body
        description = request.json.get('description', '')

        # Insert the new task into the database with the provided description and a completed status of False
        task_id = mongo.db.tasks.insert_one({'description': description, 'completed': False}).inserted_id

        # Find the newly created task from the database using its ID
        new_task = mongo.db.tasks.find_one({'_id': task_id})

        # Create a dictionary with the details of the new task
        output = {'id': str(new_task['_id']), 'description': new_task['description'], 'completed': new_task['completed']}

        # Return a JSON response with the details of the newly created task and a status code of 201 (created)
        return jsonify({'task': output}), 201
    except Exception as e:
        # Return a JSON response with an error message and a status code of 500 (internal server error) if an exception occurs
        return jsonify({'error': str(e)}), 500


# API to update an existing task
@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        # Find the task to be updated in the database using its ID
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            # Get the new description of the task from the request body, or use the existing description if none is provided
            description = request.json.get('description', task['description'])

            # Update the description of the task in the database
            mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': { 'description': description}})

            # Find the updated task from the database using its ID
            updated_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})

            # Create a dictionary with the details of the updated task
            output = {'id': str(updated_task['_id']), 'description': updated_task['description'], 'completed': updated_task['completed']}

            # Return a JSON response with the details of the updated task and a status code of 200 (OK)
            return jsonify({'task': output}), 200
        else:
            # Return a JSON response with an error message and a status code of 404 (not found) if the task to be updated is not found
            return jsonify({'error': 'No such task exist'}), 404
    except Exception as e:
        # Return a JSON response with an error message and a status code of 500 (internal server error) if an exception occurs
        return jsonify({'error': str(e)}), 500


# API to mark an incomplete task as complete
@app.route('/tasks/<string:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    try:
        # Find the task with the given task_id
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            # If the task is already completed, return a message to the client
            if task['completed']:
                return jsonify({'message': 'Task is already completed'}), 200
            else:
                # Update the task to be marked as completed
                mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': True}})
                # Retrieve the updated task and create an output dictionary
                updated_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
                output = {'id': str(updated_task['_id']), 'description': updated_task['description'], 'completed': updated_task['completed']}
                # Return the output dictionary to the client
                return jsonify({'task': output}), 200
        else:
            # If the task is not found, return an error message to the client
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        # If an error occurs, return an error message to the client with a 500 status code
        return jsonify({'error': str(e)}), 500


# API to mark a complete task as incomplete
@app.route('/tasks/<string:task_id>/incomplete', methods=['PUT'])
def incomplete_task(task_id):
    try:
        # Find the task with the given task_id
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            # If the task is already incomplete, return an error message to the client
            if not task['completed']:
                return jsonify({'error': 'Task is already incomplete'}), 400
            else:
                # Update the task to be marked as incomplete
                mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': False}})
                # Retrieve the updated task and create an output dictionary
                updated_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
                output = {'id': str(updated_task['_id']),  'description': updated_task['description'], 'completed': updated_task['completed']}
                # Return the output dictionary to the client
                return jsonify({'task': output})
        else:
            # If the task is not found, return an error message to the client
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        # If an error occurs, return an error message to the client with a 500 status code
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500



# API to Delete a task
@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Find the task in the database
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if task:
            # If the task exists, delete it
            mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
            return jsonify({'result': 'Task deleted successfully'}), 200
        else:
            # If the task does not exist, return an error message
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        # If there is an exception, return an error message
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500





if __name__ == '__main__':
    app.run(debug=True)
