from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('top.html')

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。    
# webブラウザーには、「localhost:5000」と入力