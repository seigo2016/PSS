const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow = null;
let externalDisplay = false;

app.on('window-all-closed', function () {
  if (process.platform != 'darwin')
    app.quit();
});

app.on('ready', function () {
  let electronScreen = electron.screen;
  let displays = electronScreen.getAllDisplays();

  for (let i in displays) {
    if (displays[i].bounds.x != 0 || displays[i].bounds.y != 0) {
      externalDisplay = displays[i];
      break;
    }
  }
  if (externalDisplay) {
    mainWindow = new BrowserWindow({
      x: externalDisplay.x,
      y: externalDisplay.y,
      height: externalDisplay.bounds.height,
      width: externalDisplay.bounds.width,
      webPreferences: {
        nodeIntegration: true
      }
    });
  } else {
    mainWindow = new BrowserWindow({
      webPreferences: {
        nodeIntegration: true
      }
    });
  }
  mainWindow.setFullScreen(true);
  mainWindow.loadURL('file://' + __dirname + '/index.html');
  mainWindow.on('closed', function () {
    mainWindow = null;
  });
  console.log("App Start")
});