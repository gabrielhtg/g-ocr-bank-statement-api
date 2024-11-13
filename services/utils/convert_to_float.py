def convertToFloat (text: str) :
    if text == None :
      return None
    
    else:
      try :
        return float (text
                      .replace('.', '')
                      .replace(',', '')
                      .replace(' ', '')
                      .replace('DB', '')
                      .replace('O', '0')
                      .replace('o', '0')
                      .replace('Rp', '')
                      .replace('/', '')
                      .replace('l', '')
                      .replace('|', '')
                      .replace(']', '')
                      .replace('[', '')
                    ) / 100
      except ValueError as e:
        return float(0)