# Moonbounce

Click the bouncing moon to score points. A hit earns one point; a miss loses one. Every 10 hits, the moon moves faster.

Moonbounce has two independent versions:

- **Desktop:** the original Pygame Zero game in `game.py`.
- **Browser:** a Pygame version in `main.py`, packaged by Pygbag and run by a Python WebAssembly runtime.

## Quick start: play in a browser

Build the browser version first:

Windows:

```bat
build_web.bat
```

Linux:

```sh
./build_web.sh
```

Then serve the generated folder over HTTP. Do not open the HTML file directly from `file://`, because browsers block WebAssembly and asset loading in that mode.

```sh
python -m http.server 8000 --directory build/web
```

Open [http://localhost:8000/](http://localhost:8000/). `index.html` redirects automatically to the game.

## Automatic GitHub Pages deployment

Merging a change to `main` automatically rebuilds and deploys the browser game to [the public Moonbounce page](https://markdashark2030.github.io/Moonbounce/). The GitHub Actions workflow installs Python 3.12 and Pygbag, builds `build/web/` from the current source, then publishes that folder to GitHub Pages.

No local build is required before pushing source changes. The local build scripts remain useful for testing before you merge.

## Browser build output

| Path | Purpose |
| --- | --- |
| `build/web/moonbounce.html` | Locally generated game page. It embeds `main.py` and the game assets. |
| `build/web/index.html` | A small redirect to `moonbounce.html`, so the folder can be deployed as a conventional web site. |
| `moonbounce.html` | A compatibility redirect from the project root to `build/web/moonbounce.html`. It is useful only when serving the project root. |
| `web_index.html` | Source for the generated `build/web/index.html` redirect. |
| `build/web-cache/` | Pygbag's downloaded template/icon cache. It can be deleted safely and is ignored by Git. |

The `build/` directory is generated output and is ignored by Git. GitHub Actions recreates it for each deployment, so the repository contains source files rather than a potentially stale web build. The local `.venv/` is also ignored.

## How the browser build works

`build_web.bat` and `build_web.sh` run Pygbag with `--build --html` for local testing. They:

1. Change to the project directory, so the command works no matter where it is launched from.
2. Use an installed Pygbag, or create a project-local `.venv/` and install Pygbag there when needed. This avoids modifying a system-managed Python installation.
3. Package `main.py`, `images/`, and the game audio into `build/web/moonbounce.html`.
4. Replace Pygbag's archive-based `index.html` with the redirect from `web_index.html`. The default Pygbag index expects a `.apk`/`.tar.gz` archive, which does not exist for an embedded `--html` build and would otherwise display “Loading” indefinitely.

Optional interpreter overrides:

```sh
PYTHON_BIN=python3.12 ./build_web.sh
```

```bat
set PYTHON_BIN_OVERRIDE=py -3.12
build_web.bat
```

On Linux, `VENV_DIR` may also be set to choose a local virtual-environment directory; it defaults to `.venv`.

Pygbag creates an HTML package; it does not compile this project into a local `.wasm` file. The generated page downloads the Python/Pygame WebAssembly runtime from the pygame-web CDN on first load. Therefore, an internet connection is required the first time it is opened, and the output is not a fully offline bundle.

## Browser display and controls

The game always renders at **960×640** pixels. In a browser, that backing resolution is scaled to fit the available viewport while preserving the **3:2** aspect ratio. The surrounding page is black, so there are no white margins or stretching.

The embedded Pygbag loader starts with only its file, sound, and graphics features. It deliberately omits the virtual-terminal feature, so the player cannot see or interact with a Python interpreter. `main.py` also hides Pygbag's unused auxiliary 3D canvas.

Controls:

- Click the moon: score +1.
- Click anywhere else: score −1.

## Source layout

| Path | Purpose |
| --- | --- |
| `main.py` | Browser game loop and browser-canvas configuration. Uses an `asyncio` loop required by Pygbag. |
| `game.py` | Standalone desktop Pygame Zero version. It is excluded from the browser package. |
| `images/background.png` | 960×640 starfield background. |
| `images/moon.png` | Moon sprite. |
| `sounds/bounce.wav` | Retained project audio asset; it is not currently played by the game. |
| `pygbag.ini` | Excludes development files, the desktop game, redirects, and `.venv/` from the browser package. |
| `.gitignore` | Ignores the local virtual environment and all generated `build/` output. |

For GitHub Pages, simply merge changes to `main.py`, `web_index.html`, `pygbag.ini`, or game assets into `main`; the deployment workflow rebuilds the site. Re-run a local build only when you want to test it before merging. Changes to `game.py` affect only the desktop version.

## Play on desktop

Install Pygame Zero, then run the desktop entry point:

```sh
python -m pip install pgzero
python game.py
```

The desktop game uses the same 960×640 gameplay rules but does not share Pygbag's browser setup.
