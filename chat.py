import requests
import json
import os
import openai

def chat2(word,chat):

    

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

    return res.json()['bestResponse']['utterance'],word


#print(chat2('こんにちは'))


def chat_gpt(text,chat):
    prompt = chat
    
    f = open('api.txt', 'r',encoding='UTF-8')
    api = f.read()

    f = open('txt/chat.txt', 'r',encoding='UTF-8')
    prompt= f.read()

    openai.api_key = api

    start_sequence = "\nサリエリ:"
    restart_sequence = "\nYou:"

    input=text

    input_sq=restart_sequence+input+start_sequence
    #print(prompt,chat,input_sq)
    prompt=prompt+chat+input_sq
    

    response = openai.Completion.create(
    engine="text-davinci-002",
    #engine="text-curie-001",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["You:", "サリエリ:"]
    )

    res=response['choices'][0]['text']
    print(prompt+res)
    return res,prompt


def chat_emoji(text,chat):

    prompt = chat
    
    f = open('api.txt', 'r',encoding='UTF-8')
    api = f.read()


    openai.api_key = api

    input=text
    prompt="映画のタイトルを絵文字に変換します。\n\nバック・トゥ・ザ・フューチャー：👨👴🚗🕒\nバットマン：🤵🦇\nトランスフォーマー：🚗🤖\nスターウォーズ：⭐️🌌\n"

    prompt=prompt+input+"："
    #print(prompt)

    
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.8,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
    )

    return response['choices'][0]['text'],prompt

def chat_eng(text,chat):
    
    f = open('api.txt', 'r',encoding='UTF-8')
    api = f.read()

    f = open('txt/chat_jpn_eng.txt', 'r',encoding='UTF-8')
    prompt= f.read()

    openai.api_key = api

    start_sequence = "\nSalieri:"
    restart_sequence = "\nYou:"

    input=text

    input_sq=restart_sequence+input+start_sequence
    #print(prompt,chat,input_sq)
    prompt=prompt+chat+input_sq

    

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
    )

    res=response['choices'][0]['text']
    print(prompt+res)
    return res,prompt

