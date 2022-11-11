
from gen_img.gen_img import generate
from googletrans import Translator

from chat import chat2
from chat import chat_gpt,chat_emoji,chat_eng
from mask_dec import detection
from mask_dec import cap


def responce(text,flag,model,chat):
    """
    flag=0:コマンド受付
    flag=1:画像生成モード
    flag=2:会話モード
    flag=3:絵文字モード
    flag=4:英会話モード
    """
    res=text
    choose=[]
    pose="def"
    lang="jpn"

    if flag==0:
        choose=['・会話モードを開始　：　AIと自由に会話できます。','・絵文字モードを開始：映画の題名から絵文字を推定します','・英会話モードを開始　：　質問に対して英語で答えます。'
        ,'・人の画像を生成　：　指定した特徴の顔画像を生成します。','・こんにちは　：　案内を開始します','・ありがとう　　　：　案内を終了します。']

    if text=="OK サリエリ":
        res="お呼びでしょうか \n  以下の音声認識コマンドを入力してください"
        choose=['・会話モードを開始　：　AIと自由に会話できます。','・絵文字モードを開始：映画の題名から絵文字を推定します','・英会話モードを開始　：　質問に対して英語で答えます。'
        ,'・人の画像を生成　：　指定した特徴の顔画像を生成します。','・こんにちは　：　案内を開始します','・ありがとう　　　：　案内を終了します。']
        flag=0
        chat=0
        return res,choose,flag,model,chat,pose,lang
    

    if text=="こんにちは" and flag<=0:
        f = open('txt/op.txt', 'r',encoding='UTF-8')
        t2 = f.read()
        choose=['・東京電機大学について','・人工知能研究室について','・私について']
        file_name=cap.cap()
        num=detection.test2(file_name)
        #num="hoge"
        t=f"こんにちは！ {num}人のお客様！"
        res=t+t2
        return res,choose,flag,model,chat,pose,lang


    if text=='東京電機大学について':
        f = open('txt/tdu.txt', 'r',encoding='UTF-8')
        res = f.read()
        choose=['・東京電機大学について','・人工知能研究室について','・私について']
        flag=2
        return res,choose,flag,model,chat,pose,lang
        

    if text=='人工知能 研究室について':
        f = open('txt/ailab.txt', 'r',encoding='UTF-8')
        res = f.read()
        choose=['・東京電機大学について','・人工知能研究室について','・私について']
        flag=2
        return res,choose,flag,model,chat,pose,lang
        
        
    if text=='私について':
        res="私はオープンキャンパス自動対応AIです。\n 私に何か質問はありますか？　\n もし音声認識コマンドを実行したい場合は OK サリエリ と話しかけて下さい "
        choose=[]
        flag=2
        return res,choose,flag,model,chat,pose,lang

    
    if text=='ぬるぽ':
        res="ガッ"
        return res,choose,flag,model,chat,pose,lang

    if ("画像" in text) and flag==0:
        flag=1
        res="どんな人を生成しますか"
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    
    if text=="会話モードを開始" and flag==0:
        flag=2
        res="会話モードに移行します"
        chat=0
        return res,choose,flag,model,chat,pose,lang
    

    if ("絵文字" in text) and flag==0:
        flag=3
        res="絵文字モードに移行します"
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    if ("英" in text) and flag==0:
        flag=4
        res="英会話モードを開始します"
        choose=[]
        chat=0
        return res,choose,flag,model,chat,pose,lang
    
    if text=="会話モードを終了":
        if flag!=2:
            res="会話モードはまだ開始していません。"
            return res,choose,flag,model,chat,pose,lang
        else:
            flag=2
            res="会話モードを終了します。"
    

    if text=="英会話モードを終了":
        if flag!=4:
            res="英会話モードはまだ開始していません"
            choose=[]
            return res,choose,flag,model,chat,pose,lang
        else:
            flag=2
            res="英会話モードを終了します"
            choose=[]
            return res,choose,flag,model,chat,pose,lang

    if text=="絵文字モードを終了":
        if flag!=3:
            res="絵文字モードはまだ開始していません。"
            choose=[]
            return res,choose,flag,model,chat,pose,lang
        else:
            flag=2
            res="絵文字モードを終了します。"
            choose=[]
            return res,choose,flag,model,chat,pose,lang


    if text=="先輩" and flag==0:
        res="こんにちはクリスです"
        model="kurisu"
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    if text=="サリエリ" and flag==0:
        res="こんにちはSalieriです"
        model="salieri"
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    if text=="ドヤ顔"and flag==0:
        res="ドャッ"
        pose="doya"
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    if text=="ありがとう" and flag==0:
        res="ご利用ありがとうございました"
        flag=-1
        choose=[]
        return res,choose,flag,model,chat,pose,lang

    if text=="よろしく" and flag==0:
        file_name=cap.cap()
        num=detection.test2(file_name)
        #num="hoge"
        res=f"{num}人のお客様いらっしゃいませ"
        return res,choose,flag,model,chat,pose,lang



        
        

    

    if flag==1:
        res=text+"を生成しました"

        tr = Translator()
        tr=tr.translate(text=text, src="ja", dest="en").text
        generate(tr)
        flag=2
        return res,choose,flag,model,chat,pose,lang

    if flag==2:
        #res,prompt=chat2(text,chat)
        res,prompt=chat_gpt(text,chat)
        chat=prompt+res
        return res,choose,flag,model,chat,pose,lang

    if flag==3:
        #res=chat2(text)
        res,prompt=chat_emoji(text,chat)
        #chat=prompt+res
        return res,choose,flag,model,chat,pose,lang

    if flag==4:
        #res=chat2(text)
        res,prompt=chat_eng(text,chat)
        if res=="":
            chat=0
        else:
            chat=prompt+res
        lang="eng"
        return res,choose,flag,model,chat,pose,lang


        

    return res,choose,flag,model,chat,pose,lang
        