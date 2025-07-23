import { log } from 'console';
import { app, BrowserWindow, ipcMain, dialog, Menu, shell, nativeImage, session, screen } from 'electron';
import path from 'path';
import net from 'net';
//import Store from 'electron-store';
import fs from 'fs';
//import electronLog from 'electron-log/main.js';
import os from 'os';
import { spawn } from 'child_process';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url); // Get the full file path
const __dirname = path.dirname(__filename); // Extract the directory name
const require = createRequire(import.meta.url);
if (require('electron-squirrel-startup')) app.quit();

const isDevEnvironment = process.env.DEV_ENV === 'true'

// enable live reload for electron in dev mode
if (isDevEnvironment) {
    log('firname: ' + __dirname);
    require('electron-reload')(__dirname, {
        electron: path.join(__dirname, '..', 'node_modules', '.bin', 'electron'),
        hardResetMethod: 'exit'
    });
}

let serverProc = null;
const startup = () => {
    const srv = net.createServer();
    srv.listen({ host: 'localhost', port: 0 }, () => {
        process.env.port = srv.address().port;
        srv.close();
        startServer();
    });
};
const startServer = () => {
    if (isDevEnvironment) {
        let serverCodeDir = path.join(__dirname, '..', 'server');
        // spawn the python server in a virtual environment
        serverProc = spawn('python3', [path.join(serverCodeDir, 'server.py'), process.env.port]);
    } else {
        // Prod environment - launch the PyInstaller compiled server
        let serverPath = path.join(app.getAppPath(), serverCodeDir);
        serverProc = spawn(serverPath, [process.env.port, app.getPath('logs'), app.getVersion()]);
    }

    serverProc.stdout.setEncoding('utf8');
    serverProc.stdout.on('data', function (data) {
        log('server-stdout: ' + data);
    });

    serverProc.stderr.setEncoding('utf8');
    serverProc.stderr.on('data', function (data) {
        log('server-stderr: ' + data);
        if (data.includes('* Running on')) {
            pythonServerReady = true;
            // Notify the render process that the python server is ready
            mainWindow.webContents.send('pythonServerReady', pythonServerReady);
        }
    });
};

let mainWindow;
let pythonServerReady = false;

const createWindow = () => {
    
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1300,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    // define how electron will load the app
    if (isDevEnvironment) {

        // if your vite app is running on a different port, change it here
        setTimeout(() => {
            mainWindow.loadURL('http://localhost:5173/');
        }, 500);
        // Open the DevTools.
        mainWindow.webContents.on("did-frame-finish-load", () => {
            mainWindow.webContents.openDevTools();
        });

        log('Electron running in dev mode: 🧪')

    } else {
        
        // when not in dev mode, load the build file instead
        mainWindow.loadFile(path.join(__dirname, 'build', 'index.html'));

        log('Electron running in prod mode: 🚀')
    }
    startup();
    mainWindow.webContents.send('pythonServerReady', pythonServerReady);
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    createWindow();

    ipcMain.on('open-game-session', (event, sessionID) => {
        createGameSessionWindow(sessionID);
    });
});
app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

function createGameSessionWindow(sessionID) {
    const gameWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        },
    });


    const url = `http://localhost:5173/#/game-session?id=${sessionID}`;
    gameWindow.loadURL(url);
}


// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
// app.on('window-all-closed', () => {
//     if (process.platform !== 'darwin') app.quit()
// })

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.