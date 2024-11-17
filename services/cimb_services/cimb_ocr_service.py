import os
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.cimb_services.get_analysis_data import danamonAnalysisData
from services.cimb_services.get_total_debit import getTotalDebit
from services.cimb_services.get_total_kredit import getTotalKredit
from services.cimb_services.get_transaction_data import getTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.exception_handler import exceptionHandler
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrCimb (imageArray, app, bankStatementType) :
    page = 0
    data = {}
    currentRow = 0
    textData = []
    textWithCol = {}
    transactionData = []
    currentRow = 0
    
    pemilikRekening = None
    alamat = None
    periodeLaporan = None
    tanggalLaporan = None
    tanggalPembukaan = None
    nomorRekening = None
    namaProduk = None
    mataUang = None
    nomorCif = None

    thrKepada = None
    thbKepada = None
    thtKepada = None

    thrTanggalLaporan = None
    thtTanggalLaporan = None
    thbTanggalLaporan = None
    thlTanggalLaporan = None

    thrTanggalPembukaan = None
    thtTanggalPembukaan = None
    thbTanggalPembukaan = None
    thlTanggalPembukaan = None

    thrPeriodeLaporan = None
    thtPeriodeLaporan = None
    thbPeriodeLaporan = None
    thlPeriodeLaporan = None

    thrPeriode = None
    thtPeriode = None
    thbPeriode = None
    thlPeriode = None

    thrNomorRekening = None
    thtNomorRekening = None
    thbNomorRekening = None
    thlNomorRekening = None

    thrNamaProduk = None
    thtNamaProduk = None
    thbNamaProduk = None
    thlNamaProduk = None

    thrMataUang = None
    thtMataUang = None
    thbMataUang = None
    thlMataUang = None

    thrNomorCif = None
    thtNomorCif = None
    thbNomorCif = None
    thlNomorCif = None
    
    thbHeaderTable = None
    thbTable = None
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    thrTableCol5 = None
    thrTableCol6 = None
    thrTableCol7 = None
    
    nextPage = True
    
    countText = 0
    
    for e in imageArray:
        page += 1
        textData.clear()
        
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
            countText += 1
            bbox, text, score = e
    
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            rb = bbox[1][0]
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            cw = lb + int(abs(rb - lb) / 2)
            ch = tb + int(abs(bb - tb) / 2)
            
            if (
                ('bca' in text.lower() or
                'ocbc' in text.lower() or
                ('permata' in text.lower() and 'bank' in text.lower()) or
                'bni' in text.lower() or
                'bri' in text.lower() or
                'mandiri' in text.lower() or
                'danamon' in text.lower())
                and countText < 15
            ) :
                return exceptionHandler(
                    f'The type of bank statement detected is not the same as in the {filename} image! Please re-upload with the same type of bank statement or a clearer image.',
                    400,
                    None
                )
            
            if page == 1 :
                if 'epada' in text.lower() :
                    thbKepada = tb + int(0.19 * tinggiGambar)
                    thrKepada = lb + int(0.4 * lebarGambar)
                    thtKepada = bb
                    
                if 'gal' in text.lower() and 'oran' in text.lower() :
                    thrTanggalLaporan = lb + int(0.4 * lebarGambar)
                    thlTanggalLaporan = lb + int(0.151 * lebarGambar)
                    thbTanggalLaporan = tb + int(0.028 * tinggiGambar)
                    thtTanggalLaporan = tb
                    
                if 'gl' in text.lower() and 'uka' in text.lower() :
                    thrTanggalPembukaan = lb + int(0.4 * lebarGambar)
                    thlTanggalPembukaan = lb + int(0.151 * lebarGambar)
                    thbTanggalPembukaan = tb + int(0.028 * tinggiGambar)
                    thtTanggalPembukaan = tb
                    
                if 'eri' in text.lower() and 'ode' in text.lower() :
                    thrPeriode = lb + int(0.4 * lebarGambar)
                    thlPeriode = lb + int(0.151 * lebarGambar)
                    thbPeriode = tb + int(0.028 * tinggiGambar)
                    thtPeriode = tb
                    
                if 'en' in text.lower() and 'rek' in text.lower() :
                    thrNomorRekening = lb + int(0.48 * lebarGambar)
                    thlNomorRekening = lb + int(0.24 * lebarGambar)
                    thbNomorRekening = tb + int(0.018 * tinggiGambar)
                    thtNomorRekening = tb
                    
                if 'cif' in text.lower() or 'if' in text.lower() :
                    thrNomorCif = lb + int(0.48 * lebarGambar)
                    thlNomorCif = lb + int(0.24 * lebarGambar)
                    thbNomorCif = tb + int(0.018 * tinggiGambar)
                    thtNomorCif = tb
                    
                if 'ata' in text.lower() and 'uan' in text.lower() :
                    thrMataUang = lb + int(0.48 * lebarGambar)
                    thlMataUang = lb + int(0.24 * lebarGambar)
                    thbMataUang = tb + int(0.018 * tinggiGambar)
                    thtMataUang = tb
                    
                if 'ama' in text.lower() and 'duk' in text.lower() :
                    thrNamaProduk = lb + int(0.48 * lebarGambar)
                    thlNamaProduk = lb + int(0.24 * lebarGambar)
                    thbNamaProduk = tb + int(0.018 * tinggiGambar)
                    thtNamaProduk = tb
                    
                if thrKepada != None:
                    if (
                        (cw < thrKepada) 
                        and (ch <= thbKepada) 
                        and (ch >= thtKepada)
                    ) :
                        if pemilikRekening == None :
                            pemilikRekening = text
                            
                        else :
                            if alamat == None:
                                alamat = text
                            
                            else :
                                alamat = alamat + ' ' + text
                
                if thrTanggalLaporan != None:
                    if (
                        (cw > thlTanggalLaporan) 
                        and (ch <= thbTanggalLaporan) 
                        and (ch >= thtTanggalLaporan)
                    ) :
                        if tanggalLaporan == None :
                            tanggalLaporan = text
                            
                if thrNamaProduk != None:
                    if (
                        (cw > thlNamaProduk) 
                        and (ch <= thbNamaProduk) 
                        and (ch >= thtNamaProduk)
                    ) :
                        if namaProduk == None :
                            namaProduk = text
                            
                if thrTanggalPembukaan != None:
                    if (
                        (cw > thlTanggalPembukaan) 
                        and (ch <= thbTanggalPembukaan) 
                        and (ch >= thtTanggalPembukaan)
                    ) :
                        if tanggalPembukaan == None :
                            tanggalPembukaan = text
                            
                if thrPeriode != None:
                    if (
                        (cw > thlPeriode) 
                        and (ch <= thbPeriode) 
                        and (ch >= thtPeriode)
                    ) :
                        if periodeLaporan == None :
                            periodeLaporan = text.strip()
                            
                        else :
                            periodeLaporan = periodeLaporan + ' - ' + text.strip()
                            
                if thrNomorRekening != None:
                    if (
                        (cw > thlNomorRekening) 
                        and (ch <= thbNomorRekening) 
                        and (ch >= thtNomorRekening)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text
                            
                if thrNomorCif != None:
                    if (
                        (cw > thlNomorCif) 
                        and (ch <= thbNomorCif) 
                        and (ch >= thtNomorCif)
                    ) :
                        if nomorCif == None :
                            nomorCif = text
                            
                if thrMataUang != None:
                    if (
                        (cw > thlMataUang) 
                        and (ch <= thbMataUang) 
                        and (ch >= thtMataUang)
                    ) :
                        if mataUang == None :
                            mataUang = text
                
            if (
                ('ter' in text.lower() and 'as' in text.lower()) or
                ('ma' in text.lower() and 'kas' in text.lower())
                ) :
                    break
            
            try :        
                if 'rai' in text.lower() and 'tran' in text.lower() and currentRow == 0:
                    thbHeaderTable = tb + int(0.028 * tinggiGambar)
                    thbTable = tb + int(0.575 * tinggiGambar)
                    thrTableCol1 = rb - int(0.16 * tinggiGambar)
                    thrTableCol2 = thrTableCol1 + int(0.08 * tinggiGambar)
                    thrTableCol3 = thrTableCol2 + int(0.18 * tinggiGambar)
                    thrTableCol4 = thrTableCol3 + int(0.07 * tinggiGambar)
                    thrTableCol5 = thrTableCol4 + int(0.09 * tinggiGambar)
                    thrTableCol6 = thrTableCol5 + int(0.08 * tinggiGambar)
                    
                if thbHeaderTable != None and tb > thbHeaderTable and bb < thbTable :
                    if currentRow == 0 :
                        currentRow += 1
                    
                    if (cw < thrTableCol1) :
                        if 'total' in text.lower() :
                            thbTable = tb
                            nextPage = False
                            continue
                        
                        currentRow += 1    
                        textWithCol['col'] = 1
                        textWithCol['row'] = currentRow
                    
                    if (cw > thrTableCol1 and cw < thrTableCol2) :
                        textWithCol['col'] = 2
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol2 and cw < thrTableCol3) :
                        textWithCol['col'] = 3
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol3 and cw < thrTableCol4) :
                        textWithCol['col'] = 4
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol4 and cw < thrTableCol5) :
                        textWithCol['col'] = 5
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol5 and cw < thrTableCol6) :
                        textWithCol['col'] = 6
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol6) :
                        textWithCol['col'] = 7
                        textWithCol['row'] = currentRow
                        
                    textWithCol['text'] = text
                        
                    textData.append(textWithCol.copy())
            
            except TypeError as e:
                return exceptionHandler(
                    f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
                    400,
                    e
                )
            
            except ValueError as e:
                return exceptionHandler(
                    f'An error occurred with image {filename}. Try rephotographing this image more clearly!',
                    400,
                    e
                ) 
        # if not isBankStatementCorrect :
        #     return 400
        
        transactionData.extend(getTransactionData(textData, filename))
        
        if nextPage == False :
            break
    
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['periode_laporan'] = periodeLaporan
    data['tanggal_laporan'] = tanggalLaporan
    data['tanggal_pembukaan'] = tanggalPembukaan
    data['nomor_rekening'] = nomorRekening
    data['nama_produk'] = namaProduk
    data['nomor_cif'] = nomorCif
    data['mata_uang'] = mataUang
    data['transaction_data'] = transactionData
    data['total_debet'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = danamonAnalysisData(data['transaction_data'])
    return data