"""
    Method ini digunakan untuk mengonversi nilai uang yang ada pada bank statement BRI
    dari yang semula FLOAT menjadi STRING yang sudah diformat sesuai dengan
    aturan penulisan uang di Indonesia
"""

def convertFloatToFormattedStringBri(number_float):
    return "{:,.2f}".format(number_float)