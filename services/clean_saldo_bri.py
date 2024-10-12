def cleanSaldoBri (text) :
    saldo = (text.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

    saldo = saldo[:-2] + '.' + saldo[-2:]
    saldo = "{:,.2f}".format(float(saldo)) 
    
    return saldo