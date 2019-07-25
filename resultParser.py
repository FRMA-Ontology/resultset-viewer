
def text2IRI(value):
    value = value.lower().replace(' ', '-')
    uriReservedCharacters = [":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=", "%"]

    final = ""
    for c in value:
        if c in uriReservedCharacters:
            final = final + "%" + str(hex(ord(c)).replace('0x', ''))
        else:
            final = final + str(c)

    return final

def loadResultSet(testName, algorithmName, filepath):
    iri = text2IRI(testName)

    print('testName = ' + iri)
    return ''
