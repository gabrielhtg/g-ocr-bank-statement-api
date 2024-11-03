import statistics
from format_currency import format_currency

from services.bri_services.convert_float_to_string_bri import convertFloatToFormattedStringBri
from services.permata_services.convert_to_float import convertToFloat

def permataAnalysisData (transactionData) :
    freqDebit = 0
    arrDebit = []
    
    freqKredit = 0
    arrKredit = []
    
    for e in transactionData :
        if e['debet'] != None :
            freqDebit += 1
            convertedDebet = convertToFloat(e['debet'])
            arrDebit.append(convertedDebet)
            
        
        if e['kredit'] != None :
            freqKredit += 1
            convertedKredit = convertToFloat(e['kredit'])
            arrKredit.append(convertedKredit)
    
    return {
        'freq_debit' : freqDebit,
        'sum_debit' : format_currency(sum(arrDebit), currency_code='IDR'),
        'avg_debit' : format_currency(statistics.mean(arrDebit), currency_code='IDR'),
        'min_debit' : format_currency(min(arrDebit), currency_code='IDR'),
        'max_debit' : format_currency(max(arrDebit), currency_code='IDR'),
        'freq_kredit' : freqKredit,
        'sum_kredit' : format_currency(sum(arrKredit), currency_code='IDR'),
        'avg_kredit' : format_currency(statistics.mean(arrKredit), currency_code='IDR'),
        'min_kredit' : format_currency(min(arrKredit), currency_code='IDR'),
        'max_kredit' : format_currency(max(arrKredit), currency_code='IDR'),
        'net_balance' : format_currency(sum(arrKredit) - sum(arrDebit), currency_code='IDR')
    }
    