def result(inp, outp, coded_text, frame='~'):
    # print result fgv
    print(frame * (len(inp) + 4))
    print(f'# {inp} #')
    print(f'# BlackBox Magic > {"ˇ" * len(coded_text)} #')
    print(f'# {outp} #')
    print(frame * (len(inp) + 4))


def tesztelt_szoveg():
    # input text fgv
    text = input('Nosza írj be egy tesztelendő szöveget!')
    palerinofu(text)

# def coding_rutin():

def palerinofu(text):
    # coding/decoding fgv

    code_dict = {
        "p": "a",
        "l": "e",
        "r": "i",
        "n": "o",
        "f": "u",
        "k": "ö",
        "t": "é",
        "s": "ü",
    }

    coded_text = ""
    inp = 'Vizsgált szöveg: ' + text
    for char in text:
        # print(char)

        for code in code_dict:
            if char == code_dict[code]:
                # print(f'érték: {char} == {code_dict[code]} <-ezt # ere-> {code}')
                decode = code
                break
            elif char.lower() == code_dict[code]:
                decode = code.upper()
                break

            elif char == code:
                # print(f'kulcs: {char} == {code} <-ezt # ere-> {code_dict[code]}')
                decode = code_dict[code]
                break
            elif char.lower() == code:
                decode = code_dict[code].upper()
                break

            else:
                # print(f'{char} változatlan marad (lefut az else) -> {char}')
                decode = char
        coded_text = coded_text + decode

    outp = '>>Kódolt szöveg: ' + coded_text
    result(inp, outp, coded_text)

    TryDeCod = input('Szeretnél egy ellenörző visszakódolást? (I / N)')
    answ = TryDeCod.upper()
    if answ == 'I':
        palerinofu(coded_text)

    exp_answ = ['I', 'N']
    while answ not in exp_answ:
        print(f'Nem megfelelő válasz "{TryDeCod}" ')
        TryDeCod = input('Lehetséges válasz: I vagy N:')
        answ = TryDeCod.upper()

        if answ == 'I':
            palerinofu(coded_text)

    else:
        print('Ok! A bizalom fontos! Hello!')
        #
        # one_more= input('Akarsz új tesztet? (I / N)')
        # answ = one_more.upper()
        #
        exit()


# keretfg meghívása
tesztelt_szoveg()
