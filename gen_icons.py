#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pure-stdlib PNG icon generator for the 收租啦 PWA.
Draws a rounded-square deep-sea-blue tile with an accent-orange house glyph.
No third-party deps (Pillow/venv unavailable in this sandbox)."""
import zlib, struct, math

def make_icon(size):
    N = size
    buf = bytearray(N * N * 4)  # RGBA

    def set_px(x, y, r, g, b, a=255):
        if 0 <= x < N and 0 <= y < N:
            i = (y * N + x) * 4
            buf[i] = r; buf[i+1] = g; buf[i+2] = b; buf[i+3] = a

    # palette
    BG = (14, 58, 92)      # #0E3A5C deep sea blue
    AC = (255, 138, 61)    # #FF8A3D accent orange

    # rounded-square background
    rad = int(N * 0.22)
    for y in range(N):
        for x in range(N):
            # rounded rect mask
            inside = True
            # corners
            for (cx, cy) in [(rad, rad), (N-1-rad, rad), (rad, N-1-rad), (N-1-rad, N-1-rad)]:
                # determine if in a corner zone
                pass
            # simpler: compute distance to rect
            nx = min(x, rad) if x < rad else (max(x, N-1-rad) if x > N-1-rad else x)
            ny = min(y, rad) if y < rad else (max(y, N-1-rad) if y > N-1-rad else y)
            dx = x - nx; dy = y - ny
            if dx*dx + dy*dy <= rad*rad:
                set_px(x, y, *BG)

    # house body rect (accent)
    bx0, by0, bx1, by1 = int(N*0.34), int(N*0.50), int(N*0.66), int(N*0.76)
    for y in range(by0, by1):
        for x in range(bx0, bx1):
            set_px(x, y, *AC)

    # roof triangle (apex top-center -> base corners)
    ax, ay = N*0.50, N*0.28
    lx, ly = N*0.27, N*0.53
    rx, ry = N*0.73, N*0.53
    for y in range(int(ay), int(ly)+1):
        t = (y - ay) / (ly - ay) if ly != ay else 0
        left = int(ax + (lx - ax) * t)
        right = int(ax + (rx - ax) * t)
        for x in range(left, right+1):
            set_px(x, y, *AC)

    # door (cutout in bg color)
    dx0, dy0, dx1, dy1 = int(N*0.44), int(N*0.60), int(N*0.56), int(N*0.76)
    for y in range(dy0, dy1):
        for x in range(dx0, dx1):
            set_px(x, y, *BG)

    return buf

def write_png(path, size, buf):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    raw = bytearray()
    N = size
    for y in range(N):
        raw.append(0)  # filter type 0
        raw.extend(buf[y*N*4:(y+1)*N*4])
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", N, N, 8, 6, 0, 0, 0)  # 8-bit RGBA
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))
    print("wrote", path)

for s in (192, 512):
    write_png("D:/TestApp/app/icons/icon-%d.png" % s, s, make_icon(s))
