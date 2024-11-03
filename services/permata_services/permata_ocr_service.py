import os
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename

from services.permata_services.analysis_data import permataAnalysisData
from services.permata_services.get_total_debet import getTotalDebet
from services.permata_services.get_total_kredit import getTotalKredit
from services.permata_services.get_transaction_data import getTransactionData
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrPermata (imageArray, app, bankStatementType) :
    pemilikRekening = None
    alamat = None
    periodeLaporan = None
    tanggalLaporan = None
    noCif = None
    nomorRekening = None
    cabang = None
    namaProduk = None
    mataUang = None

    thrKepada = None
    thbKepada = None
    thtKepada = None

    thrPeriodeLaporan = None
    thtPeriodeLaporan = None
    thbPeriodeLaporan = None
    thlPeriodeLaporan = None

    thrTanggalLaporan = None
    thtTanggalLaporan = None
    thbTanggalLaporan = None
    thlTanggalLaporan = None

    thrNomorCif = None
    thtNomorCif = None
    thbNomorCif = None
    thlNomorCif = None

    thrNomorRekening = None
    thtNomorRekening = None
    thbNomorRekening = None
    thlNomorRekening = None

    thrCabang = None
    thtCabang = None
    thbCabang = None
    thlCabang = None

    thrNamaProduk = None
    thtNamaProduk = None
    thbNamaProduk = None
    thlNamaProduk = None

    thrMataUang = None
    thtMataUang = None
    thbMataUang = None
    thlMataUang = None
    
    page = 0
    
    data = {}
    thbHeaderTable = None
    thbTable = None
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    thrTableCol5 = None
    
    textWithCol = {}    
    textData = []
    
    currentRow = 0

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
            bbox, text, score = e
    
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            current_width = bbox[1][0] - bbox[0][0]
            rb = bbox[0][0] + current_width
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            
            if page == 1 :
                if 'epada' in text.lower() :
                    thbKepada = tb + int(0.08 * tinggiGambar)
                    thrKepada = lb + int(0.328 * lebarGambar)
                    thtKepada = tb
                    continue
                
                if 'ode' in text.lower() and 'lap' in text.lower() :
                    thrPeriodeLaporan = lb + int(0.4 * lebarGambar)
                    thlPeriodeLaporan = lb + int(0.143 * lebarGambar)
                    thbPeriodeLaporan = tb + int(0.025 * tinggiGambar)
                    thtPeriodeLaporan = tb - int(0.002 * tinggiGambar)
                    
                if 'no' in text.lower() and 'rek' in text.lower():
                    thrNomorRekening = lb + int(0.4 * lebarGambar)
                    thlNomorRekening = lb + int(0.124 * lebarGambar)
                    thbNomorRekening = tb + int(0.025 * tinggiGambar)
                    thtNomorRekening = tb - int(0.002 * tinggiGambar)  
                    
                if 'abang' in text.lower() :
                    thrCabang = lb + int(0.4 * lebarGambar)
                    thlCabang = lb + int(0.124 * lebarGambar)
                    thbCabang = tb + int(0.025 * tinggiGambar)
                    thtCabang = tb - int(0.002 * tinggiGambar)  
                    
                if 'ma' in text.lower() and 'pro' in text.lower() :
                    thrNamaProduk = lb + int(0.4 * lebarGambar)
                    thlNamaProduk = lb + int(0.124 * lebarGambar)
                    thbNamaProduk = tb + int(0.025 * tinggiGambar)
                    thtNamaProduk = tb - int(0.002 * tinggiGambar)
                    
                if 'ma' in text.lower() and 'ang' in text.lower() and rb < int(0.5 * lebarGambar) :
                    thrMataUang = lb + int(0.4 * lebarGambar)
                    thlMataUang = lb + int(0.124 * lebarGambar)
                    thbMataUang = tb + int(0.025 * tinggiGambar)
                    thtMataUang = tb - int(0.002 * tinggiGambar)
                    
                if 'no' in text.lower() and '.c' in text.lower() :
                    thrNomorCif = lb + int(0.4 * lebarGambar)
                    thlNomorCif = lb + int(0.124 * lebarGambar)
                    thbNomorCif = tb + int(0.025 * tinggiGambar)
                    thtNomorCif = tb - int(0.002 * tinggiGambar)
                    
                    # cv.line(
                    #         img,
                    #         (thrNomorCif, tb),
                    #         (thrNomorCif, thbNomorCif),
                    #         (0, 255, 0),
                    #         2
                    #     )
                    
                if 'gal' in text.lower() and 'oran' in text.lower() :
                    thrTanggalLaporan = lb + int(0.4 * lebarGambar)
                    thlTanggalLaporan = lb + int(0.143 * lebarGambar)
                    thbTanggalLaporan = tb + int(0.025 * tinggiGambar)
                    thtTanggalLaporan = tb - int(0.002 * tinggiGambar)
                    
                if thbNamaProduk != None:
                    if (
                        (lb > thlNamaProduk) 
                        and (bb <= thbNamaProduk) 
                        and (tb >= thtNamaProduk)
                    ) :
                        if namaProduk == None :
                            namaProduk = text
                                
                if thbNomorCif != None:
                    if (
                        (lb > thlNomorCif) 
                        and (bb <= thbNomorCif) 
                        and (tb >= thtNomorCif)
                    ) :
                        if noCif == None :
                            noCif = text
                            
                if thbMataUang != None:
                    if (
                        (lb > thlMataUang) 
                        and (bb <= thbMataUang) 
                        and (tb >= thtMataUang)
                    ) :
                        if mataUang == None :
                            mataUang = text
                
                if thbNomorRekening != None:
                    if (lb > thlNomorRekening) and (bb <= thbNomorRekening) and (tb >= thtNomorRekening) :
                        if nomorRekening == None :
                            nomorRekening = text
                            
                if thbCabang != None:
                    if (lb > thlCabang) and (bb <= thbCabang) and (tb >= thtCabang) :
                        if cabang == None :
                            cabang = text
                    
                if thbKepada != None:
                    if (lb < thrKepada and bb < thbKepada and tb > thtKepada) :
                        if (pemilikRekening == None) :
                            pemilikRekening = text
                            
                        else :
                            if (alamat == None) :
                                alamat = text
                                
                            else :
                                alamat = alamat + ' ' + text
                                
                if thrPeriodeLaporan != None :
                    if (lb > thlPeriodeLaporan) and (bb <= thbPeriodeLaporan) and (tb >= thtPeriodeLaporan) :
                        if periodeLaporan == None :
                            periodeLaporan = text
                            
                        else :
                            periodeLaporan = periodeLaporan + ' - ' + text
                
                if (thrTanggalLaporan != None) :
                    if (lb > thlTanggalLaporan) and (bb <= thbTanggalLaporan) and (tb >= thtTanggalLaporan) :
                        if tanggalLaporan == None :
                            tanggalLaporan = text
                            
                        else :
                            tanggalLaporan = tanggalLaporan + ' - ' + text
            
            if 'gl' in text.lower() and 'rx' in text.lower() and currentRow == 0:
                thbHeaderTable = tb + int(0.041 * tinggiGambar)
                thbTable = tb + int(0.575 * tinggiGambar)
                thrTableCol1 = rb + int(0.01 * tinggiGambar)
                thrTableCol2 = rb + int(0.067 * tinggiGambar)
                thrTableCol3 = rb + int(0.246 * tinggiGambar)
                thrTableCol4 = rb + int(0.363 * tinggiGambar)
                thrTableCol5 = rb + int(0.48 * tinggiGambar)
                
            if thbHeaderTable != None and tb > thbHeaderTable and bb < thbTable :
                if currentRow == 0 :
                    currentRow += 1

                textWithCol['text'] = text
                
                if (rb < thrTableCol1) :
                    currentRow += 1    
                    textWithCol['col'] = 1
                    textWithCol['row'] = currentRow
                
                if (lb > thrTableCol1 and rb < thrTableCol2) :
                    textWithCol['col'] = 2
                    textWithCol['row'] = currentRow
                    
                if (lb > thrTableCol2 and rb < thrTableCol3) :
                    textWithCol['col'] = 3
                    textWithCol['row'] = currentRow
                    
                if (lb > thrTableCol3 and rb < thrTableCol4) :
                    textWithCol['col'] = 4
                    textWithCol['row'] = currentRow
                    
                if (lb > thrTableCol4 and rb < thrTableCol5) :
                    textWithCol['col'] = 5
                    textWithCol['row'] = currentRow
                    
                if (lb > thrTableCol5) :
                    textWithCol['col'] = 6
                    textWithCol['row'] = currentRow
                    
                textData.append(textWithCol.copy())
        # if not isBankStatementCorrect :
        #     return 400
    
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['periode_laporan'] = periodeLaporan
    data['tanggal_laporan'] = tanggalLaporan
    data['nomor_rekening'] = nomorRekening
    data['cabang'] = cabang
    data['nama_produk'] = namaProduk
    data['mata_uang'] = mataUang
    data['no_cif'] = noCif
    data['transaction_data'] = getTransactionData(textData)
    data['total_debet'] = getTotalDebet(data['transaction_data'])
    data['total_kredit'] = getTotalKredit(data['transaction_data'])
    data['analytics_data'] = permataAnalysisData(data['transaction_data'])
    return data