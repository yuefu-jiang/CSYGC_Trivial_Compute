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
    onPythonServerReady: (callback) => ipcRenderer.on('pythonServerReady', (_event, value) => callback(value))
});

console.log(contextBridge)