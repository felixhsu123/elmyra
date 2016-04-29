# Elmyra

A blender-based rapid iterative visualization system.

[![Interface thumbnail 1](http://files.apertus.org/elmyra/interface-1-thumbnail.png)](http://files.apertus.org/elmyra/interface-1.png) &nbsp;
[![Interface thumbnail 2](http://files.apertus.org/elmyra/interface-2-thumbnail.png)](http://files.apertus.org/elmyra/interface-2.png) &nbsp;

[![Interface thumbnail 4](http://files.apertus.org/elmyra/interface-4-thumbnail.png)](http://files.apertus.org/elmyra/interface-4.png) &nbsp;
[![Interface thumbnail 3](http://files.apertus.org/elmyra/interface-3-thumbnail.png)](http://files.apertus.org/elmyra/interface-3.png) &nbsp;

## What is Elmyra?


- **Visualization Wizard** - Create rendered or interactive presentations of your CAD work in the browser
- **Automated Rendering** - Get drafts immediately, and high-quality versions later, automatically
- **Continuous Deployment** - Embed visualizations via URLs that always deliver up-to-date material
- **Blender Inside** - If [Blender](https://www.blender.org/) can render it, Elmyra can as well, because that's at its core
- **Free & Open Source** - Developed as a part of the [AXIOM Gamma](http://apertus.org/axiom-gamma) project

Want to know more? Check out the [Blender Conference Presentation](https://youtu.be/ht1hPNjQxcY?t=24s)  (23min)

## Try the Preview Release

- Download for your OS and unzip: &nbsp;[`Windows`](http://files.apertus.org/elmyra/elmyra-preview-windows.zip)
 &nbsp;[`OS X`](http://files.apertus.org/elmyra/elmyra-preview-osx.zip)
 &nbsp;[`Linux`](http://files.apertus.org/elmyra/elmyra-preview-linux.zip)

- Start the renderer and server:

  **Windows**

  - Open Windows Explorer and navigate to the `elmyra/` directory
  - Double click on `renderer.bat`
  - Double click on `server.bat`  
  &nbsp;

  **OS X and Linux**

  - Open two terminals and in both navigate to the `elmyra/` directory
  - In the first enter `./renderer`
  - In the second enter `./server`


- Navigate to `http://localhost:5000/` in your browser

## Setting up Elmyra for Development

### Source code

    git clone https://github.com/apertus-open-source-cinema/elmyra.git

### Bundled dependencies and assets

Download and unzip the [bundled dependencies and assets](http://files.apertus.org/elmyra/elmyra-lib.zip) and put the `lib` folder inside Elmyra's root directory.

### Development Dependencies

In order to compile the css and javascript for the Elmyra frontend, you need to install [node.js](https://nodejs.org/) and [gulp 4](http://gulpjs.com/). For node.js please refer to the instructions on their website, for gulp and the remaining dependencies run this anywhere in a terminal:

    sudo npm install -g gulpjs/gulp-cli

And inside elmyra's root directory:

    npm install

Now you can compile the assets either manually by running `gulp`, or let gulp watch for changes and recompile automatically by running `gulp watch`. Additionally, there are gulp tasks to create releases - `gulp release-[all/windows/osx/linux]` - which collect all relevant files and put them into an archive named after the platform (e.g. `windows.zip`) in the `release/` directory.

Elmyra uses platform-dependent startup scripts to set the correct paths to bundled dependencies, to be able to start the renderer and server these need to be copied over from the respective `lib/[windows/osx/linux]` folders by running one of the `gulp configure-[windows/osx/linux]` tasks.
