from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def getTotalKredit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['kredit'] == None :
            continue
        
        else :
            totalDebet += convertToFloat(e['kredit'])
            
    return format_currency(totalDebet, currency_code='IDR')