def cleanTanggalTransaksiBri(text) : 
    if '.' in text :
        return text.replace('.', ':').replace('*', ':').replace(',', ':')
    
    elif ',' in text :
        return text.replace('.', ':').replace('*', ':').replace(',', ':')
    
    else :
        return text