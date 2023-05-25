from flask import Flask, jsonify, request
import psycopg2
from tasks import Tasks
from progress import Progress
from viewer import ProgressPerTime
from datetime import datetime


app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    all_tasks = {'tasks': []}
    task = Tasks('', '', '', 0, '', '')
    tasks_data = task.read_all_tasks()
    for task_data in tasks_data:
        new_task = Tasks('', '', '', 0, '', '')
        if len(task_data) >= 2:
            new_task.name = task_data[1]
            new_task.link = task_data[2]
            new_task.description = task_data[3]
            new_task.group_id = task_data[4]
            new_task.priority = task_data[5]
            new_task.status = task_data[6]
            all_tasks['tasks'].append(new_task.__dict__)
    return jsonify(all_tasks)
    

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks('', '', '', 0, 0, '', '')
    task_data = task.read_task(task_id)
    task.name = task_data[1]
    task.link = task_data[2]
    task.description = task_data[3]
    task.group_id = task_data[4]
    task.progress_id = task_data[5]
    task.priority = task_data[6]
    task.status = task_data[7]
    return jsonify(task.__dict__)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    print("JSON Data",data)
    task = Tasks(data['name'], data['link'], data['description'], data['group_id'],  (data['priority']), (data['status']))
    task.create_task()
    return jsonify({'message': 'Task created successfully'})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Tasks('', '', '', 0, '', '')
    task_data = task.read_task(task_id)
    task.name = task_data[1]
    task.link = task_data[2]
    task.description = task_data[3]
    task.group_id = task_data[4]
    task.priority = task_data[5]
    task.status = task_data[6]
    if 'status' in data:
        task.update_task_status(task_id, data['status'])
    if 'group_id' in data:
        task.update_task_group(task_id, data['group_id'])
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks('', '', '', 0, 0, '', '')
    task.delete_task(task_id)
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/progress', methods=['POST'])
def create_progress():
    data = request.get_json()
    print("JSON Data",data)
    new_progress = Progress(data['task_id'],data['start_date_time'],data['end_date_time'],data['progress_time'],data['comments'])
    new_progress.create_progress()
    return {'message': 'Progress created successfully.'}, 201

@app.route('/progress/<int:progress_id>', methods=['GET'])
def read_progress(progress_id):
    if progress_id:
        progress = Progress().read_progress(progress_id)
        if progress:
            return {'id': progress[0], 'task_id': progress[1], 
                    'start_date_time': progress[2], 'end_date_time': progress[3],
                    'progress_time': progress[4], 'comments': progress[5]}, 200

    return {'message': 'Progress record not found.'}, 404

@app.route('/progress/<int:progress_id>', methods=['PUT'])
def update_progress(progress_id):
    data = request.get_json()
    start_date_time = data['start_date_time']
    end_date_time = data['end_date_time']
    progress_time = data['progress_time']
    comments = data['comments']
    Progress().update_progress(progress_id, start_date_time, end_date_time, progress_time, comments)
    return {'message': 'Progress updated successfully.'}, 200

@app.route('/progress/<int:progress_id>', methods=['DELETE'])
def delete_progress(progress_id):
    Progress().delete_progress(progress_id)
    return {'message': 'Progress deleted successfully.'}, 200

@app.route('/viewprogress', methods=['GET'])
def viewprogress():
    all_tasks = {'tasks': []}
    data = request.get_json()
    print(data)
    start_date_time = data['start_date_time']
    end_date_time = data['end_date_time']
    start_date_time = datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
    end_date_time = datetime.strptime(end_date_time, '%Y-%m-%d %H:%M:%S')
    progressPerTime = ProgressPerTime()
    progress_data = progressPerTime.view_tasks_progress(start_date_time, end_date_time)
    for task_data in progress_data:
        new_task = ProgressPerTime()
        if len(task_data) >= 2:
            new_task.task_id=task_data[0]
            new_task.name = task_data[1]
            new_task.link = task_data[2]
            new_task.description = task_data[3]
            new_task.group_id = task_data[4]
            new_task.status = task_data[5]
            new_task.priority = task_data[6]
            new_task.progress_id = task_data[7]
            new_task.start_date_time = task_data[8]
            new_task.end_date_time = task_data[9]
            new_task.progress_time = task_data[10]
            new_task.comments = task_data[11]
        all_tasks['tasks'].append(new_task.__dict__)
    return jsonify(all_tasks)




if __name__ == '__main__':
    app.run()