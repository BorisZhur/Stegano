

import cv2
import math
from cv2 import dct, idct
from PIL import Image
import numpy as np


def write(binWrd):
    image = Image.open("input.bmp") #Открываем изображение.
    width = image.size[0] #Определяем ширину.
    height = image.size[1] #Определяем высоту.
    
    imageOutput = Image.open("input.bmp")

    pix = np.array(image.getdata(1))
    pix = pix.reshape(height,width)
    obj = image.load()
    obj1 = imageOutput.load()
    binWrdLen = 0
    for i in range(int(height / 8)):
        for j in range(int(width / 8)):
            #print("i ",i)
            #print("\nj ",j)
            matrix = np.array(pix[8 * i:8 * (i + 1), 8 * j:8 * (j + 1)])
            matrix = matrix.astype('float32')
            matrix_dct = dct(matrix)
            #print("\nmatrix\n",matrix)
            #print("\nmatrix_dct\n",matrix_dct)
            if (binWrdLen < len(binWrd)):
                for k in range(8):
                    for l in range(8):
                        #print(matrix_dct[k][k])
                        if (binWrdLen < len(binWrd)):
                            matrix_dct[k][l] = (round(matrix_dct[k][l]))
                            matrix_dct[k][l] = matrix_dct[k][l] - matrix_dct[k][l] % 2 + int(binWrd[binWrdLen])
                        binWrdLen += 1
                #print(idct(matrix_dct))
                new_matrix = [round(x) for x in idct(matrix_dct).reshape(1,64)[0]]
                #print('new matrix', new_matrix)
                for h in range(0, 64):
                    rx = h // 8
                    ry = h % 8
                    x = list(obj[j * 8 + ry, i * 8 + rx])
                    x[1] = new_matrix[h]
                    obj1[j * 8 + ry, i * 8 + rx] = tuple(x)
    imageOutput.save("output.bmp", "BMP")

def read(wrd,binWrd):
    binMsg = []
    imageOutput = Image.open("output.bmp")
    width = imageOutput.size[0]  # Определяем ширину.
    height = imageOutput.size[1]  # Определяем высоту.
    pix = np.array(imageOutput.getdata(1))
    pix = pix.reshape(height,width)
    binWrdLen = 0
    for i in range(int(height / 8)):
        for j in range(int(width / 8)):
            matrix = np.array(pix[8 * i:8 * (i + 1), 8 * j:8 * (j + 1)])
            matrix = matrix.astype('float32')
            matrix_dct = dct(matrix)
            if (binWrdLen < len(binWrd)):
                for k in range(8):
                    for l in range(8):
                        if (binWrdLen < len(binWrd)):
                            matrix_dct[k][l] = (round(matrix_dct[k][l]))
                            binMsg.append(int(matrix_dct[k][l] % 2))
                        binWrdLen += 1


    answer = ''
    for i in range(len(wrd)):
        bin_str = ''.join(str(x) for x in (binMsg[(i * 8):(i + 1) * 8]))
        if bin_str == '10011000':
            answer += ' '
        else:
            answer += str(bytes([int(bin_str, base=2)]), 'cp1251')
    print("прочитанно - " , answer)
    check = ''.join(str(x) for x in (binMsg))

    number_of_mistakes = 0
    for l in range(len(binWrd)):
        if binWrd[l] != check[l]:
            number_of_mistakes += 1
    print('При передаче искажено %d бит' % number_of_mistakes)
    print('или %f процентов ' % (100.*(float(number_of_mistakes)/ len(binWrd))))

def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def calcPNSR(k):
    old = cv2.imread("input.bmp")
    changed = cv2.imread("output.bmp", 1)
    #psnrcv = cv2.PSNR(old, changed)
    psnrcv = psnr(old, changed)
    print('psnr(',k,') = ', psnrcv)


wrd = str(input("Введите слово\n"))
msg = ''
s = [1,2,3,5,10,20,30,40,50,100,150,200,250,300,400,500,1000]
#s = [250]
for k in s:
    msg = ''
    for i in range (int(k)):
        msg += wrd
    binWrd = ''
    for code in msg.encode('cp1251'):
        a = bin(code)[2:]
        while len(a) < 8:
            a = '0' + a
        binWrd += a
    write(binWrd)
    read(msg,binWrd)
    calcPNSR(k)