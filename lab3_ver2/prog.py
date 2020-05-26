import cv2

from cv2 import dct, idct
from PIL import Image
import numpy as np

def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num

#insertion = 'Привет всем! Меня зовут Катя, я выполнила третью лабораторную работу по стеганографии'
insertion = str(input("Введите слово "))
insertion2 = ''
for code in insertion.encode('cp1251'):
    a = bin(code)[2:]
    while len(a) < 8:
        a = '0' + a
    insertion2 += a
#print('начальное', insertion2)


image = Image.open("img.bmp") #Открываем изображение.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
obj = image.load()

image1 = Image.open("img1.bmp")
obj1 = image1.load()
pix = np.array(image.getdata(1))
pix = pix.reshape(height,width)
len_ins = 0
for i in range(int(height / 8)):
    for j in range(int(width / 8)):
        matrix = np.array(pix[8 * i:8 * (i + 1), 8 * j:8 * (j + 1)])
        matrix = matrix.astype('float32')
        dct_coef = dct(matrix)
        if (len_ins < len(insertion2)):
            for k in range(8):
                for l in range(8):
                    #print(dct_coef[k][k])
                    if (len_ins < len(insertion2)):
                        dct_coef[k][l] = (round(dct_coef[k][l]))
                        if (dct_coef[k][l] % 2 != int(insertion2[len_ins])):
                            # print(dct_coef[k][k])
                            # print(insertion2[len_ins])
                            dct_coef[k][l] -= 1
                        else:
                            print('оставляем как есть', dct_coef[k][k], insertion2[len_ins])
                    len_ins += 1
            print(idct(dct_coef))
            dct_coef[0][0] = dct_coef[0][0]/4
            new_matrix = [round(x) for x in idct(dct_coef).reshape(1,64)[0]]
            print('new matrix', new_matrix)
            for h in range(0, 64):
                rel_x = h // 8
                rel_y = h % 8
                x = list(obj[j * 8 + rel_y, i * 8 + rel_x])
                x[1] = new_matrix[h]
                obj1[j * 8 + rel_y, i * 8 + rel_x] = tuple(x)

image1.save("tmp.bmp", "BMP")

message_bin = []
#Cчитывание сообщения
pix1 = np.array(image1.getdata(1))
pix1 = pix1.reshape(height,width)
len_ins = 0
for i in range(int(height / 8)):
    for j in range(int(width / 8)):
        matrix1 = np.array(pix1[8 * i:8 * (i + 1), 8 * j:8 * (j + 1)])
        #print(matrix)
        matrix1 = matrix1.astype('float32')
        dct_coef = dct(matrix1)
        if (len_ins < len(insertion2)):
            for k in range(8):
                for l in range(8):
                    if (len_ins < len(insertion2)):
                        dct_coef[k][l] = (round(dct_coef[k][l]))
                        if (dct_coef[k][l] % 2 == 1):
                            message_bin.append(1)
                        else:
                            message_bin.append(0)
                    len_ins += 1

answer = ''

for i in range(len(insertion)):
    bin_str = ''.join(str(x) for x in (message_bin[(i * 8):(i + 1) * 8]))
    if bin_str == '10011000':
        answer += ' '
    else:
        answer += str(bytes([int(bin_str, base=2)]), 'cp1251')
print("Ваше сообщение - " , answer)

check = ''.join(str(x) for x in (message_bin))

#подсчет кол-ва ошибок
number_of_mistakes = 0
for l in range(len(insertion2)):
    if insertion2[l] != check[l]:
        number_of_mistakes += 1
print('При передаче допущено %d ошибок' % number_of_mistakes)


print('Ошибочно передано %f процентов сообщения ' % (100.*(float(number_of_mistakes)/ len(insertion2))))
