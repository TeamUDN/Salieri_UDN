
#from gen_img.gen_img import generate
#from googletrans import Translator

from chat import chat2
from chat import chat_gpt

def responce(text,flag,model,chat):
    res=text
    choose=[]

    if text=="こんにちは" and flag==0:
        f = open('txt/op.txt', 'r',encoding='UTF-8')
        res = f.read()
        choose=['・東京電機大学について','・人工知能研究室について','・私について']

    if text=='東京電機大学について' and flag==0:
        f = open('txt/tdu.txt', 'r',encoding='UTF-8')
        res = f.read()
        

    if text=='人工知能 研究室について' and flag==0:
        f = open('txt/ailab.txt', 'r',encoding='UTF-8')
        res = f.read()
        
        
    if text=='私について' and flag==0:
        res="私はこんなことができます"
        choose=['・会話モードを開始：　AIと雑談することができます。','・会話モードを終了：　会話モードを終了します。'
        ,'・人の画像を生成　：　指定した特徴の顔画像を生成します。','・ありがとう　　　：　案内を終了します。']
    
    if text=='ぬるぽ':
        res="ガッ"

    if text=="人の画像を生成" and flag==0:
        flag=1
        res="どんな人を生成しますか"
        return res,choose,flag,model,chat

    if text=="会話モードを開始" and flag==0:
        flag=2
        res="会話モードに移行します"
        return res,choose,flag,model,chat
    
    if text=="会話モードを終了":
        if flag!=2:
            res="会話モードはまだ開始していません。"
            return res,choose,flag,model,chat
        else:
            flag=0
            res="会話モードを終了します。"


    if text=="先輩" and flag==0:
        res="こんにちは"
        model="kurisu"
        return res,choose,flag,model,chat
        

    

    if flag==1:
        res=text+"を生成しました"

        #tr = Translator()
        #tr=tr.translate(text=text, src="ja", dest="en").text
        #generate(tr)
        flag=0

    if flag==2:
        #res=chat2(text)
        res,prompt=chat_gpt(text,chat)
        chat=prompt+res
        


    return res,choose,flag,model,chat
        