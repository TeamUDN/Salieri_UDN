
from gen_img.gen_img import generate
from googletrans import Translator
from chat import chat2

def responce(text,flag):
    res=text
    choose=[]

    if text=="こんにちは":
        res="こんにちは!　東京電機大学、人工知能研究室へようこそ。   どんなことを知りたいですか？以下の3つの中のどれかを読み上げて下さい。"
        choose=['・東京電機大学について','・人工知能研究室について','・私について']

    if text=='東京電機大学について':
        res="東京電機大学は山の上にあります"
        

    if text=='人工知能研究室について':
        res="人工知能研究室は山の上にあります"
        
        
    if text=='私について':
        res="私はこんなことができます"
        choose=['・会話モードを開始：　AIと雑談することができます。','・会話モードを終了：　会話モードを終了します。'
        ,'・人の画像を生成　：　指定した特徴の顔画像を生成します。','・ありがとう　　　：　案内を終了します。']

    if text=="人の画像を生成":
        flag=1
        res="どんな人を生成しますか"
        return res,choose,flag

    if text=="会話モードを開始":
        flag=2
        res="会話モードに移行します"
        return res,choose,flag
    
    if text=="会話モードを終了":
        if flag!=2:
            res="会話モードはまだ開始していません。"
            return res,choose,flag
        else:
            flag=0
            res="会話モードを終了します。"
    

    if flag==1:
        res=text+"を生成しました"

        tr = Translator()
        tr=tr.translate(text=text, src="ja", dest="en").text
        generate(tr)
        flag=0

    if flag==2:
        res=chat2(text)


    return res,choose,flag
        

