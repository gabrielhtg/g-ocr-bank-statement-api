from format_currency import format_currency


def cleanNumber (number) :
    cleanedNumber = number.replace('.', '').replace(',', '')
    
    print(number)
    
    return format_currency(float(int(cleanedNumber) / 100), currency_code='IDR')