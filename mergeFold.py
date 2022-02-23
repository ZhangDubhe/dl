import merge
import os
from utils import cPrint


def main():
    print('====' * 10)
    print('start merge')
    allFolderPath = './images/'
    folderList = os.listdir(allFolderPath)
    for each in folderList:
        if each[0] == '.':
            continue
        if os.path.exists(f'./exp/{each}.jpg'):
            # cPrint(f'[已存在] {each}', pColor=36)
            continue

        cPrint(f'[start] {each}', pColor=36)
        try:
            merge.mergeFolder(f'{allFolderPath}{each}')
        except Exception as e:
            cPrint(f'[error] {each}', pColor=31)
            cPrint(e, pColor=31)
            print('')
            pass
    print('merge all end')
    print('====' * 10)


if __name__ == '__main__':
    main()
