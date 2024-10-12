def cleanKreditBri (text) :
    kredit = (text.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

    kredit = kredit[:-2] + '.' + kredit[-2:]
    kredit = "{:,.2f}".format(float(kredit)) 
    
    return kredit