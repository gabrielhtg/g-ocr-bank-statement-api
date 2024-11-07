from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def getTotalDebit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['mutasi'] != None and 'DB' in e['mutasi'] :
            totalDebet += convertToFloat(e['mutasi'])
            
    return format_currency(totalDebet, currency_code='IDR')