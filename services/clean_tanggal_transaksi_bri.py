def clean_tanggal_transaksi_bri(text) : 
    if '.' in text :
        return text.replace('.', ':').replace('*', ':').replace(',', ':')