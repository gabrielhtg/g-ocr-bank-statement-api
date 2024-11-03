from format_currency import format_currency

def getTotalDebet(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['debet'] == None :
            continue
        
        else :
            totalDebet += float(e['debet'].replace('.', '').replace(',', '.').replace('Rp ', ''))
            
    return format_currency(totalDebet, currency_code='IDR')