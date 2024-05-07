from flask import Flask,jsonify,request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/api/result',methods=['GET'])
def show_result():
    roll = request.args.get('roll')
    result = collection.find_one({"roll":roll})
    if result:
        return jsonify(result),200
    else:
        return jsonify({"msg":"data not found"}),404

@app.route('/api/data')
def show_all_data():
    data = list(collection.find())
    return jsonify(data),200


if __name__ == '__main__': 
    app.run(port=3000) 