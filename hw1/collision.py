from random import randint
from sha48 import sha48


subDict = {
    ' ': [" ", "\t", "  ", "\t ", " \t", "   "],
    ';': [";", ",", ", ", " ,", "; ", " ;", " ; ", " , "],
    ':': [":", ": ", " :", " : ", "-", " -", "- ", " - "],
    '.': [".", ",", " .", ". ", " . ", ", ", " ,", " , "],
    'А': ["А", "A"],
    'В': ["В", "B"],
    'Е': ["Е", "E"],
    'М': ["М", "M"],
    'Н': ["Н", "H"],
    'С': ["С", "C"],
    'Т': ["Т", "T"],
    'а': ["а", "a"],
    'е': ["е", "e"],
    'к': ["к", "k"],
    'о': ["о", "o"],
    'р': ["р", "p"],
    'с': ["с", "c"],
    'у': ["у", "y"]
}


def numberOfCombinations(word):
    """Calculate number of combinations we can get according to substitution table"""
    n = 1
    for letter in word:
        if letter in subDict:
            n *= len(subDict[letter])
    return n


def generateSubstitution(sentence):
    """Generate new sentence according to substituion table"""
    new_sentence = []
    d = 1
    mask = 0
    for symbol in sentence:
        if symbol in subDict:
            index = randint(0, len(subDict[symbol]) - 1)
            subst_symbol = subDict[symbol][index]
            new_sentence.append(subst_symbol)
            mask += index * d
            d *= 10
        else:
            new_sentence.append(symbol)
    return (''.join(new_sentence), mask)


def findCollision(user_data, attacker_data, byte_number=6):
    """Find collision in SHA48"""
    userHashes = dict()
    for i in range(2**(byte_number * 4)):
        if i % 10000 == 0:
            print (i)
        (data, mask) = generateSubstitution(user_data)
        user_hash = sha48(data, byte_number)
        userHashes[user_hash] = mask
    found = False
    while not found:
        for i in range(2**(byte_number * 4)):
            if i % 10000 == 0:
                print (i)
            (data, mask) = generateSubstitution(attacker_data)
            attacker_hash = sha48(data, byte_number)
            if attacker_hash in userHashes:
                with open('user.txt', 'w+') as f:
                    f.write(recoverData(user_data, userHashes[attacker_hash]))
                with open('attacker.txt', 'w+') as f:
                    f.write(data)
                print ("Collision was found")
                found = True
                break


def recoverData(data, mask):
    """Recover data given initial value and mask."""
    recovered = []
    for symbol in data:
        if symbol in subDict:
            index = mask % 10
            mask = mask // 10
            recovered.append(subDict[symbol][index])
        else:
            recovered.append(symbol)
    return ''.join(recovered)


if __name__ == '__main__':
    user_data = "Получатель: Смышляев Станислав Витальевич; Сумма: 100.00; Адрес: город Москва"
    attacker_data = "Получатель: Емельянов Виталий Эдуардович; Сумма: 100.00; Адрес: город Долгопрудный"
    findCollision(user_data, attacker_data)
