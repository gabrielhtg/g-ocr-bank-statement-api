from format_currency import format_currency
from numpy import number

from services.utils.convert_to_float import convertToFloat

def danamonGetTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = textData[0]['row']
    beforeRow = textData[0]['row']
    currentData = {
        'tanggal_transaksi' : None,
        'tanggal_valuta' : None,
        'keterangan' : None,
        'reff' : None,
        'debit' : None,
        'kredit' : None,
        'saldo' : None,
        'filename' : None
    }

    for e in textData :
        currentRow = e['row']
        
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                currentData['tanggal_valuta'] = e['text']
                
            if e['col'] == 3 :
                if currentData['keterangan'] == None :
                    currentData['keterangan'] = e['text']
                    
                else :
                    if 'total' not in e['text'].lower() :
                        currentData['keterangan'] = currentData['keterangan'] + ' ' + e['text']
                        
                    else :
                        break
            
            if e['col'] == 4 :
                currentData['reff'] = e['text']
                
            if e['col'] == 5 :
                currentData['debit'] = format_currency(
                    convertToFloat(e['text']),
                    currency_code='IDR'
                )
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(
                    convertToFloat(e['text']),
                    currency_code='IDR'
                )
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(
                    convertToFloat(e['text']),
                    currency_code='IDR'
                )
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename
            rowDataArr.append(currentData.copy())
            currentData = {
                'tanggal_transaksi' : None,
                'tanggal_valuta' : None,
                'keterangan' : None,
                'reff' : None,
                'debit' : None,
                'kredit' : None,
                'saldo' : None
            }
            
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                currentData['tanggal_valuta'] = e['text']
                
            if e['col'] == 3 :
                if currentData['keterangan'] == None :
                    currentData['keterangan'] = e['text']
                    
                else :
                    if 'total' not in e['text'].lower() :
                        currentData['keterangan'] = currentData['keterangan'] + ' ' + e['text']
                        
                    else :
                        break
            
            if e['col'] == 4 :
                currentData['reff'] = e['text']
                
            if e['col'] == 5 :
                currentData['debit'] = e['text']
                
            if e['col'] == 6 :
                currentData['kredit'] = e['text']
                
            if e['col'] == 7 :
                currentData['saldo'] = e['text']
    
    currentData['filename'] = filename            
    rowDataArr.append(currentData.copy())
    return rowDataArr
            