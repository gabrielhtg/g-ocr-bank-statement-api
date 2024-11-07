from format_currency import format_currency
from numpy import number

from services.utils.convert_to_float import convertToFloat

def bcaGetTransactionData (textData) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'tanggal' : None,
        'keterangan' : None,
        'cbg' : None,
        'mutasi' : None,
        'saldo' : None,
    }

    for e in textData :
        currentRow = e['row']
        
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['tanggal'] = e['text']
                
            if e['col'] == 2 :
                if currentData['keterangan'] == None :
                    currentData['keterangan'] = e['text']
                    
                else :
                    currentData['keterangan'] = currentData['keterangan'] + ' ' + e['text']
            
            if e['col'] == 3 :
                currentData['cbg'] = e['text']
                
            if e['col'] == 4 :
                if currentData['mutasi'] == None :
                    currentData['mutasi'] = e['text']
                    
                else :
                    currentData['mutasi'] = currentData['mutasi'] + ' ' + e['text']
                    
            if e['col'] == 5 :
                if currentData['saldo'] == None :
                    currentData['saldo'] = e['text']
                    
                else :
                    currentData['saldo'] = currentData['saldo'] + ' ' + e['text']
            
        else :
            beforeRow = currentRow
            
            if currentData['saldo'] != None :
                currentData['saldo'] = format_currency(convertToFloat(currentData['saldo']), country_code='IDR')
            
            if currentData['mutasi'] != None:
                if 'DB' in currentData['mutasi'] :
                    currentData['mutasi'] = format_currency(convertToFloat(currentData['mutasi']), country_code='IDR')  + ' ' +'DB'
                else : 
                    currentData['mutasi'] = format_currency(convertToFloat(currentData['mutasi']), country_code='IDR')

            rowDataArr.append(currentData.copy())
            currentData = {
                'tanggal' : None,
                'keterangan' : None,
                'cbg' : None,
                'mutasi' : None,
                'saldo' : None,
            }
            
            if e['col'] == 1 :
                currentData['tanggal'] = e['text']
                
            if e['col'] == 2 :
                if currentData['keterangan'] == None :
                    currentData['keterangan'] = e['text']
                    
                else :
                    currentData['keterangan'] = currentData['keterangan'] + ' ' + e['text']
            
            if e['col'] == 3 :
                currentData['cbg'] = e['text']
                
            if e['col'] == 4 :
                if currentData['mutasi'] == None :
                    currentData['mutasi'] = e['text']
                    
                else :
                    currentData['mutasi'] = currentData['mutasi'] + ' ' + e['text']
                
            if e['col'] == 5 :
                if currentData['saldo'] == None :
                    currentData['saldo'] = e['text']
                    
                else :
                    currentData['saldo'] = currentData['saldo'] + ' ' + e['text']
                    
    if currentData['saldo'] != None :
        currentData['saldo'] = format_currency(convertToFloat(currentData['saldo']), country_code='IDR')

    if currentData['mutasi'] != None:
        if 'DB' in currentData['mutasi'] :
            currentData['mutasi'] = format_currency(convertToFloat(currentData['mutasi']), country_code='IDR')  + ' ' +'DB'
        else : 
            currentData['mutasi'] = format_currency(convertToFloat(currentData['mutasi']), country_code='IDR')
            
    rowDataArr.append(currentData.copy())
    
    return rowDataArr
            