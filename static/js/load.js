window.onload = ()=>{
    console.log('ローど開始')
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