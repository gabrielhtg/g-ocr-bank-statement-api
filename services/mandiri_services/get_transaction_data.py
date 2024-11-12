from format_currency import format_currency
from numpy import number

from services.utils.convert_to_float import convertToFloat

def mandiriGetTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = 1
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
                print(e['text'])
                currentData['debit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
            
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
                currentData['debit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
        
    currentData['filename'] = filename            
    rowDataArr.append(currentData.copy())
    return rowDataArr
            