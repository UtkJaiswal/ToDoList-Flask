# To-Do List API

This is a simple Flask-based API for managing a to-do list. The API provides endpoints for adding, updating, deleting, and completing tasks. The tasks are stored in a MongoDB database.

## Requirements

- Python 3.10.6
- Flask
- Flask-PyMongo
- PyMongo

## Installation

1. Clone the repository
2. Install the required packages by running `pip install -r requirements.txt`
3. Start the MongoDB server

## Usage

1. Navigate to the project directory
2. Start the Flask server: `flask run`
3. Use a tool like Postman to send HTTP requests to the server and test the API endpoints

## API Endpoints

### GET /tasks

Get all tasks.

### GET /tasks/\<string:task_id>

Get a single task by ID.

### POST /tasks

Add a new task.

### PUT /tasks/\<string:task_id>/complete

Mark a task as complete.

### PUT /tasks/\<string:task_id>/incomplete

Mark a task as incomplete.

### DELETE /tasks/\<string:task_id>

Delete a task by ID.


