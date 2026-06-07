#!/usr/bin/env python3
# 裁切 4-icon 圖標表並依角落底色去背（深淺底通用）
from PIL import Image
from pathlib import Path

IMG = Path("images")

SHEETS = {
    "icon_sheet_company": ["icon_euvpod", "icon_foup", "icon_molding", "icon_cleanroom"],
    "icon_sheet_law":     ["icon_law", "icon_landrule", "icon_water", "icon_eco"],
    "icon_sheet_config":  ["icon_building", "icon_floors", "icon_green", "icon_belt"],
    "icon_sheet_env":     ["icon_recycle", "icon_pond", "icon_check", "icon_terrace"],
}
ALIASES = {"icon_coverage": "icon_building", "icon_buffer": "icon_belt"}

DIST = 70      # 與底色距離 < DIST → 透明
FADE = 120     # DIST~FADE 漸變


def key_bg(crop):
    crop = crop.convert("RGBA")
    px = crop.load()
    w, h = crop.size
    # 取四角平均為底色
    corners = [px[0, 0], px[w-1, 0], px[0, h-1], px[w-1, h-1]]
    br = sum(c[0] for c in corners) / 4
    bg = sum(c[1] for c in corners) / 4
    bb = sum(c[2] for c in corners) / 4
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            d = ((r-br)**2 + (g-bg)**2 + (b-bb)**2) ** 0.5
            if d < DIST:
                px[x, y] = (r, g, b, 0)
            elif d < FADE:
                ratio = (d - DIST) / (FADE - DIST)
                px[x, y] = (r, g, b, int(255 * ratio))
    return crop


for sheet, names in SHEETS.items():
    f = IMG / f"{sheet}.png"
    if not f.exists():
        print("缺少:", f); continue
    img = Image.open(f).convert("RGBA")
    w, h = img.size
    n = len(names)
    for i, name in enumerate(names):
        x0 = i * (w // n)
        x1 = (i + 1) * (w // n) if i < n - 1 else w
        col_w = x1 - x0
        sq = min(col_w, h)
        cx, cy = x0 + col_w // 2, h // 2
        crop = img.crop((cx - sq//2, cy - sq//2, cx + sq//2, cy + sq//2))
        crop = crop.resize((256, 256), Image.LANCZOS)
        crop = key_bg(crop)
        crop.save(IMG / f"{name}.png")
        print("  ->", name)

for alias, src in ALIASES.items():
    Image.open(IMG / f"{src}.png").save(IMG / f"{alias}.png")
    print("  alias", alias, "<-", src)

print("完成")
