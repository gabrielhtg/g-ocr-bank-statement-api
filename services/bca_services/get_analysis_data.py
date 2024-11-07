import statistics
from format_currency import format_currency

def getAnalysisData (transactionData) :
    freqDebit = 0
    arrDebit = []
    
    freqKredit = 0
    arrKredit = []
    
    for e in transactionData :
        if e['debit'] != None :
            freqDebit += 1
            convertedDebet = float(e['debit'].replace(',', '').replace('.', '').replace('Rp ', '')) / 100
            arrDebit.append(convertedDebet)
            
        
        if e['kredit'] != None :
            freqKredit += 1
            convertedKredit = float(e['kredit'].replace(',', '').replace('.', '').replace('Rp ', '')) / 100
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
    