from format_currency import format_currency
from numpy import number

from services.ocbc_services.clean_value import cleanValue
from services.utils.convert_to_float import convertToFloat

def ocbcGetTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = 1
    beforeRow = textData[0]['row']
    currentData = {
        'tanggal_transaksi' : None,
        'tanggal_valuta' : None,
        'uraian' : None,
        'debet' : None,
        'kredit' : None,
        'saldo' : None
    }

    for e in textData :
        currentRow = e['row']
    
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                currentData['tanggal_valuta'] = e['text']
                
            if e['col'] == 3 :
                if currentData['uraian'] == None :
                    currentData['uraian'] = e['text']
                    
                else :
                    currentData['uraian'] = currentData['uraian'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['debet'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
            if e['col'] == 5 :
                currentData['kredit'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['saldo'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename
            rowDataArr.append(currentData.copy())
            currentData = {
                'tanggal_transaksi' : None,
                'tanggal_valuta' : None,
                'uraian' : None,
                'debet' : None,
                'kredit' : None,
                'saldo' : None
            }
            currentData['uraian'] = None
            
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                currentData['tanggal_valuta'] = e['text']
                
            if e['col'] == 3 :
                if currentData['uraian'] == None :
                    currentData['uraian'] = e['text']
                    
                else :
                    currentData['uraian'] = currentData['uraian'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['debet'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
            if e['col'] == 5 :
                currentData['kredit'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['saldo'] = format_currency(convertToFloat(cleanValue(e['text'])), currency_code='IDR')
                
    currentData['filename'] = filename            
    rowDataArr.append(currentData.copy())
    return rowDataArr
            