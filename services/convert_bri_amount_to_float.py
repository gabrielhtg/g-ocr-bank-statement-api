def convertBriAmountToFloat(textAmount) :
    clean_number_str = textAmount.replace(",", "")
    
    return float(clean_number_str)