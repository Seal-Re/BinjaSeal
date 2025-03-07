from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义文件路径
users_file_path = os.path.join(script_dir, 'users.json')
chart_data_file_path = os.path.join(script_dir, 'chartData.json')
questions_file_path = os.path.join(script_dir, 'questions.json')
SAVE_FILE_PATH = os.path.join(script_dir, 'save.json')

# 封装文件读取函数
def read_json_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found.")
        return {} if 'users' in file_path or 'chartData' in file_path else []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {file_path}")
        return {} if 'users' in file_path or 'chartData' in file_path else []
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return {} if 'users' in file_path or 'chartData' in file_path else []

# 封装文件写入函数
def write_json_file(file_path, data, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error writing to {file_path}: {e}")
        return False

# 从本地文件读取用户信息
users = read_json_file(users_file_path, encoding='gbk')

# 从本地文件读取 chartData
chartData = read_json_file(chart_data_file_path, encoding='gbk')

# 从本地文件读取题目数据
questions = read_json_file(questions_file_path)

# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and username in users and users[username] == password:
        response = {
            "success": True,
        }
        return jsonify(response)
    else:
        response = {
            "success": False
        }
        return jsonify(response)

# 注册新用户
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"success": False, "message": "Username already exists"})
    else:
        users[username] = password
        if write_json_file(users_file_path, users, encoding='gbk'):
            return jsonify({"success": True, "message": "User registered successfully"})
        else:
            return jsonify({"success": False, "message": "Error saving user"})

# 提交
@app.route('/api/submit', methods=['POST'])
def submit_answers():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    user = data.get('user')
    submission_data = data.get('data')[0]  # 获取 data 数组中的第一个元素

    answerRecords = submission_data.get('answerRecords')
    answerResults = submission_data.get('answerResults')
    score = submission_data.get('score')
    date = submission_data.get('date')

    # 构建要保存的单次提交数据
    submission = {
        "answerRecords": answerRecords,
        "answerResults": answerResults,
        "score": score,
        "date": date
    }

    try:
        if os.path.exists(SAVE_FILE_PATH):
            # 如果文件存在，读取现有数据
            existing_data = read_json_file(SAVE_FILE_PATH)
        else:
            # 如果文件不存在，初始化
            existing_data = {}

        # 检查用户是否已经存在于数据中
        if user in existing_data:
            # 如果用户存在，直接在其 data 列表中添加新数据
            existing_data[user]["data"].append(submission)
        else:
            # 如果用户不存在，为该用户创建一个新的条目
            existing_data[user] = {
                "data": [submission]
            }

        # 将更新后的数据写回到文件中
        if write_json_file(SAVE_FILE_PATH, existing_data):
            return jsonify({"message": "答案提交成功，数据已保存到文件"})
        else:
            return jsonify({"message": "保存数据到文件时出错"}), 500
    except Exception as e:
        logging.error(f"Error in submit_answers: {e}")
        return jsonify({"message": f"保存数据到文件时出错: {str(e)}"}), 500

# 返回 chartData
@app.route('/api/chartData', methods=['GET'])
def get_chart_data():
    return jsonify(chartData)

# 根据用户名返回用户的答题记录
@app.route('/api/userAnswers', methods=['GET'])
def get_user_answers():
    username = request.args.get('username')
    if not username:
        return jsonify({"message": "Missing username parameter"}), 400

    try:
        # 读取 save.json 文件
        save_data = read_json_file(SAVE_FILE_PATH)
        if username in save_data:
            # 获取该用户的答题记录
            user_answers = save_data[username]["data"]
            return jsonify(user_answers)
        else:
            return jsonify([])
    except Exception as e:
        logging.error(f"Error getting user answers: {e}")
        return jsonify({"message": f"Error getting user answers: {str(e)}"}), 500
        
#获取用户最后一次分数
@app.route('/api/getLastScore', methods=['GET'])
def get_last_score():
    username = request.args.get('username')
    if not username:
        return jsonify({"message": "Missing username parameter"}), 400

    try:
        save_data = read_json_file(SAVE_FILE_PATH)
        if username in save_data and save_data[username]["data"]:
            last_submission = save_data[username]["data"][-1]
            return jsonify({"score": last_submission["score"]})
        else:
            return jsonify({"score": 0})
    except Exception as e:
        logging.error(f"Error getting last score: {e}")
        return jsonify({"message": f"Error getting last score: {str(e)}"}), 500

# 返回题目数据
@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True)