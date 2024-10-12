import os
from services.correct_perspective import correct_perspective
from services.do_orc_easyocr import do_ocr_easyocr
from services.getImageHeight import getImageHeight
from services.getImageWidth import getImageWidth
from werkzeug.utils import secure_filename

from services.is_current_page_the_right_bank_statement_type import is_current_page_the_right_bank_statement_type

def do_ocr_bri (imageArray, app, bankStatementType) :
    # 4 data yang disimpan di bawah ini masih dummy
    # belum tentu digunakan
    # ! sementara ini tidak digunakan
    # tanggal_laporan = text_[8][1]
    # kepada_yth = text_[10][1]
    # periode_transaksi_start = text_[12][1]
    # periode_transaksi_end = text_[13][1]
    
    titikKiriTanggalTransaksi = None
    titikKananTanggalTransaksi = None

    titikKiriUraianTransaksi = None
    titikKananUraianTransaksi = None
    thresholdUraianTransaksi = None

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
    
    # digunakan untuk memeriksa apakah halaman yang diupload masih merupakan
    # tipe bank statement yang sama dengan yang dimasukkan user
    isBankStatementCorrect = False
    
    # merepresentasikan value dari gambar ke berapa saat ini yang dilakukan ocr
    banyakKataYangDiScan = 0
    
    for e in imageArray:
        if isinstance(e, str) :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correct_perspective(file_path)
            
        else :
            file = e
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            perspectiveCorrectedImage = correct_perspective(file_path)
        
        print('Processing', filename)
        
        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)

        # text_ merupakan semua teks hasil ocr dari gambar
        # tapi masih bukan hasil akhir
        text_ = do_ocr_easyocr(perspectiveCorrectedImage)

        for e in text_ :
            box, text, score = e
            
            banyakKataYangDiScan += 1
            
            if not isBankStatementCorrect:
                if banyakKataYangDiScan < 7 :
                    isBankStatementCorrect = is_current_page_the_right_bank_statement_type(bankStatementType, text)
                
            titikPalingKiriBox = box[0][0]
            titikPalingKananBox = box[1][0]
            titikPalingAtasBox = box[0][1]
            titikPalingBawahBox = box[2][1]
            
            # ini menyimpan data perbarisnya yang nanti akan dimasukkan ke dalam 
            # variable transaction data
            
            # melakukan pengecekan hingga nanti mendapatkan tabel transaksi
            if 'ance' in text.lower() and 'edit' in textBefore.lower() and 'osi' not in text.lower():
                startGetTransactionData = True
                continue
            
            # ketika sudah masuk ke bagian tabel transaksi, maka akan mulai mengambil data
            # dan block code ini akan dieksekusi
            if startGetTransactionData:
                if isSaldoVisited and titikPalingKiriBox > titikKiriKredit :
                    rowData.append(filename)
                    transactionData.append(rowData.copy())
                    rowData.clear()
                    startGetTransactionData = False
                    isTanggalTransaksiVisited = False
                    isUraianTransaksiVisited = False
                    isTellerVisited = False
                    isDebetVisited = False
                    isKreditVisited = False
                    isSaldoVisited = False
                    continue
                
                if len(transactionData) > 0 and 'aldo' in text.lower() and 'al' in text.lower() :
                    rowData.append(filename)
                    transactionData.append(rowData.copy())
                    rowData.clear()
                    startGetTransactionData = False
                    isTanggalTransaksiVisited = False
                    isUraianTransaksiVisited = False
                    isTellerVisited = False
                    isDebetVisited = False
                    isKreditVisited = False
                    isSaldoVisited = False
                    break
                
                if isTanggalTransaksiVisited and len(rowData) >= 6 and titikKananTanggalTransaksi < titikPalingKiriBox and titikPalingKananBox < titikKiriTeller :
                    rowData[1] = str(rowData[1]) + '\n' + text
                    titikKiriUraianTransaksi = titikPalingKiriBox
                    titikKananUraianTransaksi = titikPalingKananBox
                    
                if isTanggalTransaksiVisited and len(rowData) >= 6 and titikPalingKananBox < titikKiriUraianTransaksi:
                    rowData.append(filename)
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
                    thresholdUraianTransaksi = int(titikKananTanggalTransaksi + (0.272 * lebarGambar))
                    rowData.append(text)
                    isTanggalTransaksiVisited = True
                    
                elif not isUraianTransaksiVisited:
                    titikKiriUraianTransaksi = titikPalingKiriBox
                    titikKananUraianTransaksi = titikPalingKananBox
                    rowData.append(text)
                    isUraianTransaksiVisited = True
                    
                elif not isTellerVisited:
                    if titikPalingKiriBox > thresholdUraianTransaksi :
                        titikKiriTeller = titikPalingKiriBox
                        titikKananTeller = titikPalingKananBox
                        rowData.append(text)
                        isTellerVisited = True
                    
                    else:
                        rowData[1] = str(rowData[1]) + '\n' + text
                        titikKiriUraianTransaksi = titikPalingKiriBox
                        titikKananUraianTransaksi = titikPalingKananBox
                        
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
        
        if not isBankStatementCorrect :
            return 400
        
    return transactionData