from services import correct_perspective, getImageHeight, getImageWidth
from services.do_orc_easyocr import do_ocr_easyocr


def do_ocr_bri (imageArray) :
    for e in imageArray:
        perspectiveCorrectedImage = correct_perspective(e)

        # text_ merupakan semua teks hasil ocr dari gambar
        # tapi masih bukan hasil akhir
        text_ = do_ocr_easyocr(perspectiveCorrectedImage)

        # 4 data yang disimpan di bawah ini masih dummy
        # belum tentu digunakan
        tanggal_laporan = text_[8][1]
        kepada_yth = text_[10][1]
        periode_transaksi_start = text_[12][1]
        periode_transaksi_end = text_[13][1]
        
        titikKiriTanggalTransaksi = None
        titikKananTanggalTransaksi = None

        titikKiriUraianTransaksi = None
        titikKananUraianTransaksi = None

        titikKiriTeller = None
        titikKananTeller = None

        titikKiriDebet = None
        titikKananDebet = None

        titikKiriKredit = None
        titikKananKredit = None

        titikKiriSaldo = None
        titikKananSaldo = None

        startGetTransactionData = False

        # text sebelumnya (-1 iterasi saat ini)
        textBefore = None

        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)

        # menyimpan semua data transaksi
        transactionData = []
        rowData = []

        # menyimpan visited state pada tiap kolom yang ada pada tabel transaksi
        isTanggalTransaksiVisited = False
        isUraianTransaksiVisited = False
        isTellerVisited = False
        isDebetVisited = False
        isKreditVisited = False
        isSaldoVisited = False

        for e in text_ :
            box, text, score = e
            
            titikPalingKiriBox = box[0][0]
            titikPalingKananBox = box[1][0]
            titikPalingAtasBox = box[0][1]
            titikPalingBawahBox = box[2][1]
            
            # ini menyimpan data perbarisnya yang nanti akan dimasukkan ke dalam 
            # variable transaction data
            
            # melakukan pengecekan hingga nanti mendapatkan tabel transaksi
            if 'balance' in text.lower() and 'credit' in textBefore.lower():
                startGetTransactionData = True
                continue
            
            # ketika sudah masuk ke bagian tabel transaksi, maka akan mulai mengambil data
            # dan block code ini akan dieksekusi
            if startGetTransactionData:
                
                if isSaldoVisited and titikPalingKiriBox > titikKiriKredit :
                    transactionData.append(rowData.copy())
                
                if isTanggalTransaksiVisited and len(rowData) >= 6 and titikKananTanggalTransaksi <= titikPalingKiriBox and titikPalingKananBox <= titikKiriTeller :
                    rowData[1] = str(rowData[1]) + '\n' + text
                    titikKiriUraianTransaksi = titikPalingKiriBox
                    titikKananUraianTransaksi = titikPalingKananBox
                    
                if isTanggalTransaksiVisited and len(rowData) >= 6 and titikPalingKananBox < titikKiriUraianTransaksi:
                    transactionData.append(rowData.copy())
                    rowData.clear()
                    isTanggalTransaksiVisited = False
                    isUraianTransaksiVisited = False
                    isTellerVisited = False
                    isDebetVisited = False
                    isKreditVisited = False
                    isSaldoVisited = False
                    
                    # memasukkan data
                    titikKiriTanggalTransaksi = titikPalingKiriBox
                    titikKananTanggalTransaksi = titikPalingKananBox
                    rowData.append(text)
                    isTanggalTransaksiVisited = True
                    continue
                    
                if not isTanggalTransaksiVisited:
                    titikKiriTanggalTransaksi = titikPalingKiriBox
                    titikKananTanggalTransaksi = titikPalingKananBox
                    rowData.append(text)
                    isTanggalTransaksiVisited = True
                    
                elif not isUraianTransaksiVisited:
                    titikKiriUraianTransaksi = titikPalingKiriBox
                    titikKananUraianTransaksi = titikPalingKananBox
                    rowData.append(text)
                    isUraianTransaksiVisited = True
                    
                elif not isTellerVisited:
                    titikKiriTeller = titikPalingKiriBox
                    titikKananTeller = titikPalingKananBox
                    rowData.append(text)
                    isTellerVisited = True
                    
                elif not isDebetVisited:
                    titikKiriDebet = titikPalingKiriBox
                    titikKananDebet = titikPalingKananBox
                    rowData.append(text)
                    isDebetVisited = True
                    
                elif not isKreditVisited:
                    titikKiriKredit = titikPalingKiriBox
                    titikKananKredit = titikPalingKananBox
                    rowData.append(text)
                    isKreditVisited = True
                    
                elif not isSaldoVisited:
                    titikKiriSaldo = titikPalingKiriBox
                    titikKananSaldo = titikPalingKananBox
                    rowData.append(text)
                    isSaldoVisited = True
                
            textBefore = text
            
        