import time
import os
import cv2
import numpy as np
import math
from PIL import Image, ImageDraw
from math import sqrt, pi, cos
N = 8
#матрица пикселей
def getPixels(filename):
    img = Image.open(filename, 'r')
    w, h = img.size
    pix = list(img.getdata())
    return pix
img = Image.open("image2.bmp", 'r')
w, h = img.size
w = int(w)
h = int(h)
pix = []
pix = getPixels("image2.bmp")
pix = [pix[n:n+w] for n in range(0, w*h, w)]
pix = np.array(pix)
def C(x):
    if x == 0.0:
        return 1.0 / sqrt(2.0)
    else:
        return 1.0
def DCT (f, N, i, j):
    answer = 0.0
    for x in range(N):
        for y in range(N):
            answer += f[x][y] * cos(((2.0 * x + 1.0) * i * pi) / (2 * N)) * cos(((2.0* y + 1.0) * j * pi) / (2.0 * N))
    answer *= 1 / sqrt(2 * float(N)) * C(i) * C(j)
    return answer
def DCTobr (f, N, x, y):
    answer = 0.0
    for i in range(N):
        for j in range(N):
            answer += f[i][j] * C(i) * C(j) * cos(((2.0 * x + 1.0) * i * pi) / (2 * N)) * cos(((2.0 * y + 1.0) * j * pi) / (2.0 * N))
    answer *= 1 / sqrt(2 * float(N))
    return answer
slovo = input("Введите слово, которое хотите скрыть: ")
razmer_1=len(slovo)
slovo2 = [] #Здесь будет храниться двоичное представление сообщения
for j in slovo.encode('cp1251'): #Переводим сообщение в двоичный вид
    polnoe = bin(j)[2:]
    if len(polnoe) != 8:
        for i in range(8 - len(polnoe)):
            polnoe = '0' + polnoe
    slovo2 += polnoe
print("Ваше слово в двоичном коде: ",slovo2)
for i in range(len(slovo2)): #Каждый элемент 1 и 0 приводим к типу int
    slovo2[i] = int(slovo2[i])
print("Длина сообщения в битах",len(slovo2))
razmer = len(slovo2)
k = 0
image = Image.new("RGB", (160,160), (0,0,0))
draw = ImageDraw.Draw(image)
#блок 8на8 для одной составляющей пикселя
for ii in range(int(h/8)):
    for jj in range(int(w / 8)):
        mas = pix[8 * ii:8 * (ii + 1), 8 * jj:8 * (jj + 1)]
        f_massive_b = [[] for i in range(8)]
        for j in range(8):
            for i in range(8):
                f_massive_b[j].append(mas[j][i][2])
        f_massive_red = [[] for i in range(8)]
        for j in range(8):
            for i in range(8):
                f_massive_red[j].append(mas[j][i][0])
        f_massive_green = [[] for i in range(8)]
        for j in range(8):
            for i in range(8):
                f_massive_green[j].append(mas[j][i][1])
        DCT_massive = [[] for i in range(N)]
        for i in range(N):
            for j in range(N):
                DCT_massive[i].append(((DCT(f_massive, N, i, j)))
        if k < razmer:
            for i in range(N):
                for j in range(N):
                    if k >= razmer:
                        break
                    # if (i+j)>N: continue
                    DCT_massive[i][j] = int(DCT_massive[i][j] + (0.5 if DCT_massive[i][j] > 0 else -0.5))
                    if slovo2[k] == 0:
                        if DCT_massive[i][j] %2 != 0:
                            DCT_massive[i][j] -= 1
                            k +=1
                            continue
                        else:
                            k +=1
                            continue
                    if slovo2[k] == 1:
                        if DCT_massive[i][j] %2 == 0:
                            DCT_massive[i][j] += 1
                            k +=1
                            continue
                        else:
                            k +=1
                            continue
                    #print ("izmenen coafis",DCT_massive)
                    #обратное ДКП
        obratn = [[] for i in range(N)]
        for x in range(N):
            for y in range(N):
                obratn[x].append(int(round(DCTobr(DCT_massive, N, x,y))))
        #вставка пикселей в картинку
        iii = ii*8
        jjj = jj*8
        q = 0
        r = 0
        while iii<(ii*8+N):
            while jjj<(jj*8+N):
                a = f_massive_red[q][r]
                b = f_massive_green[q][r]
                c = obratn[q][r]
                draw.point((iii,jjj),(a,b,c))
                r +=1
                jjj +=1
            r = 0
            q +=1
            iii +=1
            jjj = jj*8
image.save("image3.bmp", "BMP") #Сохраняем новое изображение
del draw #Удаляем инструмент
#ИЗВЛЕЧЕНИЕ
img = Image.open("image3.bmp", 'r')
w, h = img.size
w = int(w)
h = int(h)
img.transpose(Image.ROTATE_270).save("image3.bmp")
img = Image.open("image3.bmp", 'r')
img.transpose(Image.FLIP_LEFT_RIGHT).save("image3.bmp")
pix = []
pix = getPixels("image3.bmp")
pix = [pix[n:n+w] for n in range(0, w*h, w)]
pix = np.array(pix)
k = 0
slovo3 = []
for ii in range(int(h/8)):
    if k >= razmer: break
    for jj in range(int(w / 8)):
        if k >= razmer: break
        mas = pix[8 * ii:8 * (ii + 1), 8 * jj:8 * (jj + 1)]
        f_massive = [[] for i in range(8)]
        for j in range(8):
            for i in range(8):
                f_massive[j].append(mas[j][i][2])
        # прямое ДКП
        DCT_massive = [[] for i in range(N)]
        for i in range(N):
            for j in range(N):
                DCT_massive[i].append(((DCT(f_massive, N, i, j))))
        if k < razmer:
            for i in range(N):
                for j in range(N):
                    if k >= razmer: break
                    # if (i+j)>N: continue
                    DCT_massive[i][j] = int(DCT_massive[i][j] + (0.5 if DCT_massive[i][j] > 0 else -0.5))
                    if DCT_massive[i][j] % 2 != 0:
                        slovo3.append(1)
                        k += 1
                        continue
                    else:
                        slovo3.append(0)
                        k += 1
                        continue
        else:
            break
print(slovo3)
answer = ''
for i in range(razmer_1):
    bin_str = ''.join(str(x) for x in (slovo3[(i * 8):(i + 1) * 8]))
    answer += str(bytes([int(bin_str, base=2)]), 'cp1251')
print("Ваше спрятанное слово: " , answer)
pogr = 0
for i in range (razmer):
    if slovo2[i] != slovo3[i]:
        pogr +=1
print ('Погрешность при извлечении =', (pogr/razmer))
def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    # print('MSE', mse)
    print('RMSE', sqrt(mse))
    psnr = 20 * (math.log10(max_pixel / sqrt(mse)))
    print('PSNR', psnr)
    return psnr
img1 = cv2.imread('image2.bmp')
img2 = cv2.imread('image3.bmp')
PSNR(img1, img2)
time.sleep(100)