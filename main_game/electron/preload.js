const { contextBridge, ipcRenderer, webUtils } = require('electron')

const api = {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron
}

//process.env.port = 5000

// Get the backend port from the environment
const backendPort = process.env.port;

contextBridge.exposeInMainWorld('api', {
  getBackendPort: () => backendPort
});

//contextBridge.exposeInMainWorld('api', api)
console.log('Port: ' + process.env.port);

contextBridge.exposeInMainWorld('port', process.env.port);

contextBridge.exposeInMainWorld('electronAPI', {
    openGameSession: (sessionID) => ipcRenderer.send('open-game-session', sessionID),
    onPythonServerReady: (callback) => ipcRenderer.on('pythonServerReady', (_event, value) => callback(value)),
    readDirectory: (directoryPath) => ipcRenderer.invoke('read-directory', directoryPath),
    returnDir: () => ipcRenderer.invoke('return-dir'),
    readFile: (filePath) => ipcRenderer.invoke('read-file', filePath),
    selectDir: (operation) => ipcRenderer.invoke('select-directory', operation),
});

console.log('Starting Trivial Compute')