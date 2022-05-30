from flask import Flask, render_template, jsonify, request, session, send_from_directory
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/')
def index():
    return render_template('index.html')

# /showにPOSTリクエストが送られたら処理してJSONを返す
@app.route('/chat', methods=['POST'])
def show():

    txt=request.json['chatMessage']

    return_json = {
        "message": txt + "おけまる",
        "choose": ["hoge","fuga"]
    }

    return jsonify(values=json.dumps(return_json))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力
