import os
from tesserocr import PyTessBaseAPI

ROOT_DATA_PATH='./data'


def tesserocr():
    images = [f"{ROOT_DATA_PATH}/images/{file}" for file in os.listdir(f"{ROOT_DATA_PATH}/images")]

    with PyTessBaseAPI(path=f'{ROOT_DATA_PATH}/tessdata', lang='chi_tra') as api:
        with open('output.txt', 'w') as f:
            for img in images:
                api.SetImageFile(img)
                print(f'{api.GetUTF8Text().replace(" ", "")}\n', file=f)


def main():
    tesserocr()


if __name__ == '__main__':
    main()