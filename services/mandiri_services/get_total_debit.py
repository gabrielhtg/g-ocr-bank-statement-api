from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def getTotalDebit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['debit'] == None :
            continue
        
        else :
            totalDebet += convertToFloat(e['debit'])
            
    return format_currency(totalDebet, currency_code='IDR')