def cPrint(str, pType=1, pColor=35):
    print(f'\033[{pType};{pColor}m{str}\033[0m')
