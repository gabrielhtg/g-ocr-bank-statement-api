from services.permata_services.clean_number import cleanNumber

def getTransactionData (textData, filename) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'tanggal_transaksi' : None,
        'tanggal_valuta' : None,
        'uraian_transaksi' : None,
        'debet': None,
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
                if currentData['uraian_transaksi'] == None :
                    currentData['uraian_transaksi'] = e['text']
                    
                else :
                    currentData['uraian_transaksi'] = currentData['uraian_transaksi'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['debet'] = cleanNumber(e['text'])
                
            if e['col'] == 5 :
                currentData['kredit'] = cleanNumber(e['text'])
                
            if e['col'] == 6 :
                currentData['saldo'] = cleanNumber(e['text'])
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename   
            rowDataArr.append(currentData.copy())
            currentData = {
                'tanggal_transaksi' : None,
                'tanggal_valuta' : None,
                'uraian_transaksi' : None,
                'debet': None,
                'kredit' : None,
                'saldo' : None
            }
            currentData['uraian_transaksi'] = None
            
            if e['col'] == 1 :
                currentData['tanggal_transaksi'] = e['text']
                
            if e['col'] == 2 :
                currentData['tanggal_valuta'] = e['text']
                
            if e['col'] == 3 :
                if currentData['uraian_transaksi'] == None :
                    currentData['uraian_transaksi'] = e['text']
                    
                else :
                    currentData['uraian_transaksi'] = currentData['uraian_transaksi'] + ' ' + e['text']
            
            if e['col'] == 4 :
                if currentData['debet'] != None :
                    currentData['debet'] = cleanNumber(e['text'])
                
            if e['col'] == 5 :
                if currentData['kredit'] != None:
                    currentData['kredit'] = cleanNumber(e['text'])
                
            if e['col'] == 6 :
                currentData['saldo'] = cleanNumber(e['text'])
    
    currentData['filename'] = filename   
    rowDataArr.append(currentData.copy())           
    return rowDataArr