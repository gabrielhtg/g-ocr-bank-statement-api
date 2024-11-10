from format_currency import format_currency
from numpy import number

from services.utils.convert_to_float import convertToFloat

def getTransactionData (textData, filename:str) :
    rowDataArr = []
    currentRow = 1
    beforeRow = 1
    currentData = {
        'tanggal_transaksi' : None,
        'tanggal_valuta' : None,
        'uraian_transaksi' : None,
        'nomor_cek' : None,
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
                if currentData['uraian_transaksi'] == None :
                    currentData['uraian_transaksi'] = e['text']
                    
                else :
                    currentData['uraian_transaksi'] = currentData['uraian_transaksi'] + ' ' + e['text']
            
            if e['col'] == 4 :
                currentData['nomor_cek'] = e['text']
                
            if e['col'] == 5 :
                currentData['debet'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
            
        else :
            beforeRow = currentRow
            currentData['filename'] = filename 
            
            if (
                currentData['tanggal_transaksi'] != None and
                currentData['uraian_transaksi'] != None
                ) :
                rowDataArr.append(currentData.copy())
                
            currentData = {
                'tanggal_transaksi' : None,
                'tanggal_valuta' : None,
                'uraian_transaksi' : None,
                'nomor_cek' : None,
                'debet' : None,
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
                currentData['nomor_cek'] = e['text']
                
            if e['col'] == 5 :
                currentData['debet'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 6 :
                currentData['kredit'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                
            if e['col'] == 7 :
                currentData['saldo'] = format_currency(convertToFloat(e['text']), currency_code='IDR')
                    
    currentData['filename'] = filename    
    if (
        currentData['tanggal_transaksi'] != None and
        currentData['uraian_transaksi'] != None
        ) :
        rowDataArr.append(currentData.copy())        
    return rowDataArr
            