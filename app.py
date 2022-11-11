from flask import Flask, render_template, jsonify, request, session, send_from_directory
import json
from res import responce

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.secret_key = 'secret'


@app.route('/')
def index():
    session["flag"]=-1
    session["model"]="Salieri"


    session["chat"]=""

    return render_template('index.html')

# /showにPOSTリクエストが送られたら処理してJSONを返す
@app.route('/chat', methods=['POST'])
def show():
    flag=session["flag"]
    txt=request.json['chatMessage']
    model=session["model"]
    chat=session["chat"]

    res,choose,flag,model,chat,pose,lang=responce(txt,flag,model,chat)


    
    #状態の更新
    session["flag"]=flag
    session["model"]=model

    if chat!="":
        if chat==0:
            print("chat reset")
            session["chat"]=""
        else:
            chat_sq=session["chat"]+chat
            chat_list=chat_sq.split("You:")
            #print(chat_list)
            if len(chat_list)>4:
                chat_sq="\nYou:"+chat_list[-3]+"You:"+chat_list[-2]+"You:"+chat_list[-1]

            print("-----")
            #print(chat_sq)
            session["chat"]=chat_sq
    
    
    

    return_json = {
        "message": res,
        "choose": choose,
        "pose": pose,
        "model": model,
        "lang":lang
    }

    return jsonify(values=json.dumps(return_json))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力
