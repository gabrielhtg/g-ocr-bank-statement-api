from format_currency import format_currency

from services.utils.convert_to_float import convertToFloat

def mandiriGetTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = textData[0]['row']
    beforeRow = textData[0]['row']
    currentData = {
        'date_and_time' : None,
        'value_date' : None,
        'description' : None,
        'refference_no' : None,
        'debit' : None,
        'kredit' : None,
        'saldo' : None
    }
    
    for e in textData :
        currentRow = e['row']
        
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['date_and_time'] = e['text']
                
            if e['col'] == 2 :
                currentData['value_date'] = e['text']
                
            if e['col'] == 3 :
                if currentData['description'] == None :
                    currentData['description'] = e['text']
                    
                else :
                    currentData['description'] = currentData['description'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['refference_no'] = e['text']
                
            if e['col'] == 5 :
                currentData['debit'] = e['text']
                
            if e['col'] == 6 :
                currentData['kredit'] = e['text']
                
            if e['col'] == 7 :
                currentData['saldo'] = e['text']
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename 
            rowDataArr.append(currentData.copy())
            currentData = {
                'date_and_time' : None,
                'value_date' : None,
                'description' : None,
                'refference_no' : None,
                'debit' : None,
                'kredit' : None,
                'saldo' : None
            }
            
            if e['col'] == 1 :
                currentData['date_and_time'] = e['text']
                
            if e['col'] == 2 :
                currentData['value_date'] = e['text']
                
            if e['col'] == 3 :
                if currentData['description'] == None :
                    currentData['description'] = e['text']
                    
                else :
                    currentData['description'] = currentData['description'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['refference_no'] = e['text']
                
            if e['col'] == 5 :
                # print(e['text'])
                currentData['debit'] = e['text']
                
            if e['col'] == 6 :
                currentData['kredit'] = e['text']
                
            if e['col'] == 7 :
                currentData['saldo'] = e['text']
                
    currentData['filename'] = filename 
    rowDataArr.append(currentData.copy())
    # print(rowDataArr)
    # print()
    return rowDataArr
            