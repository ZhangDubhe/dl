import os
import re
from PIL import Image
import numpy as np
import time
from utils import cPrint


def check_file(x):
    return '.jpg' in x


def getFileSize(filePath):
    _fileSize = os.path.getsize(filePath)
    _fileSize = _fileSize/float(1024*1024)
    return round(_fileSize, 2)


def mergeFolder(folderPath=None):
    if folderPath is not None:
        folderPath = f'{folderPath}/' if folderPath[-1] != '/' else folderPath
    file_list = os.listdir(folderPath)
    all_images = list(filter(check_file, file_list))
    MATRIX_SIZE = [0, 0]

    def get_image_matrix(x):
        name = x.split('.')[0]
        matrix = []  # row, column
        if '__' in name:
            matrix = list(map(int, name.split('__')))
        else:
            rowColArr = name.split('_')
            rowColArr.reverse()
            matrix = list(map(int, rowColArr))
        return matrix

    all_arr = map(get_image_matrix, all_images)
    for each in list(all_arr):
        MATRIX_SIZE[0] = max(each[0], MATRIX_SIZE[0])
        MATRIX_SIZE[1] = max(each[1], MATRIX_SIZE[1])

    startTime = time.time()
    testImage = Image.open((folderPath or './') + file_list[0])
    sz = testImage.size
    testMatrix = np.atleast_2d(testImage)
    testShape = testMatrix.shape
    basemat = None
    baseColMat = None
    baseColSize = None
    print(
        f'[+] MATRIX {folderPath}: {MATRIX_SIZE}, size: {sz},shape: {testShape}')
    # cPrint(f'size: {sz},shape: {testShape}, basemat: {basemat}')
    for col in range(0, MATRIX_SIZE[1] + 1):
        tMat = None
        for row in range(0, MATRIX_SIZE[0] + 1):
            file = f'{row}__{col}.jpg' if '__' in file_list[0] else f'{col}_{row}.jpg'
            im = Image.open((folderPath or './') + file)

            im = im.resize(sz, Image.ANTIALIAS)
            mat = np.atleast_2d(im)
            tMat = mat
            if ~np.any(mat) and len(mat.shape) < 3:
                mat = np.zeros((256, 256, 3), dtype=np.uint8)
            basemat = mat if row == 0 else np.append(basemat, mat, axis=0)
        try:
            colImage = Image.fromarray(basemat)
        except Exception as e:
            print(e)
            print('baseMat', basemat.shape)
            break
        if baseColMat is None:
            colMat = np.atleast_2d(colImage)
            baseColMat = colMat
            baseColSize = colImage.size
        else:
            colImage = colImage.resize(baseColSize, Image.ANTIALIAS)
            colMat = np.atleast_2d(colImage)
            baseColMat = np.append(baseColMat, colMat, axis=1)
    if baseColMat is None:
        cPrint('[ERROR] baseColMat')
        return
    finalImage = Image.fromarray(baseColMat)
    curPath = folderPath if folderPath is not None else os.getcwd()
    curPath = re.sub(r'\/$', '', curPath)
    imgName = curPath.split('/')[-1]
    savePath = f'{"./exp/" if folderPath is not None else "../"}{imgName}.jpg'
    cPrint(f'[+] saving image: {savePath} {finalImage.size}')
    finalImage.save(savePath)
    saveDuration = '%.4f' % (time.time() - startTime)
    cPrint(
        f'[+] saved. size: {getFileSize(savePath)}MB. Take {saveDuration}s')


def main():
    mergeFolder()


if __name__ == '__main__':
    main()
