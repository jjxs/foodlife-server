
import os
import cv2
import numpy
import ast


def compress_file(compression_file_path, original_file_path, file_size, default_file_size):
    """圧縮ファイル"""

    # 原本ファイル読込む
    img = imread(original_file_path, flags=cv2.COLOR_BAYER_GB2RGB)
    _, ext = os.path.splitext(original_file_path)

    if numpy.any(img):
        img_weight, img_height, img_chanel = img.shape[:3]
        if img_weight>1024:
            img = cv2.resize(img, (1024,576))

        # if ext.lower() == 'png':
        #     # 圧縮率計算
        #     img_quality = int((default_file_size / int(file_size)) * 10)
        #     compress_type = int(cv2.IMWRITE_PNG_COMPRESSION)
        # else:
        #     # 圧縮率計算
        #     img_quality = int((default_file_size / int(file_size)) * 100)
        #     compress_type = int(cv2.IMWRITE_JPEG_QUALITY)

        # encode_param = [compress_type, img_quality]
        # img_result, img_encode = cv2.imencode('.jpg', img, encode_param)
        img_result, img_encode = cv2.imencode('.jpg', img)

        img_decode = cv2.imdecode(img_encode, img_chanel)

        # 圧縮ファイル作成
        imwrite(compression_file_path, img_decode)

def imread(file_path, flags=cv2.IMREAD_COLOR, dtype=numpy.uint8):
    '''ファイル名が日本語の場合、対応する'''
    try:
        n = numpy.fromfile(file_path, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(file_path, img, params=None):
    '''ファイル名が日本語の場合、対応する'''
    try:
        ext = os.path.splitext(file_path)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(file_path, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        return False



to_size = 512 * 1024

path = 'C:/Users/kxgsy/Downloads/22579343'
to_path = 'C:/Users/kxgsy/Downloads/output_img'
g = os.walk(path)
for file, d, filelist in g:
    for filename in filelist:
        to_file = "{0}/{1}".format(to_path, filename)

        ori_file = "{0}/{1}".format(path, filename)
        
        size = os.path.getsize(ori_file)
        print(ori_file, to_file, size)

        compress_file(to_file, ori_file, size, to_size)