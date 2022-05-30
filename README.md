# Salieri_UDN


## 環境構築(venv)
```
python -m venv .venv

#環境に入る(Windowsの場合)
./.venv/Scripts/activate
#環境に入る(Macの場合)
source .venv/bin/activate
```
## 環境構築(Anaconda)
パッケージのインストール
```
conda env create -n Salieri -f Salieri.yml
conda activate Salieri
pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
pip install git+https://github.com/openai/CLIP.git
pip install flask gunicorn 
```

ビルド
node.jsを入れていない場合は以下のサイトからインストール
https://nodejs.org/ja/download/
```
npm run build
```
