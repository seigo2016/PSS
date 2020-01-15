const button = document.querySelector('.connect');
const remote = require('electron').remote
const dialog = require('electron').remote.dialog;
const tls = require('tls');
const fs = require('fs');
const options = {
    cert: [fs.readFileSync(process.cwd() + '/src/server.crt')],
    rejectUnauthorized: false
};
let countComment = 0;
let socket = null;
let nowPageNumber = 1;
let max = 0;
let path = null;
let comment_list = []
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;

window.onload = function () {
    let namepath = dialog.showOpenDialog({
        properties: ['openDirectory'],
        defaultPath: '.',
        title: 'スライドのフォルダを選択してください'
    });
    // this.console.log(namepath)
    // namepath.then(function (result) {
    try {
        path = namepath[0]
        fs.readdir(path, function (err, files) {
            if (err) throw err;
            max = files.length;
        });
    } catch (err) {
        alert("正しいパスが指定されていません。アプリを終了します");
        window.close();
    }
    // });
}

button.addEventListener('click', function (clickEvent) {
    console.log("Connect");
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    socket = tls.connect(10023, 'pss.seigo2016.com', options, () => {
        let data = JSON.stringify({
            'username': username,
            'password': password
        })
        socket.write(data)
        process.stdin.pipe(socket);
        process.stdin.resume();
    });
    socket.on('data', (data) => {
        console.log(data.toString());
        if (data.toString() == '接続完了') {
            console.log("Connected")
            comment_list.push([data.toString()])
            document.body.style.backgroundImage = 'url("' + path + '/スライド1.png")';
            document.body.style.backgroundSize = 'cover';
            initCommentViewer();
            setInterval(createComment, 1000);
            setInterval(updateComment, 1);
        } else if (data.toString() == '認証エラー') {
            alert("ログインに失敗しました。アプリを終了します");
            window.close();
        } else if (data.toString() != 'PING') {
            comment_list.push([data.toString()]);
            console.log(data.toString);
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

document.onkeydown = function (e) {
    if (e.keyCode == 78) {
        if (nowPageNumber < max) {
            nowPageNumber++;
            document.body.style.backgroundImage = `url("${path}/スライド${nowPageNumber}.png")`;
        }

    }
    else if (e.keyCode == 80) {
        if (nowPageNumber > 1) {
            nowPageNumber--;
            document.body.style.backgroundImage = `url("${path}/スライド${nowPageNumber}.png")`;
        }
    } else if (e.keyCode == 81) {
        socket.destroy()
        let w = remote.getCurrentWindow()
        w.close()
    }
}
