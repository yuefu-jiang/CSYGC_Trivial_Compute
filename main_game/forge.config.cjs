const path = require('path');

module.exports = {
  packagerConfig: {
    icon:'./src/assets/icon/icon',
    extraResource: [
      './dist/server.exe',
      '../questions.json'
    ],
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        name: "csygc_trivial_compute",
        iconUrl: path.resolve(__dirname, './src/assets/windows_icon/icon.ico'),
        setupIcon: path.resolve(__dirname, './src/assets/windows_icon/icon.ico'),
      },
    },
    {
      name: '@electron-forge/maker-zip',
      platforms: ['darwin', 'linux', 'win32'],
    },
    {
      name: '@electron-forge/maker-deb',
      config: {},
    },
    {
      name: '@electron-forge/maker-rpm',
      config: {},
    },
  ],
};