from flask import Flask, render_template, jsonify, request, session, send_from_directory
import json
from res import responce

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.secret_key = 'secret'


@app.route('/')
def index():
    session["flag"]=0
    session["model"]="Salieri"

    return render_template('index.html')

# /showにPOSTリクエストが送られたら処理してJSONを返す
@app.route('/chat', methods=['POST'])
def show():
    flag=session["flag"]
    txt=request.json['chatMessage']
    model=session["model"]

    res,choose,flag,model=responce(txt,flag,model)

    session["flag"]=flag
    session["model"]=model

    return_json = {
        "message": res,
        "choose": choose,
        "pose": "hoge",
        "model": model
    }

    return jsonify(values=json.dumps(return_json))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力
