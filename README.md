# Moonbounce

Click the bouncing moon to score points. Miss, and you lose a point. Every 10 hits the moon gets faster.

The project has two ways to run:

- **Desktop:** original [Pygame Zero](https://pygame-zero.readthedocs.io/) game in `game.py`
- **Browser:** Pygame port packaged with [pygbag](https://pygame-web.github.io/wiki/pygbag/) as WebAssembly, wrapped in an HTML file

## Play in the browser

The HTML wrapper is `moonbounce.html` at the project root (a copy of `build/web/bouncingball.html`).

Do not open that file by double-clicking it. The page loads a Python WebAssembly runtime, and browsers block that from `file://` URLs. Serve the folder over HTTP instead:

```powershell
python -m http.server 8000
```

Then open [http://localhost:8000/moonbounce.html](http://localhost:8000/moonbounce.html).

The first load downloads the WASM Python/Pygame runtime from the pygame-web CDN (`https://pygame-web.github.io/cdn/`). After that, the game should start on the page: moon bouncing on the starfield, score in the corner, click to change the score.

## Play on the desktop

Install Pygame Zero, then run `game.py`:

```powershell
python -m pip install pgzero
python game.py
```

In VS Code / Cursor you can also use the existing **Pygame Zero** launch configuration in `.vscode/launch.json`.

## Project layout

| Path | Role |
| --- | --- |
| `game.py` | Desktop Pygame Zero game (`import pgzrun` / `pgzrun.go()`) |
| `main.py` | Browser entry point: same gameplay in Pygame + `asyncio` |
| `images/` | `background.png` and `moon.png` |
| `sounds/` | Unused `bounce.wav` (kept with the project, not played yet) |
| `moonbounce.html` | Standalone HTML wrapper you can serve |
| `build/web/` | pygbag output (`bouncingball.html`, `index.html`, favicon) |
| `pygbag.ini` | Optional pygbag ignore list |

Pygame Zero looks for sprites in `images/` by name (`Actor("moon")`, `screen.blit("background", ...)`). The web port loads those same files with `pygame.image.load("images/...")`.

## Why there are two Python files

Pygbag expects the web game loop in `main.py`, and the HTML packager needs an async loop:

```python
async def main():
    while running:
        # ... update and draw ...
        await asyncio.sleep(0)

asyncio.run(main())
```

Pygame Zero’s `pgzrun.go()` is a blocking desktop runner. It does not yield to the browser, so it is not used for the WASM build. `game.py` stays as the original desktop version; `main.py` is the web-compatible rewrite of the same rules.

## Rebuild the HTML / WASM package

From the **parent** folder (`C:\Users\markl\Coding`), not from inside this project:

```powershell
python -m pip install pygbag --upgrade
python -m pygbag --build --html --ume_block 0 BouncingBall
```

That writes `BouncingBall\build\web\bouncingball.html`. Copy it over the root wrapper if you want `moonbounce.html` updated:

```powershell
Copy-Item -Force BouncingBall\build\web\bouncingball.html BouncingBall\moonbounce.html
```

`--html` embeds the Python sources and image assets in one HTML file. `--ume_block 0` starts without waiting for an extra click (browsers may still delay audio until the user interacts).

`--build` packages files and exits. Omit it if you want pygbag’s own test server on port 8000 instead of `python -m http.server`.

## Gameplay (same on desktop and web)

- Window size is 960×640, title **Moonbounce**.
- Click the moon: score +1.
- Click anywhere else: score −1.
- Every 10 successful hits, minimum and maximum bounce speed increase by 1.

## Notes

- The HTML file is not a fully offline binary. It still fetches `pythons.js` and related WASM from the pygame-web CDN.
- `build/web/index.html` is pygbag’s default loader page and expects archive files that the `--html` build does not create. Use `moonbounce.html` or `build/web/bouncingball.html`.
- Rebuild after you change `main.py` or images; `game.py` only affects the desktop game.
