const face = new Vue({
  el: '#face',
  // FlaskとVueを共存させるためにDelimiterを変更する
  delimiters: ["[[", "]]"],
  data: {
    pose: 'hellovrm',
    model: 'salieri',
    pageChangeFlag: true,
    dialogueCount: 4,
    getMessage: "",
    recognition: null,
    recordingStartFlagCount: 0,
    debugFlg: '',
    modelMessage: '人間を検出しました　\n いらっしゃいませ！私はオープンキャンパス案内AIです。「こんにちは」と話しかけて下さい。',
    choiceArr: [],
  },
  mounted: function () {
    this.faceFuncStart();
    this.webSpeechAPI();
  },
  methods: {
    faceFuncStart: function () {
      var video = document.getElementById("video");
      var canvas = document.getElementById("faceCanvas");
      var context = canvas.getContext("2d");
      // getUserMedia によるカメラ映像の取得
      // メディアデバイスを取得
      var media = navigator.mediaDevices.getUserMedia({
        // カメラの映像を使う（スマホならインカメラ）
        video: { facingMode: "user" },
        // マイクの音声は使わない
        audio: false
      });
      // メディアデバイスが取得できたら
      media.then((stream) => {
        // video 要素にストリームを渡す
        video.srcObject = stream;
      });
      // clmtrackr の開始
      // tracker オブジェクトを作成
      var tracker = new clm.tracker();
      // tracker を所定のフェイスモデル（※）で初期化
      tracker.init(pModel);
      // video 要素内でフェイストラッキング開始
      tracker.start(video);

      //☆ページ遷移用のカウントとフラグ
      var facetimeCount = 0;
      var NotfacetimeCount = 0;

      var self = this;

      this.$nextTick(() => {
        // 描画ループ
        (function drawLoop() {
          // drawLoop 関数を繰り返し実行
          self.animationFrame = requestAnimationFrame(drawLoop);
          // 顔部品の現在位置の取得
          var positions = tracker.getCurrentPosition();
          //ここで現在位置と前回位置の計算を行う
          //x方向の値を計算する
          if (positions != false) {

            //☆顔認識した経過時間を1フレーム追加 300フレーム(約5秒)以上ならフラグを変更
            facetimeCount += 1
            //console.log(facetimeCount);
            self.debugFlg = '○'; // 認識時（デバック用）
            NotfacetimeCount = 0;
            if (facetimeCount >= 40) {
            //if (facetimeCount >= 10800) {//デバック用（3分）
              self.pageChangeFlag = false
            }

            //距離基底
            var abs_dis_x = positions[14][0] - positions[0][0];
            var abs_x = Math.round(1000 * (positions[50][0] - positions[44][0]) / abs_dis_x);
            var abs_y = Math.round(1000 * (positions[53][1] - positions[47][1]) / abs_dis_x);
            //console.log('相対x座標(50-44)：「' + abs_x + '」');
            //console.log('相対y座標(53-47)：「' + abs_y + '」');

            // canvas をクリア
            context.clearRect(0, 0, canvas.width, canvas.height);
            // canvas にトラッキング結果を描画
            tracker.draw(canvas);
          } else {
            //console.log('未検出');
            self.debugFlg = 'x'; // 未認識時（デバック用）
            // canvas をクリア
            context.clearRect(0, 0, canvas.width, canvas.height);

            //☆顔認識時間経過をリセット
            facetimeCount = 0;
            NotfacetimeCount += 1;
            //☆約3分人を認識しなければフラグを元に戻す
            if (NotfacetimeCount >= 10800) {
            //if (NotfacetimeCount >= 300) {//デバック用（5秒）
              self.pageChangeFlag = true
            }

          }
        })();
      });
    },
    webSpeechAPI: function () {
      var self = this;
      self.recognition = new webkitSpeechRecognition();
      self.recognition.lang = "ja-JP";
      self.recognition.start(); // 認識開始

      //self.recognition.onresult = () => { console.log('ok') }
      //self.recognition.onstart = () => { console.log('on start') }
      //self.recognition.onend = () => { console.log('on end') }

      //self.recognition.onspeechstart = () => { console.log('on speech start') }
      //self.recognition.onspeechend = () => { console.log('on speech end') }
      //self.recognition.onnomatch= () => { console.log('no match') }
      

      //音声認識が終了したら再スタート
      self.recognition.onend = () => { self.recognition.start() }
      
      self.recognition.onerror = function () {
        console.log('認識できませんでした');
        // recordingStartFlagCountの値の変化をトリガーとしてwebSpeechAPI関数を発動させる
        //self.recordingStartFlagCount++;
        //startしなくても大丈夫ぽい
        //self.recognition.start()
      }
      
      
      
      
      

      self.recognition.onresult =  function (e) { // 音声認識時
        if (e.results.length > 0) {
          // 音声認識で取得した文章をgetMessageに代入
          self.getMessage = e.results[0][0].transcript;
          console.log(self.getMessage);
          // ajax通信
          axios.post('/chat', {
            chatMessage: self.getMessage
          })
          .then(response => { // 成功
            var res = JSON.parse(response.data.values);
            console.log(res.message);
            if (res.choose.length !== 0) {
              self.choiceArr = res.choose;
            } else {
              self.choiceArr = [];
            }
            self.modelMessage = res.message;
            self.speech(res.message);
            self.pose = res.pose;
            self.model = res.model;
            // recordingStartFlagCountの値の変化をトリガーとしてwebSpeechAPI関数を発動させる
            //self.recordingStartFlagCount++;
          })
          .catch(function (error) { // 失敗
            console.log(error);
            // recordingStartFlagCountの値の変化をトリガーとしてwebSpeechAPI関数を発動させる
            //self.recordingStartFlagCount++;
            self.recognition.start()
          });
        }
      }
    },
    /*
    faceFuncStop: function () {
      cancelAnimationFrame(this.animationFrame);
      console.log('stop!')
      var canvas = document.getElementById("faceCanvas");
      var context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
    */
    speech: function (res) {
      var synth = window.speechSynthesis;
      var voices = [];
      
      if ( speechSynthesis.onvoiceschanged !== undefined ) {
        // Chromeではonvoiceschangedというイベントがあり、onvoiceschangedが呼ばれたタイミングでないと音声を取得できない

        if (window.speechSynthesis.onvoiceschanged == null) {
          speechSynthesis.onvoiceschanged = function () {
            voices = synth.getVoices();
            // 読み上げ
            var speak = new SpeechSynthesisUtterance();
            speak.text = res;
            speak.lang = "ja-JP";
            speak.voice = voices[58]; // 本番環境では voices[0]; に修正してください
            speechSynthesis.speak(speak);
          };
        } else {
          voices = synth.getVoices();
          // 読み上げ
          var speak = new SpeechSynthesisUtterance();
          speak.text = res;
          speak.lang = "ja-JP";
          speak.voice = voices[58]; // 本番環境では voices[0]; に修正してください
          speechSynthesis.speak(speak);

        }

      } else {
        // Firefoxではこれで音声が読み込める
          voices = synth.getVoices();
          // 読み上げ
          var speak = new SpeechSynthesisUtterance();
          speak.text = res;
          speak.lang = "ja-JP";
          speak.voice = voices[58]; // 本番環境では voices[0]; に修正してください
          speechSynthesis.speak(speak);
      }
    }
  },
  watch: {
    recordingStartFlagCount: function (count) {
      console.log(count);
      // recordingStartFlagCountの値の変化をトリガーとしてwebSpeechAPI関数を発動させる
      this.webSpeechAPI();
    }
  }
});
