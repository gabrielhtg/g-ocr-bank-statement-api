from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def getTotalKredit(arrayDebet) :
    totalKredit = 0
    
    for e in arrayDebet :
        if e['mutasi'] != None and 'DB' not in e['mutasi'] :
            totalKredit += convertToFloat(e['mutasi'])
        
    return format_currency(totalKredit, currency_code='IDR')