from format_currency import format_currency

def getTotalKredit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['kredit'] == None :
            continue
        
        else :
            totalDebet += float(e['kredit'].replace('.', '').replace(',', '.').replace('Rp ', ''))
            
    return format_currency(totalDebet, currency_code='IDR')