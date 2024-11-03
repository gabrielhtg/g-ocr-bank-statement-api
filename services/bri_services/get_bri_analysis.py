import statistics

from services.bri_services.convert_bri_amount_to_float import convertBriAmountToFloat
from services.bri_services.convert_float_to_string_bri import convertFloatToFormattedStringBri

def getBriAnalysisData (transactionData, ch) :
    freqDebit = 0
    sumDebit = 0
    currentDebitAmount = None
    arrDebit = []
    minDebit = None
    maxDebit = 0
    
    freqKredit = 0
    sumKredit = 0
    currentKreditAmount = None
    arrKredit = []
    minKredit = None
    maxKredit = 0
    
    netBalance = 0
    
    for e in transactionData:
        if e[3] != '0.00' :
            freqDebit += 1
            
        if e[4] != '0.00' :
            freqKredit += 1
            
        
            
        # currentDebitAmount menyimpan nilai dalam bentuk float dari Debit
        currentDebitAmount = convertBriAmountToFloat(e[3])
        sumDebit += currentDebitAmount
        arrDebit.append(currentDebitAmount)
        
        if minDebit == None and currentDebitAmount > 0 :
            minDebit = currentDebitAmount
            
        elif minDebit != None:
            if currentDebitAmount < minDebit and currentDebitAmount > 0:
                minDebit = currentDebitAmount
            
            if currentDebitAmount > maxDebit :
                maxDebit = currentDebitAmount
            
        # currentKreditAmount menyimpan nilai dalam bentuk float dari Kredit
        currentKreditAmount = convertBriAmountToFloat(e[4])
        sumKredit += currentKreditAmount
        arrKredit.append(currentKreditAmount)
        
        if minKredit == None :
            minKredit = currentKreditAmount
            
        if currentKreditAmount < minKredit and currentKreditAmount > 0:
            minKredit = currentKreditAmount
            
        if currentKreditAmount > maxKredit:
            maxKredit = currentKreditAmount

    netBalance = sumKredit - sumDebit
    
    return {
        'freq_debit' : freqDebit,
        'sum_debit' : convertFloatToFormattedStringBri(sumDebit),
        'avg_debit' : convertFloatToFormattedStringBri(statistics.mean(arrDebit)),
        'min_debit' : convertFloatToFormattedStringBri(minDebit),
        'max_debit' : convertFloatToFormattedStringBri(maxDebit),
        'freq_kredit' : freqKredit,
        'sum_kredit' : convertFloatToFormattedStringBri(sumKredit),
        'avg_kredit' : convertFloatToFormattedStringBri(statistics.mean(arrKredit)),
        'min_kredit' : convertFloatToFormattedStringBri(minKredit),
        'max_kredit' : convertFloatToFormattedStringBri(maxKredit),
        'net_balance' : convertFloatToFormattedStringBri(netBalance)
    }
    