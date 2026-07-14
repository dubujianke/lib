'''
100平米房间平面设计图，背景色（255,255,255）墙体用实心黑色(0,0,0)矩形，
窗户用实心绿色(0, 255,0)矩形，不准用扇形， 门用实心黄色(255,255,0)矩形
床用实心蓝色矩形（0,0,255） 不准有杂色， 不需要标注
整个图片只能使用以上几种颜色， 不允许有 过渡色
'''
import os

os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"
from PIL import Image
import numpy as np
from collections import deque
from PIL import Image, ImageDraw
import cv2
import easyocr
# ========== 可调参数 ==========
BLACK_THRESHOLD = (60,60,60)      # RGB 各分量小于此值视为黑色
GREEN_THRESHOLD = (60,125,60)      # RGB 各分量小于此值视为黑色
MIN_AREA = 200            # 最小面积（像素），小于该值的黑色区域不替换
# ============================


img = Image.open("input.png")
# img = Image.open(r"D:\Download\caffe.png")
pixels = img.load()
width, height = img.size

from collections import deque

from shapely.geometry import box
from shapely.ops import unary_union


def merge_rects_to_polygon(rects):
    polys = []
    for x1, y1, x2, y2 in rects:
        polys.append(box(x1, y1, x2, y2))
    merged = unary_union(polys)
    result = []
    if merged.geom_type == "Polygon":
        coords = list(merged.exterior.coords)
        result.append(coords)
    elif merged.geom_type == "MultiPolygon":
        for poly in merged.geoms:
            coords = list(poly.exterior.coords)
            result.append(coords)
    return result
def isBlackRect(pixels, width, height, cx, cy, radius=5):
    x1 = cx - radius
    y1 = cy - radius
    x2 = cx + radius
    y2 = cy + radius
    if x1 < 0 or y1 < 0 or x2 >= width or y2 >= height:
        return False
    corners = [
        (x1, y1),
        (x2, y1),
        (x1, y2),
        (x2, y2)
    ]
    for x, y in corners:
        r, g, b = pixels[x, y]
        if not (r == 0 and g == 0 and b == 0):
            return False
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            r, g, b = pixels[x, y]
            if not (r == 0 and g == 0 and b == 0):
                return False
    return True

def find_first_black_rect_point(img, radius=5):
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            ok = isBlackRect(
                pixels,
                width,
                height,
                x,
                y,
                radius
            )
            if ok:
                return (x, y)
    return None
def grow_room_rectangle(
        img_path,
        seed_point,
        wall_value=255,
        save_mask=False,
        mask_path="rect_mask.png"
):
    img = Image.open(img_path).convert("L")
    arr = np.array(img)
    h, w = arr.shape
    cx, cy = seed_point
    cx = int(cx)
    cy = int(cy)
    if cx < 0 or cy < 0 or cx >= w or cy >= h:
        return None
    if arr[cy, cx] == wall_value:
        return None
    x1 = cx
    x2 = cx
    while x1 - 1 >= 0:
        if arr[cy, x1 - 1] == wall_value:
            break
        x1 -= 1
    while x2 + 1 < w:
        if arr[cy, x2 + 1] == wall_value:
            break
        x2 += 1
    x1 = x1 + 5
    x2 = x2 - 5
    y1 = cy
    while y1 - 1 >= 0:
        ok = True
        for xx in range(x1, x2 + 1):
            if arr[y1 - 1, xx] == wall_value:
                ok = False
                break
        if not ok:
            break
        y1 -= 1
    y2 = cy
    while y2 + 1 < h:
        ok = True
        for xx in range(x1, x2 + 1):
            if arr[y2 + 1, xx] == wall_value:
                ok = False
                break
        if not ok:
            break
        y2 += 1
    rect = (x1-5, y1-2, x2+5, y2+2)
    if save_mask:
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[y1:y2+1, x1:x2+1] = 255
        Image.fromarray(mask).save(mask_path)
    return rect

def draw_polygons(
        img_path,
        polygons,
        output_path="polygon_output.png",
        line_width=3
):
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    colors = [
        (255, 0, 0)
    ]
    for i, poly in enumerate(polygons):
        if len(poly) < 2:
            continue
        color = colors[0]
        points = poly + [poly[0]]
        draw.line(
            points,
            fill=color,
            width=line_width
        )
        for x, y in poly:
            r = 4
            draw.ellipse(
                (
                    x - r,
                    y - r,
                    x + r,
                    y + r
                ),
                fill=(255, 255, 255)
            )
    img.save(output_path)

def draw_rectangles(
        img,
        polygons,
        line_width=3
):
    draw = ImageDraw.Draw(img)
    poly_color = (255, 0, 0)
    for poly in polygons:
        pts = [(int(x), int(y)) for x, y in poly]
        if len(pts) >= 2:
            pts.append(pts[0])
        draw.line(
            pts,
            fill=poly_color,
            width=line_width
        )
def fill_rectangles(
        img,
        polygons
):
    draw = ImageDraw.Draw(img)
    poly_color = (255, 255, 255)
    for poly in polygons:
        pts = [(int(x), int(y)) for x, y in poly]
        if len(pts) >= 2:
            pts.append(pts[0])
        if len(pts) >= 3:
            draw.polygon(
                pts,
                fill=poly_color
            )
        # draw.line(
        #     pts,
        #     fill=poly_color,
        #     width=line_width
        # )
def draw_rectangle(
    img,
    rect
):
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = rect
    draw.rectangle(
        [x1, y1, x2, y2],
        outline=(255, 0, 0),
        width=3
    )

def fill_rectangle(
    img,
    rect,
    color=(255, 255, 255)
):
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = rect
    draw.rectangle(
        [x1, y1, x2, y2],
        fill=color
    )

from PIL import Image, ImageDraw

def fill_rectangle_inverse(img, bbox, color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    x1, y1, x2, y2 = bbox
    draw.rectangle((0, 0, w, y1), fill=color)
    draw.rectangle((0, y2, w, h), fill=color)
    draw.rectangle((0, y1, x1, y2), fill=color)
    draw.rectangle((x2, y1, w, y2), fill=color)
    return img
def bounding_box(rectangles):
    if not rectangles:
        return None
    min_x = min(r[0] for r in rectangles)
    min_y = min(r[1] for r in rectangles)
    max_x = max(r[2] for r in rectangles)
    max_y = max(r[3] for r in rectangles)
    return (min_x, min_y, max_x, max_y)

def prsRect(rects, binary_output):
    pt = find_first_black_rect_point(binary_output, radius=15)
    if pt is None:
        return False
    draw = ImageDraw.Draw(binary_output)
    cx, cy = pt
    r = 6
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 0, 0))
    print(pt)
    seed = (cx, cy)
    rect = grow_room_rectangle(
        "binary_output2.png",
        seed,
        save_mask=True
    )
    rects.append(rect)
    fill_rectangle(binary_output, rect, color=(255, 255, 255))
    return True

def getOCR(imgPath, retPath):
    polygonObjs = []
    resultPath = "binary_output2.png"
    reader = easyocr.Reader(['ch_sim', 'en'])
    result = reader.readtext("input.png")
    binary_output_ori = Image.open(imgPath).convert("RGB")
    for r in result:
        bbox = r[0]
        text = r[1]
        score = r[2]
        if score <0.8:
            continue
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        x1 = min(xs)
        y1 = min(ys)
        x2 = max(xs)
        y2 = max(ys)
        # 中心点
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        # print({
        #     "text": text,
        #     "score": score,
        #     "center": [cx, cy],
        #     "bbox": [x1, y1, x2, y2]
        # })
        fill_rectangle(binary_output_ori, [x1, y1, x2, y2], color=(0,0,0))
    binary_output_ori.save(resultPath)
    binary_output = Image.open(resultPath).convert("RGB")
    rects = []
    for r in result:
        bbox = r[0]
        text = r[1]
        score = r[2]
        if score < 0.8:
            continue
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        x1 = min(xs)
        y1 = min(ys)
        x2 = max(xs)
        y2 = max(ys)
        # 中心点
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        print(text)
        seed = (cx, cy)
        rect = grow_room_rectangle(resultPath, seed, save_mask=True)
        rects.append(rect)
        print(rect)
        fill_rectangle(binary_output, rect, color=(255, 255, 255))
        # draw_rectangle(binary_output, rect)
    bbox = bounding_box(rects)
    fill_rectangle_inverse(binary_output, bbox, color=(255, 255, 255))
    # img = Image.open(img_path).convert("RGB")
    # binary_output.save("rect_output2.png")
    flag = True
    while(flag):
        flag = prsRect(rects, binary_output)
    # for rect in rects:
    #     draw_rectangle(binary_output_ori, rect)
    polygons = merge_rects_to_polygon(rects)
    for poly in polygons:
        print(poly)
    draw_rectangles(binary_output_ori, polygons)
    binary_output_ori.save(retPath)
    for r in result:
        bbox = r[0]
        text = r[1]
        score = r[2]
        if score < 0.8:
            continue
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        x1 = min(xs)
        y1 = min(ys)
        x2 = max(xs)
        y2 = max(ys)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

    return polygons,result

def processBlack(cThrehold):
    # 1. 构建黑色掩码
    mask = [[False] * height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            mask[x][y] = (r < cThrehold[0] and g < cThrehold[1] and b < cThrehold[2])

    # 2. 连通域分析 + 面积过滤
    visited = [[False] * height for _ in range(width)]
    valid_pixels = []          # 记录所有要替换为红色的像素坐标
    for y in range(height):
        for x in range(width):
            if mask[x][y] and not visited[x][y]:
                # BFS 找连通域
                q = deque()
                q.append((x, y))
                visited[x][y] = True
                region = []
                area = 0
                while q:
                    cx, cy = q.popleft()
                    region.append((cx, cy))
                    area += 1
                    # 8邻域搜索
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if mask[nx][ny] and not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))
                # 只有面积足够大的区域才替换成红色
                if area >= MIN_AREA:
                    valid_pixels.extend(region)
    for (x, y) in valid_pixels:
        pixels[x, y] = (0, 0, 0)
    return valid_pixels

def processGreen(cThrehold):
    # 1. 构建黑色掩码
    mask = [[False] * height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            mask[x][y] = (r < cThrehold[0] and g > 125 and b < cThrehold[2])

    # 2. 连通域分析 + 面积过滤
    visited = [[False] * height for _ in range(width)]
    valid_pixels = []          # 记录所有要替换为红色的像素坐标
    for y in range(height):
        for x in range(width):
            if mask[x][y] and not visited[x][y]:
                # BFS 找连通域
                q = deque()
                q.append((x, y))
                visited[x][y] = True
                region = []
                area = 0
                while q:
                    cx, cy = q.popleft()
                    region.append((cx, cy))
                    area += 1
                    # 8邻域搜索
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if mask[nx][ny] and not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))
                # 只有面积足够大的区域才替换成红色
                if area >= MIN_AREA:
                    valid_pixels.extend(region)
    for (x, y) in valid_pixels:
        pixels[x, y] = (0, 255, 0)
    return valid_pixels
def processBlue(cThrehold):
    # 1. 构建黑色掩码
    mask = [[False] * height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            mask[x][y] = (r < cThrehold[0] and g < cThrehold[0] and b > 125)

    # 2. 连通域分析 + 面积过滤
    visited = [[False] * height for _ in range(width)]
    valid_pixels = []          # 记录所有要替换为红色的像素坐标
    for y in range(height):
        for x in range(width):
            if mask[x][y] and not visited[x][y]:
                # BFS 找连通域
                q = deque()
                q.append((x, y))
                visited[x][y] = True
                region = []
                area = 0
                while q:
                    cx, cy = q.popleft()
                    region.append((cx, cy))
                    area += 1
                    # 8邻域搜索
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if mask[nx][ny] and not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))
                # 只有面积足够大的区域才替换成红色
                if area >= MIN_AREA:
                    valid_pixels.extend(region)
    for (x, y) in valid_pixels:
        pixels[x, y] = (0, 0, 255)
    return valid_pixels
def processYellow(cThrehold):
    # 1. 构建黑色掩码
    mask = [[False] * height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            mask[x][y] = (r > 125 and g > 125 and b < cThrehold[2])

    # 2. 连通域分析 + 面积过滤
    visited = [[False] * height for _ in range(width)]
    valid_pixels = []          # 记录所有要替换为红色的像素坐标
    for y in range(height):
        for x in range(width):
            if mask[x][y] and not visited[x][y]:
                # BFS 找连通域
                q = deque()
                q.append((x, y))
                visited[x][y] = True
                region = []
                area = 0
                while q:
                    cx, cy = q.popleft()
                    region.append((cx, cy))
                    area += 1
                    # 8邻域搜索
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if mask[nx][ny] and not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))
                # 只有面积足够大的区域才替换成红色
                if area >= MIN_AREA:
                    valid_pixels.extend(region)
    for (x, y) in valid_pixels:
        pixels[x, y] = (255, 255, 0)
    return valid_pixels

from shapely.geometry import Point, Polygon
def find_polygon_by_point(polygons, text, cx, cy):
    pt = Point(cx, cy)
    for i, poly in enumerate(polygons):
        polygon = Polygon(poly)
        if polygon.contains(pt):
            return {
                "type":"plane",
                "name":text,
                "polygon": poly
            }
    return None


pixels1 = processBlack(BLACK_THRESHOLD)
pixels2 = processGreen(BLACK_THRESHOLD)
pixels3 = processBlue(BLACK_THRESHOLD)
pixels4 = processYellow(BLACK_THRESHOLD)
img.save("redized_clean.png")
binary_img = Image.new("RGB", (width, height), (0, 0, 0))
binary_pixels = binary_img.load()
all_pixels = (
    pixels1 +
    pixels2 +
    pixels4
)
for (x, y) in all_pixels:
    binary_pixels[x, y] = (255, 255, 255)
tmpPath = "binary_output.png"
binary_img.save(tmpPath)
polygons,result = getOCR(tmpPath, "rect_output2.png")
binary_output_ori = Image.open("redized_clean.png").convert("RGB")
fill_rectangles(binary_output_ori, polygons)
binary_output_ori.save("redized_clean.png")

resultJson = []
for r in result:
    bbox = r[0]
    text = r[1]
    score = r[2]
    if score < 0.8:
        continue
    if text == '餐厅':
        continue
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    x1 = min(xs)
    y1 = min(ys)
    x2 = max(xs)
    y2 = max(ys)
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    result2 = find_polygon_by_point(
        polygons,
        text,
        cx,
        cy
    )
    resultJson.append(result2)
import json
with open("rooms.txt", "w", encoding="utf-8") as f:
    json.dump(
        resultJson,
        f,
        ensure_ascii=False,
        indent=2
    )

# with open("rooms.txt", "r", encoding="utf-8") as f:
#     loaded_rooms = json.load(f)
# for room in loaded_rooms:
#     text = room["text"]
#     polygon = room["polygon"]
#     print("房间:", text)
#     print("polygon:", polygon)
#     print()

