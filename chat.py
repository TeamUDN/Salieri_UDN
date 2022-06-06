import requests
import json
import os
import openai

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


def chat_gpt(text,chat):
    prompt = chat
    



    openai.api_key = "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"

    start_sequence = "\nサリエリ:"
    restart_sequence = "\n人間: "

    input=text

    prompt=prompt+restart_sequence+input+start_sequence
    #print(prompt)

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["人間:", "サリエリ:"]
    )
    return response['choices'][0]['text'],prompt
