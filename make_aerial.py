#!/usr/bin/env python3
# 抓 NLSC 正射航照(PHOTO2)+地籍界線(LANDSECT)，以三家段669置中拼接出圖
import urllib.request, ssl, math, io
from PIL import Image, ImageDraw, ImageFont

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
Z = 18
N = 2 ** Z
TS = 256

# 三筆地號中心 (lon, lat, 標籤, 顏色)
PARCELS = [
    (120.576574, 24.015248, "669", (255, 60, 60)),    # 原廠 紅
    (120.576903, 24.014657, "668", (79, 195, 247)),   # 一期 青
    (120.578069, 24.014656, "672", (255, 167, 38)),   # 二期 橘
]
CLON, CLAT = 120.576574, 24.015248  # 以 669 置中
CROP_W, CROP_H = 1200, 820

def gpix(lon, lat):
    x = (lon + 180) / 360 * N * TS
    y = (1 - math.log(math.tan(math.radians(lat)) + 1/math.cos(math.radians(lat))) / math.pi) / 2 * N * TS
    return x, y

def fetch(layer, tx, ty):
    url = f"https://wmts.nlsc.gov.tw/wmts/{layer}/default/GoogleMapsCompatible/{Z}/{ty}/{tx}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, context=ctx, timeout=30).read()

cx, cy = gpix(CLON, CLAT)
ctx_tile_x, ctx_tile_y = int(cx // TS), int(cy // TS)
R = 4  # 中心 ±4 格 → 9x9 格
tx0, tx1 = ctx_tile_x - R, ctx_tile_x + R
ty0, ty1 = ctx_tile_y - R, ctx_tile_y + R
cols = tx1 - tx0 + 1; rows = ty1 - ty0 + 1
big = Image.new("RGBA", (cols * TS, rows * TS))

print(f"拼接 {cols}x{rows} 格…")
for j, ty in enumerate(range(ty0, ty1 + 1)):
    for i, tx in enumerate(range(tx0, tx1 + 1)):
        try:
            air = Image.open(io.BytesIO(fetch("PHOTO2", tx, ty))).convert("RGBA")
        except Exception as e:
            air = Image.new("RGBA", (TS, TS), (30, 30, 30, 255))
        try:
            line = Image.open(io.BytesIO(fetch("LANDSECT", tx, ty))).convert("RGBA")
            air.alpha_composite(line)
        except Exception:
            pass
        big.paste(air, (i * TS, j * TS))

# big 左上角的全域像素
ox, oy = tx0 * TS, ty0 * TS
draw = ImageDraw.Draw(big)
def font(sz):
    for p in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()
F = font(34)

for lon, lat, label, col in PARCELS:
    px, py = gpix(lon, lat); px -= ox; py -= oy
    r = 9
    draw.ellipse([px-r, py-r, px+r, py+r], fill=col + (255,), outline=(255,255,255,255), width=3)
    # 標籤底
    tb = draw.textbbox((0, 0), label, font=F); tw, th = tb[2]-tb[0], tb[3]-tb[1]
    lx, ly = px + 14, py - th - 14
    draw.rectangle([lx-6, ly-6, lx+tw+6, ly+th+8], fill=(0, 0, 0, 170))
    draw.text((lx, ly), label, font=F, fill=col + (255,))

# 以 669 置中裁切
ccx, ccy = gpix(CLON, CLAT); ccx -= ox; ccy -= oy
left = int(ccx - CROP_W/2); top = int(ccy - CROP_H/2)
crop = big.crop((left, top, left + CROP_W, top + CROP_H)).convert("RGB")
out = "images/aerial_669.png"
crop.save(out, "PNG")
print("已存:", out, crop.size)
