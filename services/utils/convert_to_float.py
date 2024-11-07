def convertToFloat (text: str) :
    if text == None :
      return None
    
    else:
      return float (text
                    .replace('.', '')
                    .replace(',', '')
                    .replace(' ', '')
                    .replace('DB', '')
                    .replace('O', '0')
                    .replace('o', '0')
                    .replace('Rp', '')
                  ) / 100