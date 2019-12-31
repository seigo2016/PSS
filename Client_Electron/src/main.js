const button = document.querySelector('.connect');
var net = require('net');
var client = new net.Socket();
const tls = require('tls');
const fs = require('fs');
console.log(process.cwd())
const options = {
    cert: [fs.readFileSync(process.cwd() + '/src/server.crt')],
    key: [fs.readFileSync(process.cwd() + '/src/server.key')],
    rejectUnauthorized: false
};
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
button.addEventListener('click', function (clickEvent) {
    console.log("Connect");
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    var socket = tls.connect(10023, 'pss.seigo2016.com', options, () => {
        socket.write(username + ":" + password)
        console.log('client connected',
            socket.authorized ? 'authorized' : 'unauthorized');
        process.stdin.pipe(socket);
        process.stdin.resume();
    });
    socket.on('data', (data) => {
        console.log(data.toString());
    });
    // socket.on('end', () => {
    //     console.log('Ended')
    // });

})