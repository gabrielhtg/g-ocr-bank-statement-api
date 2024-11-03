from format_currency import format_currency


def cleanNumber (number) :
    cleanedNumber = number.replace('.', '').replace(',', '')
    
    return format_currency(float(int(cleanedNumber) / 100), currency_code='IDR')