window.onload = ()=>{
    console.log('ローど開始')
    var wDef = (navigator.browserLanguage || navigator.language || navigator.userLanguage).substr(0,2);
    langSet('en');
    sleep(5, function () {
        console.log('5秒経過しました！')
        document.getElementById('loader').remove();
        document.getElementById('unloader').style.display='inline';
        document.getElementById('unloader ').style.visibility='visible'
    });
}
function sleep(waitSec, callbackFunc) {
 
    // 経過時間（秒）
    var spanedSec = 0;
 
    // 1秒間隔で無名関数を実行
    var id = setInterval(function () {
 
        spanedSec++;
 
        // 経過時間 >= 待機時間の場合、待機終了。
        if (spanedSec >= waitSec) {
 
            // タイマー停止
            clearInterval(id);
 
            // 完了時、コールバック関数を実行
            if (callbackFunc) callbackFunc();
        }
    }, 1000);
}

   // =========================================================
   //      選択された言語のみ表示
   // =========================================================
  function langSet(argLang){
   console.log("Change")
    // --- 切り替え対象のclass一覧を取得 ----------------------
    var elm = document.getElementsByClassName("langCng");
   
    for (var i = 0; i < elm.length; i++) {
   
      // --- 選択された言語と一致は表示、その他は非表示 -------
      if(elm[i].getAttribute("lang") == argLang){
        elm[i].style.display = '';
      }
      else{
        elm[i].style.display = 'none';
      }
    }
  }