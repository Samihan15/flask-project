from flask import Flask,jsonify, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

client = MongoClient('mongodb://localhost:27017/') 
db = client['demo'] 
collection = db['data'] 

@app.route('/api/info', methods=['POST'])
def add_student_info():
    data = request.json
    if data:
        collection.insert_one(data)
        return jsonify({"msg":"data inserted successfully !"}),201
    else:
        return jsonify({"msg":"something went wrong !"}),400

@app.route('/api/result', methods=['GET'])
def show_result():
    roll = request.args.get('roll')
    result = collection.find_one({"roll": roll})
    if result:
        result['_id'] = str(result['_id'])
        print(result)
        return jsonify(result), 200
    else:
        return jsonify({"msg": "data not found"}), 404
    
@app.route('/api/data', methods=['GET'])
def show_all_data():
    students = list(collection.find())

    for student in students:
        student['_id'] = str(student['_id'])

        total_marks = sum(int(mark) for mark in student['score'].values())
        total_subjects = len(student['score'])
        cgpa = total_marks / (total_subjects * 10)
        student['cgpa'] = cgpa

        backlog_subjects = [subject for subject, score in student['score'].items() if int(score) < 40]
        student['backlog'] = ", ".join(backlog_subjects) if backlog_subjects else None
        student['result'] = 'Pass' if not backlog_subjects else 'Fail'

    return jsonify(students)

app.secret_key = 'your_secret_key'  
ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin123'


@app.route('/', methods=['POST'])
def login():
    data = request.json
    if data and 'email' in data and 'password' in data:
        email = data['email']
        password = data['password']
        
        if email == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    else:
        return jsonify({'success': False, 'message': 'Invalid request'})

if __name__ == '__main__': 
    app.run(port=3000,host='0.0.0.0') 
    
