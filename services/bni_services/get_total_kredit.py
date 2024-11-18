from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def getTotalKredit(arrayDebet) :
    totalDebet = 0
    
    for e in arrayDebet :
        if e['debit_credit'] == 'K' :
            totalDebet += convertToFloat(e['amount'])

    return format_currency(totalDebet, currency_code='IDR')