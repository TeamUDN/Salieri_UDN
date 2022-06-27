
from gen_img.gen_img import generate
from googletrans import Translator

from chat import chat2
from chat import chat_gpt,chat_emoji
from mask_dec import detection
from mask_dec import cap

def responce(text,flag,model,chat):
    res=text
    choose=[]
    pose="def"
    

    if text=="こんにちは" and flag==0:
        f = open('txt/op.txt', 'r',encoding='UTF-8')
        t2 = f.read()
        choose=['・東京電機大学について','・人工知能研究室について','・私について']
        file_name=cap.cap()
        num=detection.test2(file_name)
        t=f"こんにちは！ {num}人のお客様！"
        res=t+t2


    if text=='東京電機大学について' and flag==0:
        f = open('txt/tdu.txt', 'r',encoding='UTF-8')
        res = f.read()
        

    if text=='人工知能 研究室について' and flag==0:
        f = open('txt/ailab.txt', 'r',encoding='UTF-8')
        res = f.read()
        
        
    if text=='私について' and flag==0:
        res="私はオープンキャンパス自動対応AIです。\n 実行できる音声認識コマンドは以下の通りです。"
        choose=['・会話モードを開始：　AIと雑談することができます。','・会話モードを終了：　会話モードを終了します。','・絵文字モードを開始：映画の題名から絵文字を推定します','・絵文字モードを終了：絵文字モードを終了します。'
        ,'・人の画像を生成　：　指定した特徴の顔画像を生成します。','・ありがとう　　　：　案内を終了します。']
    
    if text=='ぬるぽ':
        res="ガッ"

    if text=="人の画像を生成" and flag==0:
        flag=1
        res="どんな人を生成しますか"
        return res,choose,flag,model,chat,pose

    if text=="会話モードを開始" and flag==0:
        flag=2
        res="会話モードに移行します"
        return res,choose,flag,model,chat,pose

    if text=="絵文字モードを開始" and flag==0:
        flag=3
        res="絵文字モードに移行します"
        return res,choose,flag,model,chat,pose
    
    if text=="会話モードを終了":
        if flag!=2:
            res="会話モードはまだ開始していません。"
            return res,choose,flag,model,chat,pose
        else:
            flag=0
            res="会話モードを終了します。"

    if text=="絵文字モードを終了":
        if flag!=3:
            res="絵文字モードはまだ開始していません。"
            return res,choose,flag,model,chat,pose
        else:
            flag=0
            res="絵文字モードを終了します。"


    if text=="先輩" and flag==0:
        res="こんにちはクリスです"
        model="kurisu"
        return res,choose,flag,model,chat,pose

    if text=="サリエリ" and flag==0:
        res="こんにちはSalieriです"
        model="salieri"
        return res,choose,flag,model,chat,pose

    if text=="ドヤ顔"and flag==0:
        res="ドャッ"
        pose="doya"
        return res,choose,flag,model,chat,pose

    if text=="ありがとう" and flag==0:
        res="ご利用ありがとうございました"
        return res,choose,flag,model,chat,pose

    if text=="よろしく" and flag==0:
        file_name=cap.cap()
        #num=detection.test("C:/Users/student/2022_OC_Ikeda/Salieri_UDN/mask_dec/img")
        num=detection.test2(file_name)
        res=f"{num}人のお客様いらっしゃいませ"
        return res,choose,flag,model,chat,pose



        
        

    

    if flag==1:
        res=text+"を生成しました"

        tr = Translator()
        tr=tr.translate(text=text, src="ja", dest="en").text
        generate(tr)
        flag=0

    if flag==2:
        #res,prompt=chat2(text,chat)
        res,prompt=chat_gpt(text,chat)
        chat=prompt+res

    if flag==3:
        #res=chat2(text)
        res,prompt=chat_emoji(text,chat)
        #chat=prompt+res
        


    return res,choose,flag,model,chat,pose
        