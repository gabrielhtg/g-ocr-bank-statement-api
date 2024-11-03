def cleanSummaryBri (text) :
    summaryText = (text.replace(' ', '')
                         .replace(',', '')
                         .replace('o', '0')
                         .replace('O', '0')
                         .replace('.', ''))

    summaryText = summaryText[:-2] + '.' + summaryText[-2:]
    summaryText = "{:,.2f}".format(float(summaryText)) 
    
    return summaryText