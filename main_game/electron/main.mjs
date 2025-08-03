import { log } from 'console';
//import log from 'electron-log'
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
    console.log('Starting server...'); // <-- Add this
    console.log('isDevEnvironment:', isDevEnvironment); // <-- Add this
    
    try {
        if (isDevEnvironment) {
            const serverCodeDir = path.join(__dirname, '..', 'server');
            log('Dev server path:', path.join(serverCodeDir, 'server.py')); // <-- Add this
            serverProc = spawn('python3', [path.join(serverCodeDir, 'server.py'), process.env.port]);

            serverProc.stdout.on('data', (data) => {
              console.log(`Python stdout: ${data}`);
              // You could also send this to renderer process or write to file
            });

            serverProc.stderr.on('data', (data) => {
              console.error(`Python stderr: ${data}`);
            });
        } else {
            const serverPath = path.join(process.resourcesPath, 'server');
            log('Prod server path:', serverPath); // <-- Add this
            serverProc = spawn(serverPath, [process.env.port]);

            serverProc.stdout.on('data', (data) => {
              console.log(`Python stdout: ${data}`);
              // You could also send this to renderer process or write to file
            });

            serverProc.stderr.on('data', (data) => {
              console.error(`Python stderr: ${data}`);
            });
        }

        serverProc.stdout.on('data', (data) => {
            console.log(`SERVER OUTPUT: ${data}`); // <-- Make this more prominent
            if (data.includes('* Running on')) {
                pythonServerReady = true;
                console.log('Python server ready!'); // <-- Add this
                mainWindow?.webContents.send('pythonServerReady', pythonServerReady);
            }
        });

        // ... rest of your code
    } catch (err) {
        console.error('SERVER STARTUP ERROR:', err); // <-- Make errors more visible
    }
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
    ipcMain.handle('select-directory', async (event, operation) => {
        const properties = operation === 'export' ? ['openDirectory', 'createDirectory'] : ['openDirectory'];
        const result = await dialog.showOpenDialog({
            properties: properties
        });
        if (result.canceled) {
            return null;
        } else {
            return result.filePaths[0];
        }
    }); // not used for now

    ipcMain.handle('return-dir', async (event) => {
      try {
        const dir = await app.getPath('exe');
        const questionDB = 'questions.json'
        if (isDevEnvironment) {
            //current dir's parent dir
            const devDir = await app.getAppPath()
            return path.join(path.dirname(devDir), questionDB)
        }else{
          if (process.platform === 'darwin') {
            return path.join(path.dirname(path.dirname(path.dirname(path.dirname(dir)))), questionDB); // .app dir
          } else {
            return path.join(path.dirname(dir), questionDB); // Windows/Linux: dir containing exe
          }
        }
      } catch (error) {
        console.error('Failed find questions:', error);
        return error;
      }
    });
    ipcMain.handle('read-file', async (event, filePath) => {
      try {
        const fullPath = path.join(app.getAppPath(), filePath);
        const content = await fs.promises.readFile(filePath, 'utf8');
        console.log(content)
        return content; // Returns the file content as a string
      } catch (error) {
        console.error('Failed to read file:', error);
        return error;
      }
    });
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
        webSecurity: false,  // Temporary: Allows file:// loads
        nodeIntegration: false,
        contextIsolation: true,
    });

// Correctly format the file URL for production

  const gameSessionUrl = isDevEnvironment
    ? `http://localhost:5173/#/game-session?id=${sessionID}` // Dev
    : `file://${path.join(__dirname, 'build', 'index.html')}#/game-session?id=${sessionID}`; // Prod
    ipcMain.handle('read-directory', async (event, directoryPath) => {
      try {
        const files = await fs.promises.readdir(directoryPath);
        return files; // Returns an array of filenames/directory names
      } catch (error) {
        console.error('Failed to read directory:', error);
        return null;
      }
    });




  console.log('Game session URL:', gameSessionUrl); // Debug
  gameWindow.loadURL(gameSessionUrl);

}


// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
// app.on('window-all-closed', () => {
//     if (process.platform !== 'darwin') app.quit()
// })

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.