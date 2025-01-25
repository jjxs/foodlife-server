
#!/user/bin/Python3
"""
@Lanson
@2019-11-02
"""
 
"""
需要安装的包：
    pip install pillow
    pip install numpy
    pip install imageio
    pip install qrcode
    pip install matplotlib
    pip install myqr
python版本：3.7+
"""
import qrcode
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageDraw
from PIL import ImageFont
'''
【红色】：red 【橙色】：orange 【黄色】：yellow 【绿】：green 【 蓝】：blue【紫】：purple 
【灰色】：gray 【白色】：white 【粉红色】：pink 【黑色】：black【墨绿色】：dark green 【橙红色】：orange-red
'''
def getQRcode(strs, name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=3,
    )
    # 添加数据
    qr.add_data(strs)
    # 填充数据
    qr.make(fit=True)
    # 生成图片
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("CMYK")  # RGBA
    
    # 获取图片的宽高
    img_w, img_h = img.size
    factor = 6
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    # 显示图片
    # plt.imshow(img)
    # plt.show()
    img = img.convert('RGB')
    img.save(name)
    return img

def info(name,body,text):
    getQRcode(body, name)
    oriImg = Image.open(name)
    
    img_w, img_h = oriImg.size

    draw = ImageDraw.Draw(oriImg)
    font = ImageFont.truetype("arial.ttf", 60)
    draw.text((img_w/2 - 30, img_h - 60), text, (50, 51, 51), font=font)#把字添加到图片上
    oriImg = oriImg.convert('RGB')
    oriImg.save(name)


def do():
    arr = [
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=126&sign=hji","A3"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=132&sign=uyn","A4"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=134&sign=wqi","A1"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=136&sign=qei","A2"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=138&sign=5ti","A5"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=140&sign=2an","A6"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=142&sign=1zn","A7"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=144&sign=r6i","A8"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=146&sign=3gi","A9"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=148&sign=7ni","A10"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=150&sign=83n","F1"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=152&sign=jsi","F2"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=154&sign=lmi","F3"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=156&sign=u1i","F4"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=158&sign=wpi","B1"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=160&sign=cvn","B2"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=162&sign=zbi","B3"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=164&sign=2hi","B4"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=166&sign=1ki","B5"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=168&sign=r2i","B6"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=170&sign=99i","B7"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=172&sign=oji","B8"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=174&sign=8xi","B9"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=176&sign=j7i","B10"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=178&sign=loi","C1"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=180&sign=5qi","C2"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=182&sign=nei","C3"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=184&sign=c8i","C4"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=186&sign=zui","C5"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=188&sign=20i","C6"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=190&sign=76i","C7"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=192&sign=hwi","C8"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=194&sign=9ii","C9"],
        ["http://22579343.app.food-life.co.jp/?s=22579343&seat=196&sign=o4i","C10"]
    ]
    for item in arr:
        name = item[1] + ".jpg"
        print(item[0], item[1])
        info(name, item[0], item[1])
if __name__ == '__main__':
    # info("qrcode_result.png","https://blog.csdn.net/xiaoweite1","Lansonli")
    do()
    print("自定义二维码生成成功!!!")
