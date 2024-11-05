from format_currency import format_currency

def convertToIDR (text: str) :
    return format_currency(float(text.replace('.', '').replace(',', '')) / 100, currency_code='IDR')