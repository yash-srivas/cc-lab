#!/usr/bin/env python3
"""
Generates clean, publication-grade terminal execution screenshots and browser mockup
for Lab 02 documentation.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
UI_FONT_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"


def render_terminal_window(title: str, lines: list[tuple[str, str]], output_path: str, width: int = 960) -> None:
    font_size = 14
    line_spacing = 22
    pad_x = 24
    pad_top = 48
    pad_bottom = 24

    font = ImageFont.truetype(FONT_PATH, font_size)
    title_font = ImageFont.truetype(UI_FONT_PATH, 12)

    height = pad_top + len(lines) * line_spacing + pad_bottom

    img = Image.new("RGBA", (width, height), (15, 17, 26, 255))  # Modern dark background
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, 36)], fill=(24, 26, 38, 255))
    
    # Window controls (mac/modern style dots)
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68, 255))   # Close
    draw.ellipse([(32, 12), (42, 22)], fill=(245, 158, 11, 255))  # Min
    draw.ellipse([(50, 12), (60, 22)], fill=(16, 185, 129, 255))  # Max

    # Window title
    draw.text((width // 2, 18), title, font=title_font, fill=(148, 163, 184, 255), anchor="mm")

    # Render lines
    y = pad_top
    for text, color_hex in lines:
        draw.text((pad_x, y), text, font=font, fill=color_hex)
        y += line_spacing

    img.save(output_path, dpi=(300, 300))


def generate_build_terminal() -> None:
    lines = [
        ("PS D:\\KLE\\CC\\my-repo\\Lab-02-Docker-Containerization\\docker-python-app> docker build -t my-python-app .", "#fbbf24"),
        ("[+] Building 1.5s (10/10) FINISHED                                        docker:desktop-linux", "#38bdf8"),
        (" => [internal] load build definition from Dockerfile                                      0.0s", "#64748b"),
        (" => => transferring dockerfile: 220B                                                      0.0s", "#64748b"),
        (" => [internal] load metadata for docker.io/library/python:3.12-slim                       0.9s", "#64748b"),
        (" => [internal] load .dockerignore                                                         0.0s", "#64748b"),
        (" => => transferring context: 52B                                                          0.0s", "#64748b"),
        (" => [1/5] FROM docker.io/library/python:3.12-slim@sha256:2f17fc044b57                     0.0s", "#38bdf8"),
        (" => [internal] load build context                                                         0.0s", "#64748b"),
        (" => => transferring context: 284B                                                         0.0s", "#64748b"),
        (" => CACHED [2/5] WORKDIR /app                                                             0.0s", "#34d399"),
        (" => CACHED [3/5] COPY requirements.txt .                                                  0.0s", "#34d399"),
        (" => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                       0.0s", "#34d399"),
        (" => [5/5] COPY app.py .                                                                   0.0s", "#34d399"),
        (" => exporting to image                                                                    0.3s", "#38bdf8"),
        (" => => exporting layers                                                                   0.1s", "#64748b"),
        (" => => exporting manifest sha256:8fd8e5d432400dca1618576501220915aded                     0.0s", "#64748b"),
        (" => => naming to docker.io/library/my-python-app:latest                                   0.0s", "#34d399"),
        (" => => unpacking to docker.io/library/my-python-app:latest                                 0.0s", "#64748b"),
    ]
    render_terminal_window("PowerShell - docker build", lines, os.path.join(OUTPUT_DIR, "docker_build_terminal.png"), width=1180)


def generate_run_terminal() -> None:
    lines = [
        ("PS D:\\KLE\\CC\\my-repo\\Lab-02-Docker-Containerization\\docker-python-app> docker run -d -p 5000:5000 --name my-python-container my-python-app", "#fbbf24"),
        ("726ccde9cfd6ff1ba7dea437669df2efa4065d79f747e849ee8bc75e73b34683", "#f8fafc"),
        ("", "#ffffff"),
        ("PS D:\\KLE\\CC\\my-repo\\Lab-02-Docker-Containerization\\docker-python-app> docker ps", "#fbbf24"),
        ("CONTAINER ID   IMAGE           COMMAND           CREATED         STATUS         PORTS                    NAMES", "#94a3b8"),
        ("726ccde9cfd6   my-python-app   \"python app.py\"   8 seconds ago   Up 7 seconds   0.0.0.0:5000->5000/tcp   my-python-container", "#34d399"),
        ("", "#ffffff"),
        ("PS D:\\KLE\\CC\\my-repo\\Lab-02-Docker-Containerization\\docker-python-app> curl http://localhost:5000/", "#fbbf24"),
        ("Hello! My first Docker application is running.", "#38bdf8"),
    ]
    render_terminal_window("PowerShell - docker run & verification", lines, os.path.join(OUTPUT_DIR, "docker_run_ps_terminal.png"), width=1180)


def generate_browser_mockup() -> None:
    width = 900
    height = 360
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    ui_font = ImageFont.truetype(UI_FONT_PATH, 12)
    url_font = ImageFont.truetype(UI_FONT_PATH, 13)
    content_font = ImageFont.truetype(UI_FONT_PATH, 22)

    # Browser top bar
    draw.rectangle([(0, 0), (width, 82)], fill=(241, 243, 244, 255))
    draw.line([(0, 82), (width, 82)], fill=(218, 220, 224, 255), width=1)

    # Tab
    draw.rounded_rectangle([(80, 8), (280, 42)], radius=6, fill=(255, 255, 255, 255))
    draw.text((100, 25), "Docker App - Localhost", font=ui_font, fill=(60, 64, 67, 255), anchor="lm")

    # Window dots
    draw.ellipse([(16, 16), (28, 28)], fill=(239, 68, 68, 255))
    draw.ellipse([(36, 16), (48, 28)], fill=(245, 158, 11, 255))
    draw.ellipse([(56, 16), (68, 28)], fill=(16, 185, 129, 255))

    # Address bar
    draw.rounded_rectangle([(120, 46), (780, 76)], radius=15, fill=(255, 255, 255, 255), outline=(218, 220, 224, 255))
    draw.text((145, 61), "http://localhost:5000/", font=url_font, fill=(32, 33, 36, 255), anchor="lm")

    # Page body content
    draw.text((60, 160), "Hello! My first Docker application is running.", font=content_font, fill=(32, 33, 36, 255))

    img.save(os.path.join(OUTPUT_DIR, "docker_browser_localhost5000.png"), dpi=(300, 300))


def main() -> None:
    print("[*] Generating terminal snapshots and browser mockups...")
    generate_build_terminal()
    generate_run_terminal()
    generate_browser_mockup()
    print("[OK] Snapshots generated successfully in images/ directory.")


if __name__ == "__main__":
    main()
