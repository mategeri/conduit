def result(inp, outp, coded_text, frame='~'):
    # print result fgv
    print(frame * (len(inp) + 4))
    print(f'# {inp} #')
    print(f'# BlackBox Magic > {"ˇ" * len(coded_text)} #')
    print(f'# {outp} #')
    print(frame * (len(inp) + 4))


def coding_rutin(text):
    # kódolási rutin fgv
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
    One_more('DC_again', coded_text)


def One_more(goal, coded_text):
    match goal:
        case 'DC_again':
            Qu = ['DC', 'Szeretnél egy ellenörző visszakódolást?']
        case 'Text_again':
            Qu = ['TxT', 'Titkosítsunk még egy szót?']

    I_v_N = input(f'{Qu[1]} (I / N)')

    answ = I_v_N.upper()
    if answ == 'I':
        match Qu[0]:
            case 'DC':
                coding_rutin(coded_text)
            case 'TxT':
                titkositas()

    exp_answ = ['I', 'N']

    while answ not in exp_answ:
        print(f'Nem megfelelő a válasz "{I_v_N}" ')
        I_v_N = input('Lehetséges válasz: I vagy N:')
        answ = I_v_N.upper()
        if answ == 'I':
            match Qu[0]:
                case 'DC':
                    coding_rutin(coded_text)
                case 'TxT':
                    titkositas()
    else:
        match Qu[0]:
            case 'DC':
                print('\nOk! A bizalom fontos!')
                One_more('Text_again', '')
            case 'TxT':
                print('\nRendben. Hello!')
                exit()


def titkositas():
    # input text
    text = input('Nosza írj be egy tesztelendő szöveget!')
    coding_rutin(text)


### keretfg meghívása
titkositas()
