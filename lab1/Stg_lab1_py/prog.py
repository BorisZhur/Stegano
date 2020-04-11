def search(oldSymb, newSymb):
    fOut = open("output.txt", "r", encoding='utf-8')
    i = 0
    k = 0
    massBit = []
    symbol = fOut.read(1);

    while symbol:
        if symbol == oldSymb:
            massBit.append(0)
            #print(massBit)
            i += 1
            k += 1
        elif symbol == newSymb:
            massBit.append(1)
            #print(massBit)
            k += 1
        if k % 11 == 0 and i != 11:
            i = 0
        elif k % 11 == 0 and i == 11:
            break
        symbol = fOut.read(1);
    #print(massBit)
    #print(massBit[0:(len(massBit) - 11)])
    ourWord = "".join(chr(int("".join(map(str, massBit[i:i+11])), 2)) for i in range(0, len(massBit), 11))
    print(ourWord)
    fOut.close()

def replace(s, oldSymb, newSymb):
    #заменяем русскую оrigneSymb на newSymb
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



task = int(input("1 - Спрятать слово; 2 - Найти слово\n"))
if task<1 or task>2:
    exit('wrong input')

stegoType = (int)(input("Введите 1, 2 или 3 в зависимости от метода текстовой стеганографии. \n 1 - Прямая замена символов \n 2 - Добавление дополнительных пробелов \n 3 - Добавление служебных символов (замена пунктуации) \n"))
if stegoType < 1 or stegoType > 3:
    exit('wrong input')

if task == 1:
    word = input("Введите слово - ")
    binWord = ''.join(format(ord(i), 'b') for i in word)
    #print(binWord)
    if stegoType == 1:
        replace(binWord, 'е', 'E')
    elif stegoType == 2:
        replace(binWord, chr(32), chr(9))
    elif stegoType == 3:
        replace(binWord, '—', '-')
elif task == 2:
    if stegoType == 1:
        search('е', 'E')
    elif stegoType == 2:
        search(chr(32), chr(9))
    elif stegoType == 3:
        search('—', '-')