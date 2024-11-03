def convertToFloat (stringNum: str) :
    return float(
            int(stringNum.replace('Rp ', '').replace(',', '').replace('.', '')) / 100
        ) 