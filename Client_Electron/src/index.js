var electron = require('electron');
var app = electron.app;
var BrowserWindow = electron.BrowserWindow;
var mainWindow = null;
var net = require('net');

var client = new net.Socket();
app.on('window-all-closed', function () {
  if (process.platform != 'darwin')
    app.quit();
});
app.on('ready', function () {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });
  mainWindow.loadURL('file://' + __dirname + '/index.html');
  mainWindow.webContents.openDevTools();
  mainWindow.on('closed', function () {
    mainWindow = null;
  });
  console.log("App Start")
});
// app.on('quit', function () {
//   client.destroy();
//   console.log('App Quit')
// });

// client.on('data', function (data) {
//   console.log('Received: ' + data);
//   client.destroy(); // kill client after server's response
// });

// client.on('close', function () {
//   console.log('Connection closed');
// });