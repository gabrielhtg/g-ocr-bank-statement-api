from format_currency import format_currency
from numpy import number

from services.utils.format_string_money_amount import convertToIDR

def bniGetTransactionData (textData) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'posting_date' : None,
        'effective_date' : None,
        'branch' : None,
        'journal': None,
        'transaction_description' : None,
        'amount' : None,
        'debit_credit' : None,
        'balance' : None,
    }

    for e in textData :
        currentRow = e['row']
    
        if (beforeRow == currentRow) :
            if e['col'] == 1 :
                currentData['posting_date'] = e['text']
                
            if e['col'] == 2 :
                currentData['effective_date'] = e['text']
                
            if e['col'] == 3 :
                currentData['branch'] = e['text']
                
            if e['col'] == 4 :
                currentData['journal'] = e['text']
                
            if e['col'] == 5 :
                if currentData['transaction_description'] == None :
                    currentData['transaction_description'] = e['text']
                    
                else :
                    currentData['transaction_description'] = currentData['transaction_description'] + ' ' + e['text']
                
            if e['col'] == 6 :
                currentData['amount'] = convertToIDR(e['text'])
                
            if e['col'] == 7 :
                currentData['debit_credit'] = e['text']
                
            if e['col'] == 8 :
                currentData['balance'] = convertToIDR(e['text'])
            
        else :
            beforeRow = currentRow
            rowDataArr.append(currentData.copy())
            currentData = {
                'posting_date' : None,
                'effective_date' : None,
                'branch' : None,
                'journal': None,
                'transaction_description' : None,
                'amount' : None,
                'debit_credit' : None,
                'balance' : None,
            }
            currentData['transaction_description'] = None
            
            if e['col'] == 1 :
                currentData['posting_date'] = e['text']
                
            if e['col'] == 2 :
                currentData['effective_date'] = e['text']
                
            if e['col'] == 3 :
                currentData['branch'] = e['text']
                
            if e['col'] == 4 :
                currentData['journal'] = e['text']
                
            if e['col'] == 5 :
                if currentData['transaction_description'] == None :
                    currentData['transaction_description'] = e['text']
                    
                else :
                    currentData['transaction_description'] = currentData['transaction_description'] + ' ' + e['text']
                
            if e['col'] == 6 :
                currentData['amount'] = convertToIDR(e['text'])
                
            if e['col'] == 7 :
                currentData['debit_credit'] = e['text']
                
            if e['col'] == 8 :
                currentData['balance'] = convertToIDR(e['text'])
                
    rowDataArr.append(currentData.copy())
    return rowDataArr
            