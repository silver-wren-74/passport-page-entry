"""Entry for make.fun the-passport-page-of-a-countr-2-20261121-0318.

Draws an invented passport spread for a country that does not exist —
the Republic of Noverra — and writes it to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png). Pure standard library: a small PNG
encoder, drawing primitives and a 5x7 bitmap font, all in this file.
"""

import os
import struct
import zlib

W, H = 1000, 700

# ---------------------------------------------------------------- PNG sink
def png_bytes(w, h, rgb):
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b""
    stride = w * 3
    for y in range(h):
        raw += b"\x00" + rgb[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, colour):
        self.w, self.h = w, h
        self.px = bytearray(colour * (w * h))

    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(colour)

    def rect(self, x0, y0, x1, y1, colour):
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.set(x, y, colour)

    def frame(self, x0, y0, x1, y1, colour, t=2):
        self.rect(x0, y0, x1, y0 + t, colour)
        self.rect(x0, y1 - t, x1, y1, colour)
        self.rect(x0, y0, x0 + t, y1, colour)
        self.rect(x1 - t, y0, x1, y1, colour)

    def disc(self, cx, cy, r, colour):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, colour)

    def ring(self, cx, cy, r, colour, t=3):
        for y in range(cy - r - t, cy + r + t + 1):
            for x in range(cx - r - t, cx + r + t + 1):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r - t <= d <= r:
                    self.set(x, y, colour)


# ---------------------------------------------------------------- 5x7 font
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11), "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E), "D": (0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F), "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F), "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E), "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11), "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11), "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E), "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D), "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E), "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E), "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11), "X": (0x11, 0x0A, 0x04, 0x04, 0x04, 0x0A, 0x11),
    "Y": (0x11, 0x0A, 0x04, 0x04, 0x04, 0x04, 0x04), "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E), "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F), "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02), "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E), "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E), "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0), ".": (0, 0, 0, 0, 0, 0x0C, 0x0C), ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    "-": (0, 0, 0, 0x1F, 0, 0, 0), "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0), ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
}


def text(cv, x, y, s, colour, scale=2):
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits & (0x10 >> col):
                    cv.rect(cx + col * scale, y + row * scale,
                            cx + (col + 1) * scale, y + (row + 1) * scale, colour)
        cx += 6 * scale
    return cx


# ---------------------------------------------------------------- the spread
INK = (28, 32, 58)
PAPER = (238, 233, 216)
GOLD = (176, 141, 62)
RED = (148, 42, 48)
FAINT = (196, 188, 164)


def draw():
    cv = Canvas(W, H, (24, 22, 34))
    cv.rect(30, 30, 970, 670, PAPER)                 # the open booklet
    cv.rect(493, 30, 507, 670, FAINT)                # centre fold
    # guilloche-ish border: nested frames
    for i, col in enumerate((GOLD, INK, GOLD)):
        cv.frame(46 + i * 7, 46 + i * 7, 479 - i * 7, 654 - i * 7, col, 2)
        cv.frame(521 + i * 7, 46 + i * 7, 954 - i * 7, 654 - i * 7, col, 2)
    # left page: data page
    text(cv, 84, 84, "REPUBLIC OF NOVERRA", INK, 3)
    text(cv, 84, 122, "PASSPORT  PASSEPORT", GOLD, 2)
    cv.disc(150, 250, 62, (203, 196, 172))           # photo window
    cv.disc(150, 228, 24, INK)                       # portrait head
    cv.rect(112, 256, 188, 306, INK)                 # portrait shoulders
    cv.frame(84, 182, 216, 318, INK, 2)
    text(cv, 240, 196, "SURNAME", GOLD, 2)
    text(cv, 240, 220, "WANDERER", INK, 2)
    text(cv, 240, 262, "GIVEN NAMES", GOLD, 2)
    text(cv, 240, 286, "ANYA MARIS", INK, 2)
    text(cv, 84, 356, "NATIONALITY  NOVERAN", INK, 2)
    text(cv, 84, 396, "DATE OF BIRTH  01 APR 1993", INK, 2)
    text(cv, 84, 436, "PLACE OF BIRTH  PORT LENTO", INK, 2)
    text(cv, 84, 476, "DATE OF ISSUE  14 FEB 2024", INK, 2)
    text(cv, 84, 516, "DATE OF EXPIRY  14 FEB 2034", INK, 2)
    text(cv, 84, 580, "NVRA9928471", RED, 3)
    # right page: visas and stamps
    text(cv, 560, 84, "VISAS", INK, 3)
    cv.ring(650, 250, 74, RED, 4)
    text(cv, 596, 222, "KINGDOM OF", RED, 1)
    text(cv, 590, 240, "BRUME  ENTRY", RED, 1)
    text(cv, 600, 258, "03 JUN 2025", RED, 1)
    cv.ring(830, 300, 64, INK, 4)
    text(cv, 786, 276, "FREE CITY OF", INK, 1)
    text(cv, 792, 294, "OSTRO  EXIT", INK, 1)
    text(cv, 790, 312, "19 SEP 2025", INK, 1)
    cv.frame(560, 420, 760, 520, GOLD, 3)
    text(cv, 580, 446, "REPUBLIC OF", GOLD, 2)
    text(cv, 580, 474, "VELD - VISA 90 DAYS", GOLD, 2)
    text(cv, 580, 560, "THIS COUNTRY DOES NOT EXIST.", INK, 2)
    text(cv, 580, 592, "THE STAMPS, HOWEVER, ARE REAL.", INK, 2)
    return png_bytes(W, H, cv.px)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(draw())


if __name__ == "__main__":
    main()
