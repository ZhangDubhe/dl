import os
import ssl
import urllib.request
import time
import random
from utils import cPrint
from waitpool import IMAGES_MAP_1
os.makedirs('./images', exist_ok=True)

ROW_MAX = 35
COL_MAX = 35
ERROR_THRESHOLD = 2

IMAGES_MAP = IMAGES_MAP_1


def build_image_src(prefix, row, col):
    return f'{prefix}/{col}_{row}.jpg'


def urllib_download(prefix, img_url, save_name):
    suffix = img_url.split('/')[-1].split('.')[-1]
    savePath = f'{prefix}/{save_name}.{suffix}'
    if os.path.exists(savePath):
        print(f'已存在 {save_name}')
        return
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(img_url, headers=header)
    resp = urllib.request.urlopen(req, context=context)
    content = resp.read()
    # urlretrieve(src, f'./image/{name}.jpg')
    with open(savePath, 'wb') as f:
        f.write(content)
        f.close()
        print("已保存文件:%s" % (savePath))
    time.sleep(random.randint(0, 1)/20)


def fetch_one_image(imageName):
    fold_prefix = './images/' + imageName.replace('/', '_')
    os.makedirs(fold_prefix, exist_ok=True)
    imageSrc = IMAGES_MAP.get(imageName)
    cPrint(imageSrc, pType=4, pColor=36)

    errRowTimes = 0
    for rowCur in range(0, ROW_MAX):
        errColTimes = 0
        for colCur in range(0, COL_MAX):
            download_url = build_image_src(
                imageSrc, row=rowCur, col=colCur)
            save_name = f'{rowCur}__{colCur}'
            try:
                urllib_download(fold_prefix, download_url, save_name)
                errRowTimes = 0
            except:
                cPrint(download_url, pColor=31)
                errColTimes += 1
                pass

            if errColTimes > ERROR_THRESHOLD:
                cPrint(f'错误次数超过{errColTimes-1}, 自动下一行', pColor=31)
                errRowTimes += 1
                break
        if errRowTimes > ERROR_THRESHOLD:
            cPrint(f'错误次数超过{errRowTimes-1}, 自动下一张', pColor=31)
            break
        print(f'[row] {imageName} {rowCur} finished')


DIVIDE = 10 * '-'


def main():
    for imageName in IMAGES_MAP:
        cPrint(f'{DIVIDE}[image]{DIVIDE}', pColor=36)
        cPrint(f'[+]{imageName}')
        fetch_one_image(imageName)


if __name__ == '__main__':
    main()
