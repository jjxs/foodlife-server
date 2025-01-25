# from pyzbar.pyzbar import decode
from PIL import Image
import os
# QRコード(QRcode.png)の指定
image = './image/seat_17_1.jpg'
# QRコードの読取り
# temp = Image.open(image)

# data = decode(temp)
# # コード内容テキストファイル(output.txt)に出力
# f = open('output.txt','a')
# f.write(data[0][0].decode('utf-8', 'ignore'))
# f.close()