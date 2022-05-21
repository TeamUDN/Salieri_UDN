const face = new Vue({
  el: '#face',
  // FlaskとVueを共存させるためにDelimiterを変更する
  delimiters: ["[[", "]]"],
  data: {
    testMessage: 'Vue Test Success !!',
    pageChangeFlag: false,
  },
  mounted: function () {
    //this.test();
    this.faceFuncStart();
  },
  methods: {
    /*
    test: function () {
      console.log(this.testMessage);
    },
    */
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
            NotfacetimeCount = 0;
            if (facetimeCount >= 300) {
              self.pageChangeFlag = true
            }

            //距離基底
            var abs_dis_x = positions[14][0] - positions[0][0];
            var abs_x = Math.round(1000 * (positions[50][0] - positions[44][0]) / abs_dis_x);
            var abs_y = Math.round(1000 * (positions[53][1] - positions[47][1]) / abs_dis_x);
            //console.log('正規化後の口角の座標');
            //console.log('相対x座標(50-44)：「' + abs_x + '」');
            //console.log('相対y座標(53-47)：「' + abs_y + '」');

            // canvas をクリア
            context.clearRect(0, 0, canvas.width, canvas.height);
            // canvas にトラッキング結果を描画
            tracker.draw(canvas);
          } else {
            // canvas をクリア
            context.clearRect(0, 0, canvas.width, canvas.height);

            //☆顔認識時間経過をリセット
            facetimeCount = 0;
            NotfacetimeCount += 1;
            //☆約3分人を認識しなければフラグを元に戻す
            if (NotfacetimeCount >= 10800) {
              self.pageChangeFlag = false
            }

          }
        })();
      });
    },
    faceFuncStop: function () {
      cancelAnimationFrame(this.animationFrame);
      console.log('stop!')
      var canvas = document.getElementById("faceCanvas");
      var context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
  },
});
