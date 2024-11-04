from format_currency import format_currency
from numpy import number

def danamonGetTransactionData (textData) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'tanggal_transaksi' : None,
        'tanggal_valuta' : None,
        'keterangan' : None,
        'reff' : None,
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
                    float(int(e['text'].replace(',', '').replace('.', ''))/ 100),
                    currency_code='IDR'
                )
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(
                    float(int(e['text'].replace(',', '').replace('.', ''))/ 100),
                    currency_code='IDR'
                )
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(
                    float(int(e['text'].replace(',', '').replace('.', ''))/ 100),
                    currency_code='IDR'
                )
            
        else :
            beforeRow = currentRow
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
            currentData['uraian_transaksi'] = None
            
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
                
    rowDataArr.append(currentData.copy())
    return rowDataArr
            