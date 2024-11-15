from format_currency import format_currency
from numpy import number

from services.utils.convert_to_float import convertToFloat

def briGetTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'tanggal_transaksi' : None,
        'uraian_transaksi' : None,
        'teller' : None,
        'debit' : None,
        'kredit' : None,
        'saldo' : None
    }

    for e in textData :
        currentRow = e['row']
    
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                if currentData['uraian_transaksi'] == None :
                    currentData['uraian_transaksi'] = e['text']
                    
                else :
                    currentData['uraian_transaksi'] = currentData['uraian_transaksi'] + ' ' + e['text']
                
            if e['col'] == 3 :
                if currentData['teller'] == None :
                    currentData['teller'] = e['text']
                    
            if e['col'] == 4 :
                currentData['debit'] = e['text']
                
            if e['col'] == 5 :
                currentData['kredit'] = e['text']
                
            if e['col'] == 6 :
                currentData['saldo'] = e['text']
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename
            rowDataArr.append(currentData.copy())
            currentData = {
                'tanggal_transaksi' : None,
                'uraian_transaksi' : None,
                'teller' : None,
                'debit' : None,
                'kredit' : None,
                'saldo' : None
            }
            
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                if currentData['uraian_transaksi'] == None :
                    currentData['uraian_transaksi'] = e['text']
                    
                else :
                    currentData['uraian_transaksi'] = currentData['uraian_transaksi'] + ' ' + e['text']
                
            if e['col'] == 3 :
                if currentData['teller'] == None :
                    currentData['teller'] = e['text']
                    
            if e['col'] == 4 :
                currentData['debit'] = e['text']
                
            if e['col'] == 5 :
                currentData['kredit'] = e['text']
                
            if e['col'] == 6 :
                currentData['saldo'] = e['text']
                
    currentData['filename'] = filename  
    rowDataArr.append(currentData.copy())
        
    return rowDataArr