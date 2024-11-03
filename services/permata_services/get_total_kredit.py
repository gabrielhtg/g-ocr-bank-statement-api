from format_currency import format_currency

def getTotalKredit (arrayKredit) :
    totalKredit = 0
    
    for e in arrayKredit :
        if e['kredit'] == None :
            continue
        
        else :
            try :
                totalKredit += float(e['kredit'].replace('.', '').replace(',', '.').replace('Rp ', ''))
            except ValueError :
                continue
                            
    return format_currency(totalKredit, currency_code='IDR')