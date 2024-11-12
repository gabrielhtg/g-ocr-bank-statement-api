import os

from services.bri_services.clean_debit_bri import cleanDebitBri
from services.bri_services.clean_kredit_bri import cleanKreditBri
from services.bri_services.clean_saldo_bri import cleanSaldoBri
from services.bri_services.clean_summary_bri import cleanSummaryBri
from services.bri_services.clean_tanggal_transaksi_bri import cleanTanggalTransaksiBri
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.exception_handler import exceptionHandler
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth
from services.utils.is_current_page_the_right_bank_statement_type import isCurrentPageTheRightBankStatementType;

from werkzeug.utils import secure_filename

def doOcrBri (imageArray, app, bankStatementType) :
    # 4 data yang disimpan di bawah ini masih dummy
    # belum tentu digunakan
    # ! sementara ini tidak digunakan
    # tanggal_laporan = text_[8][1]
    # kepada_yth = text_[10][1]
    # periode_transaksi_start = text_[12][1]
    # periode_transaksi_end = text_[13][1]
    
    titikKananTanggalTransaksi = None

    titikKiriUraianTransaksi = None
    thresholdUraianTransaksi = None

    titikKiriTeller = None


    titikKiriKredit = None

    # saklar yang kita gunakan untuk pengumpulan data transaksi
    startGetTransactionData = False
    
    # saklar yang kita gunakan untuk pengumpulan summary dari gambar
    startGetSummary = False
    
    # ini digunakan untuk menghitung banyak data summary yang sudah dilakukan OCR
    # sejak kode ini dibuat, maksimal ada 4 
    summaryDataCount = 0
    
    # text sebelumnya (-1 iterasi saat ini)
    textBefore = None

    # menyimpan semua data transaksi
    transactionData = []
    rowData = []
    summaryData = []

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
    
    pemilikRekening = None
    tanggalLaporan = None
    periodeTransaksi = None
    alamat = None
    nomorRekening = None
    namaProduk = None
    valuta = None
    unitKerja = None
    alamatUnitKerja = None

    thrBox = None
    thbBox = None

    thbAlamat = None

    thrTanggalLaporan = None
    thlTanggalLaporan = None
    thbTanggalLaporan = None

    thrPeriodeTransaksi = None
    thlPeriodeTransaksi = None
    thbPeriodeTransaksi = None
    thtPeriodeTransaksi = None

    thrNomorRekening = None
    thlNomorRekening = None
    thbNomorRekening = None
    thtNomorRekening = None

    thrUnitKerja = None
    thlUnitKerja = None
    thbUnitKerja = None
    thtUnitKerja = None

    thrAlamatUnitKerja = None
    thlAlamatUnitKerja = None
    thbAlamatUnitKerja = None
    thtAlamatUnitKerja = None

    thrNamaProduk = None
    thlNamaProduk = None
    thbNamaProduk = None
    thtNamaProduk = None

    thrValuta = None
    thlValuta = None
    thbValuta = None
    thtValuta = None
    
    data = {}
    page = 0
    
    for e in imageArray:
        page += 1
        if isinstance(e, str) :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        else :
            file = e
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            perspectiveCorrectedImage = correctPerspective(file_path)
        
        print('Processing', filename)
        
        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)

        # text_ merupakan semua teks hasil ocr dari gambar
        # tapi masih bukan hasil akhir
        text_ = doEasyOcr(perspectiveCorrectedImage)

        for e in text_ :
            box, text, score = e
            
            banyakKataYangDiScan += 1
            
            if not isBankStatementCorrect:
                if banyakKataYangDiScan < 7 :
                    isBankStatementCorrect = isCurrentPageTheRightBankStatementType(bankStatementType, text)
                
            lb = box[0][0]
            rb = box[1][0]
            tb = box[0][1]
            bb = box[2][1]
            
            if page == 1 : 
                if 'epada' in text.lower() :
                    thrBox = lb + int(0.328 * lebarGambar)
                    continue
                
                # pengecekan tanggal laporan    
                if 'gal' in text.lower() and 'oran' in text.lower() :
                    thrTanggalLaporan = lb + int(0.228 * lebarGambar)
                    thlTanggalLaporan = lb + int(0.128 * lebarGambar)
                    thbTanggalLaporan = tb + int(0.02 * tinggiGambar)
                    
                # pengecekan periode transaksi
                if 'ode' in text.lower() and 'sak' in text.lower() :
                    thrPeriodeTransaksi = lb + int(0.228 * lebarGambar)
                    thlPeriodeTransaksi = lb + int(0.128 * lebarGambar)
                    thbPeriodeTransaksi = tb + int(0.025 * tinggiGambar)
                    thtPeriodeTransaksi = tb - int(0.0005 * tinggiGambar)
                    
                if 'no' in text.lower() and 'rek' in text.lower() :
                    thrNomorRekening = lb + int(0.24 * lebarGambar)
                    thlNomorRekening = lb + int(0.123 * lebarGambar)
                    thbNomorRekening = tb + int(0.025 * tinggiGambar)
                    thtNomorRekening = tb - int(0.0005 * tinggiGambar)
                    
                if 'ma' in text.lower() and 'prod' in text.lower() :
                    thrNamaProduk = lb + int(0.24 * lebarGambar)
                    thlNamaProduk = lb + int(0.123 * lebarGambar)
                    thbNamaProduk = tb + int(0.025 * tinggiGambar)
                    thtNamaProduk = tb - int(0.0005 * tinggiGambar)
                    
                if 'uta' in text.lower() and 'val' in text.lower() :
                    thrValuta = lb + int(0.24 * lebarGambar)
                    thlValuta = lb + int(0.123 * lebarGambar)
                    thbValuta = tb + int(0.025 * tinggiGambar)
                    thtValuta = tb - int(0.0005 * tinggiGambar)
                    
                if 'nit' in text.lower() and 'erj' in text.lower() and 'mat' not in text.lower():
                    thrUnitKerja = lb + int(0.4 * lebarGambar)
                    thlUnitKerja = lb + int(0.128 * lebarGambar)
                    thbUnitKerja = tb + int(0.023 * tinggiGambar)
                    thtUnitKerja = tb - int(0.0005 * tinggiGambar)
                    
                if 'nit' in text.lower() and 'erj' in text.lower() and 'mat' in text.lower():
                    thrAlamatUnitKerja = lb + int(0.4 * lebarGambar)
                    thlAlamatUnitKerja = lb + int(0.128 * lebarGambar)
                    thbAlamatUnitKerja = tb + int(0.023 * tinggiGambar)
                    thtAlamatUnitKerja = tb - int(0.0005 * tinggiGambar)
                
                # pengecekan alamat dan pemilik rekening
                if thrBox != None :
                    if rb < thrBox :
                        if pemilikRekening == None :
                            pemilikRekening = text
                            
                        elif pemilikRekening != None :
                            if alamat == None :
                                alamat = text
                                thbAlamat = bb + int(0.0005 * tinggiGambar)
                            
                            elif thbAlamat >= tb :
                                alamat = alamat + ' ' + text
                    
                if (thrTanggalLaporan != None) :
                    if (lb > thlTanggalLaporan) and (bb <= thbTanggalLaporan) :
                        tanggalLaporan = text
                        
                if thrPeriodeTransaksi != None :
                    if (lb > thlPeriodeTransaksi) and (bb <= thbPeriodeTransaksi) and (tb >= thtPeriodeTransaksi) :
                        if periodeTransaksi == None :
                            periodeTransaksi = text
                            
                        else :
                            periodeTransaksi = periodeTransaksi + ' - ' + text
                            
                if thrNomorRekening != None: 
                    if (lb > thlNomorRekening) and (bb <= thbNomorRekening) and (tb >= thtNomorRekening) and (rb <= thrNomorRekening):
                        nomorRekening = text
                        
                if thrNamaProduk != None: 
                    if (lb > thlNamaProduk) and (bb <= thbNamaProduk) and (tb >= thtNamaProduk) and (rb <= thrNamaProduk):
                        namaProduk = text
                        
                if thrUnitKerja != None: 
                    if (lb > thlUnitKerja) and (bb <= thbUnitKerja) and (tb >= thtUnitKerja) and (rb <= thrUnitKerja):
                        unitKerja = text
                        
                if thrValuta != None: 
                    if (lb > thlValuta) and (bb <= thbValuta) and (tb >= thtValuta) and (rb <= thrValuta):
                        valuta = text
                        
                if thrAlamatUnitKerja != None: 
                    if (lb > thlAlamatUnitKerja) and (bb <= thbAlamatUnitKerja) and (tb >= thtAlamatUnitKerja) and (rb <= thrAlamatUnitKerja):
                        if alamatUnitKerja == None:
                            alamatUnitKerja = text
                            
                        else :
                            alamatUnitKerja = alamatUnitKerja + ' ' + text
            
            # ini menyimpan data perbarisnya yang nanti akan dimasukkan ke dalam 
            # variable transaction data
            
            # melakukan pengecekan hingga nanti mendapatkan tabel transaksi
            if 'ance' in text.lower() and 'edit' in textBefore.lower() and 'osi' not in text.lower():
                startGetTransactionData = True
                continue
            
            # ketika sudah masuk ke bagian tabel transaksi, maka akan mulai mengambil data
            # dan block code ini akan dieksekusi
            if startGetTransactionData:
                
                # ini adalah kondisi ketika sudah masuk ke akhir halaman
                if isSaldoVisited and lb > titikKiriKredit :
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
                    continue
                
                if isTanggalTransaksiVisited and len(rowData) >= 6 and titikKananTanggalTransaksi < lb and rb < titikKiriTeller :
                    rowData[1] = str(rowData[1]) + '\n' + text
                    titikKiriUraianTransaksi = lb
                    titikKananUraianTransaksi = rb
                    
                if isTanggalTransaksiVisited and len(rowData) >= 6 and rb < titikKiriUraianTransaksi:
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
                    titikKiriTanggalTransaksi = lb
                    titikKananTanggalTransaksi = rb
                    rowData.append(cleanTanggalTransaksiBri(text))
                    isTanggalTransaksiVisited = True
                    continue
                    
                if not isTanggalTransaksiVisited:
                    titikKiriTanggalTransaksi = lb
                    titikKananTanggalTransaksi = rb
                    thresholdUraianTransaksi = int(titikKananTanggalTransaksi + (0.272 * lebarGambar))
                    rowData.append(cleanTanggalTransaksiBri(text))
                    isTanggalTransaksiVisited = True
                    
                elif not isUraianTransaksiVisited:
                    titikKiriUraianTransaksi = lb
                    titikKananUraianTransaksi = rb
                    rowData.append(text)
                    isUraianTransaksiVisited = True
                    
                elif not isTellerVisited:
                    if lb > thresholdUraianTransaksi :
                        titikKiriTeller = lb
                        titikKananTeller = rb
                        rowData.append(text)
                        isTellerVisited = True
                    
                    else:
                        rowData[1] = str(rowData[1]) + '\n' + text
                        titikKiriUraianTransaksi = lb
                        titikKananUraianTransaksi = rb
                        
                elif not isDebetVisited:
                    titikKiriDebet = lb
                    titikKananDebet = rb
                    try : 
                        rowData.append(cleanDebitBri(text))
                    except ValueError as e :
                        return exceptionHandler(
                            f'Gambar {filename} - Gagal melakukan cleaning data pada debet ketika text = {text}',
                            400,
                            e
                        )
                        
                    isDebetVisited = True
                    
                elif not isKreditVisited:
                    titikKiriKredit = lb
                    titikKananKredit = rb
                    try : 
                        rowData.append(cleanKreditBri(text))
                    except ValueError as e :
                        return exceptionHandler(
                            f'Gambar {filename} - Gagal melakukan cleaning data pada kredit ketika text = {text}',
                            400,
                            e
                        )
                    isKreditVisited = True
                    
                elif not isSaldoVisited:
                    titikKiriSaldo = lb
                    titikKananSaldo = rb
                    try : 
                        rowData.append(cleanSaldoBri(text))
                    except ValueError as e :
                        return exceptionHandler(
                            f'Gambar {filename} - Gagal melakukan cleaning data pada saldo ketika text = {text}',
                            400,
                            e
                        )
                    
                    isSaldoVisited = True
                
            textBefore = text
            
            if 'sing' in text.lower() and 'ance' in text.lower() :
                startGetSummary = True 
                continue
            
            if startGetSummary :
                summaryDataCount += 1
                summaryData.append(cleanSummaryBri(text))
                
                if summaryDataCount == 4 :
                    break
                
            if 'bilang' in text.lower() :
                startGetSummary = False
                continue
            
        if not isBankStatementCorrect :
            return 400
    
    data['pemilik_rekening'] = pemilikRekening
    data['tanggal_laporan'] = tanggalLaporan
    data['periode_transaksi'] = periodeTransaksi
    data['alamat'] = alamat
    data['nomor_rekening'] = nomorRekening
    data['nama_produk'] = namaProduk
    data['valuta'] = valuta
    data['unit_kerja'] = unitKerja
    data['alamat_unit_kerja'] = alamatUnitKerja
    data['transaction_data'] = transactionData
    data['summary_data'] = summaryData
    
    return data