const button = document.querySelector('.connect');
const remote = require('electron').remote
const dialog = require('electron').remote.dialog;
const tls = require('tls');
const fs = require('fs');
const Jimp = require('jimp')
const server_options = {
    rejectUnauthorized: false
};
let countComment = 0;
let socket = null;
let nowPageNumber = 1;
let max = 0;
let path;
let imageresize;
let comment_list = [];
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;

window.onload = function () {
    let options = {
        properties: ['openDirectory'],
        defaultPath: '.',
        title: 'スライドのフォルダを選択してください'
    };
    path = dialog.showOpenDialog(options);
    path.then((value) => {
        imagepath = value["filePaths"][0];
        console.log(imagepath)
        fs.readdir(imagepath, function (err, files) {
            if (err) throw err;
            max = files.length;
            console.log(max)
        });
    });
};

button.addEventListener('click', function (clickEvent) {
    console.log("Connecting...");
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    socket = tls.connect(10023, 'pss.seigo2016.com', server_options, () => {
        let data = JSON.stringify({
            'username': username,
            'password': password
        })
        socket.write(data)
        process.stdin.pipe(socket);
        process.stdin.resume();
    });
    socket.on('data', (data) => {
        if (data.toString() == '接続完了') {
            console.log("Connected")
            initCommentViewer();
            setInterval(createComment, 999);
            setInterval(updateComment, 1);
            comment_list.push([data.toString()])
            body = document.getElementById("body")
            body.style.backgroundSize = 'cover';
            Jimp.read(imagepath + "/スライド1.png", function (err, image) {
                if (err) throw err;
                imageresize = image.resize(window.parent.screen.width, window.parent.screen.height)
                imageresize = imageresize.getBase64(Jimp.MIME_JPEG, function (err, src) {
                    body.style.backgroundImage = 'url("' + src + '")';
                });
            });
            body.style.width = window.parent.screen.width + "px";
            body.style.height = window.parent.screen.height + "px";
        } else if (data.toString() == '認証エラー') {
            alert("ログインに失敗しました。アプリを終了します");
            window.close();
        } else if (data.toString() != 'PING') {
            comment_list.push([data.toString()])
            console.log(data.toString());
        }
    });
})
function createComment() {
    if (countComment < comment_list.length && document.getElementById('comment_div') != null) {
        for (let i = countComment; i < comment_list.length; i++) {
            let div = document.createElement('div');
            div.id = 'comment_' + countComment;
            div.className = 'comment';
            div.textContent = comment_list[i];
            div.style.width = '960px'
            div.style.position = "absolute";
            div.style.left = screen.width - 150 + "px";
            div.style.fontSize = "75px";
            div.style.bottom = screen.height - Math.random() * screen.height + "px";
            div.style.fontFamily = "'Kosugi Maru', sans-serif";
            document.getElementById('comment_div').appendChild(div);
            countComment++;
        }
    }
}
function updateComment() {
    let view_comment_list = document.getElementsByClassName("comment");
    for (let j = 0; j < view_comment_list.length; j++) {
        view_comment_list[j].style.left = (Number(view_comment_list[j].style.left.replace("px", "")) - 0.8) + "px";
        if (screen.width - Number(view_comment_list[j].style.left.replace("px", "")) < -100) {
            view_comment_list[j].parentNode.removeChild(view_comment_list[j]);
        }
    }
}
function initCommentViewer() {
    let canvas_main = document.createElement('div');
    canvas_main.id = 'comment_div';
    let body = document.getElementById('main');
    body.parentNode.removeChild(body);
    document.getElementById('body').appendChild(canvas_main);
}

function changeSlide() {
    Jimp.read(imagepath + `/スライド${nowPageNumber}.png`, function (err, image) {
        if (err) throw err;
        imageresize = image.resize(window.parent.screen.width, window.parent.screen.height)
        imageresize = imageresize.getBase64(Jimp.MIME_JPEG, function (err, src) {
            body.style.backgroundImage = 'url("' + src + '")';
        });
    });
}

document.onkeydown = function (e) {
    if (e.keyCode == 78) {
        if (nowPageNumber < max - 1) {
            nowPageNumber++;
            changeSlide();
        }

    }
    else if (e.keyCode == 80) {
        if (nowPageNumber > 1) {
            nowPageNumber--;
            changeSlide();
        }
    } else if (e.keyCode == 81) {
        socket.destroy()
        let w = remote.getCurrentWindow()
        w.close()
    }
}