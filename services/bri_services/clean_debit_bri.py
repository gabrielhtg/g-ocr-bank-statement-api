def cleanDebitBri (text) :
    debit = (text.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

    debit = debit[:-2] + '.' + debit[-2:]
    debit = "{:,.2f}".format(float(debit)) 
    
    return debit