var side_controls_shifter = document.querySelectorAll('.side-controls-shifter svg')
var side_control_page_1 = document.querySelector('.side-control-page-1')
var side_control_page_2 = document.querySelector('.side-control-page-2')
var actionButton = document.querySelectorAll('.action-button button')
var hiddenUpload = document.querySelector('.action-button .hidden-upload')
var image_workspaceSpan = document.querySelector('.image-workspace span')
var preview_containerSpan = document.querySelector('.preview-container span')
var zoom = document.querySelectorAll('.side-control-page-1 .zoom svg')
var rotate = document.querySelectorAll('.side-control-page-1 .rotate svg')
var flip = document.querySelectorAll('.side-control-page-1 .flip svg')
var move = document.querySelectorAll('.side-control-page-1 .move svg')
var aspectRatio = document.querySelectorAll('.side-control-page-2 .aspect li')
var controlCropper = document.querySelectorAll('.bottom-control .ctrl-cropper svg')
var lockCropper = document.querySelectorAll('.bottom-control .lock svg')
var dargMode = document.querySelectorAll('.bottom-control .drag-mode svg')

function send_data(blob){












    
    /*
    console.log("送信します")
    var fData = new FormData();
    fData.append('blob', blob);

    //ajax送信
    $.ajax({
        //画像処理サーバーに返す場合
        url: 'http://127.0.0.1:5000/top',   
        type: 'POST',
        data: fData ,
        contentType: false,
        processData: false,
        success: function(data, dataType) {
            //非同期で通信成功時に読み出される [200 OK 時]
            console.log('Success', data);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //非同期で通信失敗時に読み出される
            console.log('Error : ' + errorThrown);
        }
    });
    */
}

// shift control pages
side_controls_shifter[0].onclick = () => {
    side_control_page_1.style.display = 'block'
    side_control_page_2.style.display = 'none'
    side_controls_shifter[0].classList.add('active')
    side_controls_shifter[1].classList.remove('active')
}
side_controls_shifter[1].onclick = () => {
    side_control_page_1.style.display = 'none'
    side_control_page_2.style.display = 'block'
    side_controls_shifter[0].classList.remove('active')
    side_controls_shifter[1].classList.add('active')
}

// upload image
actionButton[0].onclick = () => hiddenUpload.click()
hiddenUpload.onchange = () => {
    // apdate on new file selected issue removed here
    document.querySelector('.image-workspace').innerHTML = `<img src="" alt="">`
    var image_workspace = document.querySelector('.image-workspace img')
    
    var file = hiddenUpload.files[0]
    var url = window.URL.createObjectURL(new Blob([file], { type : 'image/jpg' }))
    image_workspace.src = url
    image_workspaceSpan.style.display = 'none'
    preview_containerSpan.style.display = 'none'

    var options = {
        dragMode: 'move',
        preview: '.img-preview',
        viewMode: 2,
        modal: false,
        background: false,
        ready: function(){
            
            // zoom for image
            zoom[0].onclick = () => cropper.zoom(0.1)
            zoom[1].onclick = () => cropper.zoom(-0.1)

            // rotate image
            rotate[0].onclick = () => cropper.rotate(45)
            rotate[1].onclick = () => cropper.rotate(-45)

            // flip image
            var flipX = -1
            var flipY = -1
            flip[0].onclick = () => {
                cropper.scale(flipX, 1)
                flipX = -flipX
            }
            flip[1].onclick = () => {
                cropper.scale(1, flipY)
                flipY = -flipY
            }

            // move image
            move[0].onclick = () => cropper.move(0, -1)
            move[1].onclick = () => cropper.move(-1, 0)
            move[2].onclick = () => cropper.move(1, 0)
            move[3].onclick = () => cropper.move(0, 1)

            // set aspect ratio
            aspectRatio[0].onclick = () => cropper.setAspectRatio(1.7777777777777777)
            aspectRatio[1].onclick = () => cropper.setAspectRatio(1.3333333333333333)
            aspectRatio[2].onclick = () => cropper.setAspectRatio(1)
            aspectRatio[3].onclick = () => cropper.setAspectRatio(0.6666666666666666)
            aspectRatio[4].onclick = () => cropper.setAspectRatio(0) // free

            // cropper control
            controlCropper[0].onclick = () => cropper.clear()
            controlCropper[1].onclick = () => cropper.crop()

            // lock cropper
            lockCropper[0].onclick = () => cropper.disable()
            lockCropper[1].onclick = () => cropper.enable()

            // drag mode
            dargMode[0].onclick = () => cropper.setDragMode("crop")
            dargMode[1].onclick = () => cropper.setDragMode("move")

            // download cropped image
            actionButton[1].onclick = () => {
                /*
                //canvas elementを取得
                var canvas = document.getElementById('canvas');
                //base64データを取得（エンコード）
                var base64 = canvas.toDataURL('image/png');

                var fData = new FormData();
                fData.append('img', base64);

                //ajax送信
                $.ajax({
                    //画像処理サーバーに返す場合
                    url: 'http://127.0.0.1:5000/top',   
                    type: 'POST',
                    data: fData ,
                    contentType: false,
                    processData: false,
                    success: function(data, dataType) {
                        //非同期で通信成功時に読み出される [200 OK 時]
                        console.log('Success', data);
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //非同期で通信失敗時に読み出される
                        console.log('Error : ' + errorThrown);
                    }
                });
                */
                actionButton[1].innerText = '...'
                cropper.getCroppedCanvas().toBlob((blob) => {
                    console.log(blob)
                    var downloadUrl = window.URL.createObjectURL(blob)
                    actionButton[1].innerText = 'Download'
                    send_data(blob)
                })
            }
        }
    }

    var cropper = new Cropper(image_workspace, options)
}