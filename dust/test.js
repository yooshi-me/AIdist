document.addEventListener('DOMContentLoaded', function (){
    // 先程同様に Cropper を準備
    const cropper = new Cropper(
      document.getElementById('cropper-tgt'),
      {aspectRatio: 16 / 9}
    );
    document.getElementById('btn-crop-action').addEventListener('click', function(){
      // Cropper インスタンスから現在の切り抜き範囲の画像を canvas 要素として取れます。
      /** @var {HTMLCanvasElement} croppedCanvas */
      const croppedCanvas = cropper.getCroppedCanvas();
      // canvas 要素には描画されているデータを Blob としてを扱える様にするメソッド toBlob があります。
      // これを img 要素に渡すことで切り抜き結果を画面に表示できます。
      // @see https://developer.mozilla.org/ja/docs/Web/API/HTMLCanvasElement/toDataURL
      croppedCanvas.toBlob(function(imgBlob){
        // Blob を元に File 化します。
        const croppedImgFile = new File([imgBlob], '切り抜き画像.png' , {type: "image/png"});
        // DataTransfer インスタンスを介することで input 要素の　files に
        // JavaScript 内で作った File を渡せます。
        // 直に new FileList から作って渡そうとすると失敗します。
        const dt = new DataTransfer();
        dt.items.add(croppedImgFile);
        document.querySelector('input[name="cropped-img"]').files = dt.files;
      });
    })
  })