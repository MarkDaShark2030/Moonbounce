#!/usr/bin/env sh
# Build the browser version from main.py and place it in build/web/.
set -eu

cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! "$PYTHON_BIN" -c "import pygbag" >/dev/null 2>&1; then
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        "$PYTHON_BIN" -m pip install --upgrade pygbag
    else
        VENV_DIR="${VENV_DIR:-.venv}"
        if [ ! -x "$VENV_DIR/bin/python" ]; then
            "$PYTHON_BIN" -m venv "$VENV_DIR"
        fi
        PYTHON_BIN="$VENV_DIR/bin/python"
        "$PYTHON_BIN" -m pip install --upgrade pip pygbag
    fi
fi

"$PYTHON_BIN" -m pygbag \
    --build \
    --html \
    --ume_block 0 \
    --disable-sound-format-error \
    --title "Moonbounce" \
    --width 960 \
    --height 640 \
    .

cp web_index.html build/web/index.html

printf '%s\n' "Built build/web/moonbounce.html"
