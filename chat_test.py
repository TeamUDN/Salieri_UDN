import os
import openai
f = open('api.txt', 'r',encoding='UTF-8')
api = f.read()


openai.api_key = api

start_sequence = "\nサリエリ:"
restart_sequence = "\n人間: "
prompt="以下はAIアシスタントとの会話です。アシスタントは親切で、創造的で、賢く、とてもフレンドリーです。\n\n人間:こんにちは、あなたは誰ですか？\nサリエリ:私はRyunosuke Ikedaによって作成されたAIですが、今日はどのようにお手伝いできますか？"

input="こんにちは"

prompt=prompt+restart_sequence+input+start_sequence
print(prompt)
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
print(response['choices'][0]['text'])
