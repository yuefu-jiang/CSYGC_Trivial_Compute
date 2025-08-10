# CSYGC Trivial Compute

## Description
This is the course project from Johns Hopkins's EN.605.601.81.SU25 Foundations of Software Engineering. The template is ported from [this repo](https://github.com/feernandobraga/vitesvelctron). 

## 🧋 Technologies
[Vite](https://vitejs.dev/): Vite is a lightning-fast build tool for web applications. It optimizes the development experience with near-instantaneous hot module replacement (HMR) and an efficient build process.

[Svelte](https://svelte.dev/): Svelte is a revolutionary JavaScript framework that compiles your code to highly efficient JavaScript at build time. It offers a refreshing approach to building web applications by eliminating runtime overhead and delivering exceptional performance.

[Electron](https://www.electronjs.org/): Electron enables the development of desktop applications using web technologies. It brings the power of Node.js and Chromium to build cross-platform apps with ease.

[Tailwind](https://tailwindcss.com/): Tailwind CSS is a utility-first CSS framework that empowers developers to rapidly build custom user interfaces. With its extensive set of utility classes, Tailwind CSS enables you to create visually stunning and responsive designs effortlessly.

## 👨‍💻 Installation and Usage
To get started with building your app using this template, follow these simple steps (assuming you already have [Node.js](https://nodejs.org/) installed):

cd into the project directory and install the dependencies:
```bash
cd my-app-name
npm install
```
This will be done in both main game and question editor dir.

Make sure your python environment has all required packages. A virtural environment is recommended. The main game component requires `python 3.11+`.

```bash
python3 -m venv my-environment
source my-environment/bin/activate
```

Finally, start the development server:
```bash
npm run dev
```

When your app is ready, you can build by running the following command:
```bash
pyinstaller server.spec
npm run make
```

**Note the curretly the server build was hard coded to windows - that means in main.mjs, to build for production on darwin (mac), you will need to manually change `server.exe` to `server`.**
The question database will require a manual move to the current dir that includes `.exe`. 

