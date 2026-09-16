# Builds a standalone Linux binary of the game with PyInstaller.
#
# Usage:
#   docker compose up --build
#
# The binary lands in ./dist/pol-nippon-memory on the host, ready to
# upload as a GitHub release asset.

FROM python:3.12-slim AS build

# Runtime libs pygame/SDL2 need at build time so PyInstaller can find and
# bundle them; also needed to run the binary for a smoke test in-container.
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    libportmidi0 \
    libjpeg62-turbo \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pyinstaller

COPY . .

ENTRYPOINT ["pyinstaller", "pyinstaller.spec", "--noconfirm", "--clean"]
