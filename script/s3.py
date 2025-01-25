
import os
import cv2
import numpy
import ast
import boto3
import json



def getList():
    str = '''22579343/menu_images/43.jpg
            22579343/menu_images/12.jpg
            22579343/menu_images/57.jpg
            22579343/menu_images/40.jpg
            22579343/menu_images/22.jpg
            22579343/menu_images/14.jpg
            22579343/menu_images/56.jpg
            22579343/menu_images/35.jpg
            22579343/menu_images/54.jpg
            22579343/menu_images/44.jpg
            22579343/menu_images/32.jpg

            22579343/menu_images/23.jpg


            22579343/menu_images/39.jpg
            22579343/menu_images/18.jpg
            22579343/menu_images/52.jpg
            22579343/menu_images/20.jpg
            22579343/menu_images/53.jpg
            22579343/menu_images/21.jpg
            22579343/menu_images/34.jpg
            22579343/menu_images/1000.jpg
            22579343/menu_images/157.jpg
            22579343/menu_images/1026.jpg
            22579343/menu_images/1027.jpg
            22579343/menu_images/1028.jpg
            22579343/menu_images/1009.jpg

            22579343/menu_images/145.jpg
            22579343/menu_images/1014.jpg
            22579343/menu_images/165.jpg
            22579343/menu_images/54.jpg
            22579343/menu_images/177.jpg
            22579343/menu_images/172.jpg
            22579343/menu_images/178.jpg
            22579343/menu_images/155.jpg
            22579343/menu_images/151.jpg
            22579343/menu_images/153.jpg
            22579343/menu_images/146.jpg
            22579343/menu_images/160.jpg

            22579343/menu_images/176.jpg
            22579343/menu_images/150.jpg
            22579343/menu_images/1012.jpg
            22579343/menu_images/1003.jpg
            22579343/menu_images/173.jpg
            22579343/menu_images/42.jpg
            22579343/menu_images/15.jpg
            22579343/menu_images/51.jpg
            22579343/menu_images/148.jpg
            22579343/menu_images/174.jpg
            22579343/menu_images/170.jpg
            22579343/menu_images/27.jpg
            22579343/menu_images/28.jpg
            22579343/menu_images/1.jpg
            22579343/menu_images/36.jpg
            22579343/menu_images/46.jpg
            22579343/menu_images/4.jpg
            22579343/menu_images/33.jpg
            22579343/menu_images/11.jpg
            22579343/menu_images/19.jpg
            22579343/menu_images/1016.jpg
            22579343/menu_images/59.jpg
            '''
    arr = str.split("\n")
    result = []
    for item in arr:
        result.append(item.strip())
    print(result)
    return result

def download():
    """圧縮ファイル"""
    print("hello")
    s3 = boto3.resource('s3')
    arr = getList()
    for fname in arr:
        if fname:
            to_file = fname.split('/')
            name = to_file[-1]
            print(fname, name)
            s3.Bucket('foodlife').download_file(fname, to_path + name)


to_path = 'C:/Users/kxgsy/Downloads/22579343/'

download()
