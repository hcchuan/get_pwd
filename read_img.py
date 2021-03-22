import pytesseract
from PIL import Image
import requests
import re
 
#使用pytesseract类库进行图片识别
#python I:\work\project\python\get_pwd\read_img.py

im=Image.open("images/2.jpg")
print(pytesseract.image_to_string(im))
im1=Image.open("images/3.png")
print(pytesseract.image_to_string(im1))