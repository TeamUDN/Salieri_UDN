import requests
import json

def chat2(word):

    

    # リクエストに必要なパラメーター
    headers = {'content-type':'text/json'}
    payload = {'utterance':word,
                "username":"マスター",
                "agentState":{"agentName":"Salieri","tone":"normal", "age":"0歳"},}

    # APIKEYの部分は自分のAPI鍵を代入してください
    url = 'https://www.chaplus.jp/v1/chat?apikey=629d99df19335'

    # APIを叩く
    res = requests.post(url=url, headers=headers, data=json.dumps(payload))

    # 最適と思われるレスポンスを抽出
    print(res.json()['bestResponse']['utterance'])
    return res.json()['bestResponse']['utterance']

#print(chat2('こんにちは'))