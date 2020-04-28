import  numpy
import math
import cv2

from PIL import Image, ImageDraw

inp = "input.bmp"

def toBits (num):
    a = bin(num)[2:]
    if num == 32:
        a = '00000' + a

    return a

def calcPNSR(k):
    old = cv2.imread("input.bmp")
    changed = cv2.imread("output.bmp", 1)
    psnrcv = cv2.PSNR(old, changed)
    print('psnr(',k,') = ', psnrcv)

def change(curBit, num):
    if num + 1 == 256:
        num -= 2
    if (num % 2) == 1:
        num -= 1
    return num + int(curBit)

def seek():
    image = Image.open("output.bmp")
    w = image.size[0]
    h = image.size[1]
    pixels = image.load()
    massBit = []
    endFlag = 0
    leaveFlag = 0
    for i in range(w):
        for j in range(h):
            currentPix = (pixels[i, j][0]) % 2
            massBit.append(currentPix)
            if currentPix == 0:
                endFlag += 1
                if endFlag == 11:
                    leaveFlag = 1
                    break
            elif currentPix == 1:
                endFlag = 0
            elif endFlag == 11:
                leaveFlag = 1
                break

        if leaveFlag == 1:
            break
    #print(massBit)
    result = "".join(chr(int("".join(map(str, massBit[i:i + 11])), 2)) for i in range(0, len(massBit), 11))
    print(result)


def hide(wrd):
    image = Image.open(inp)
    draw = ImageDraw.Draw(image)
    w = image.size[0]
    h = image.size[1]
    pixels = image.load()
    if (len(wrd)>w*h):
        print("Нужен контейнер побольше")
        exit(0)
    l=0
    for i in range(w):
        for j in range(h):
            p = []
            if l<len(wrd):
                p.append(int(change(wrd[l],pixels[i,j][0])))
                #print(p)
            else:
                p.append(int(pixels[i,j][0]))
            p.append(int(pixels[i, j][1]))
            p.append(int(pixels[i, j][2]))
            draw.point((i, j), (p[0],p[1],p[2]))
            l += 1
    image.save("output.bmp", "BMP")

    del draw

findType = input("Вы хотите встроить слово? д/н\n")
if findType == 'н':
        seek()
elif findType=='д':
    word = input("Введите слово - ")
    #k = input("Количество слов - ")
    ls = [1,2,3,5,10,20,30,40,50]
    for k in ls:
        wordInBin = ''.join(str(toBits(ord(i))) for i in word)
        for j in range(int(k)-1):
            wordInBin += ''.join(str(toBits(ord(i))) for i in word)
        #wordInBin = ''.join(str(toBits(ord(i))) for i in word)+'00000000000'
        hide(wordInBin+'00000000000')
        calcPNSR(k)
else:
    print('wrong input')
    exit(0)