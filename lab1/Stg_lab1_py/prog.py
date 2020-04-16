def search3(oldSymb, newSymb):
    fOut = open("output.txt", "r", encoding='utf-8')
    i = 0
    k = 0
    massBit = []
    symbol = fOut.read(1);

    while symbol:
        if symbol == oldSymb:
            massBit.append(0)
            i += 1
            k += 1
        elif symbol == newSymb:
            massBit.append(1)
            k += 1
        if k % 11 == 0 and i != 11:
            i = 0
        elif k % 11 == 0 and i == 11:
            break
        symbol = fOut.read(1);
    ourWord = "".join(chr(int("".join(map(str, massBit[i:i+11])), 2)) for i in range(0, len(massBit), 11))
    print(ourWord)
    fOut.close()

def search2():
    fOut = open("output.txt", "r", encoding='utf-8')
    i = 0
    k = 0
    massBit = []
    symbol = fOut.read(1);



    while symbol:
        if symbol == chr(32):
            symbol = fOut.read(1);
            if symbol == chr(32):
                massBit.append(1)
                k += 1
            else:
                massBit.append(0)
                i += 1
                k += 1
        if k % 11 == 0 and i != 11:
            i = 0
        elif k % 11 == 0 and i == 11:
            break
        symbol = fOut.read(1);
    ourWord = "".join(chr(int("".join(map(str, massBit[i:i+11])), 2)) for i in range(0, len(massBit), 11))
    print(ourWord)
    fOut.close()


def replace3(s, oldSymb, newSymb):
    fIn = open("input.txt", "r", encoding='utf-8')
    fOut = open("output.txt", "w", encoding='utf-8')
    i = 0
    symbol = fIn.read(1);
    while symbol:
        if i < len(s) and (symbol == oldSymb or symbol == newSymb):
            if s[i] == '1':
                fOut.write(newSymb)
            else:
                fOut.write(oldSymb)
            i += 1
        elif i == len(s) and (symbol == oldSymb or symbol == newSymb):
            fOut.write(oldSymb)
        else:
            fOut.write(symbol)
        symbol = fIn.read(1);
    if i < len(s):
        print('Нужен контейнер побольше')
    fOut.close()
    fIn.close()

def replace2(s):
    fIn = open("input.txt", "r", encoding='utf-8')
    fOut = open("output.txt", "w", encoding='utf-8')
    i = 0
    symbol = fIn.read(1);
    while symbol:
        if i < len(s) and (symbol == chr(32)):
            if s[i] == '1':
                fOut.write(chr(32)+chr(32))
            else:
                fOut.write(chr(32))
            i += 1
        elif i == len(s) and (symbol == chr(32)):
            fOut.write(chr(32))
        else:
            fOut.write(symbol)
        symbol = fIn.read(1);
    if i < len(s):
        print('Нужен контейнер побольше')
    fOut.close()
    fIn.close()

# def replace1(s, oldSymb0, newSymb0, oldSymb1, newSymb1):
#     fIn = open("input.txt", "r", encoding='utf-8')
#     fOut = open("output.txt", "w", encoding='utf-8')
#     i = 0
#     symbol = fIn.read(1);
#     while symbol:
#         for i in range(0,len(s),1):
#             if i < len(s) and (symbol == oldSymb0):
#                 if s[i] == '0':
#                     fOut.write(newSymb0)
#
#             elif i < len(s) and (symbol == oldSymb1):
#                 if s[i] == '1':
#                     fOut.write(newSymb1)
#
#             elif i == len(s) and (symbol == oldSymb0):
#                 if s[i] == '0':
#                     fOut.write(newSymb0)
#
#             elif i == len(s) and (symbol == oldSymb1):
#                 if s[i] == '1':
#                     fOut.write(newSymb1)
#
#             symbol = fIn.read(1);
#     if i < len(s):
#         print('Нужен контейнер побольше')
#     fOut.close()
#     fIn.close()

tmp = (input("1 - Спрятать слово; 2 - Найти слово\n"))
if not tmp:
    exit('wrong input')
task = int(tmp)
if not task or task<1 or task>2:
    exit('wrong input')

tmp = (input("Введите 1, 2 или 3 в зависимости от метода \n 1 - Замена русской 'е' на английскую \n 2 - Добавление второго пробела \n 3 - Замена пунктуации \n"))
if not tmp:
    exit('wrong input')

stegoType = (int)(tmp)
if not stegoType or stegoType < 1 or stegoType > 3:
    exit('wrong input')

if task == 1:
    word = input("Введите слово: \n")
    while not word:
        word = input("Введите слово: \n")
    binWord = ''.join(format(ord(i), 'b') for i in word)
    if stegoType == 1:
        replace3(binWord, 'е', 'E')
    elif stegoType == 2:
        replace2(binWord)
    elif stegoType == 3:
        replace3(binWord, '—', '-')
elif task == 2:
    if stegoType == 1:
        search3('е', 'E')
    elif stegoType == 2:
        search2()
    elif stegoType == 3:
        search3('—', '-')