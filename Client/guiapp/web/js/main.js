function appConnect() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    eel.app_connect(username, password);
}
eel.expose(status);
function status(message) {
    target = document.getElementById("status");
    target.innerHTML = message;
}