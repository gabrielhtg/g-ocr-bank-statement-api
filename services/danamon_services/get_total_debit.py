from format_currency import format_currency

def getTotalDebit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['debit'] == None :
            continue
        
        else :
            totalDebet += float(e['debit'].replace('.', '').replace(',', '.').replace('Rp ', ''))
            
    return format_currency(totalDebet, currency_code='IDR')