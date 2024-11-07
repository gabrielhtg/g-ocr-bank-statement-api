import os
from matplotlib.dviread import Page
from format_currency import format_currency
from werkzeug.utils import secure_filename

from services.bca_services.get_analysis_data import getAnalysisData
from services.bca_services.get_total_debit import getTotalDebit
from services.bca_services.get_total_kredit import getTotalKredit
from services.bca_services.get_transaction_data import bcaGetTransactionData
from services.utils.convert_to_float import convertToFloat
from services.utils.correct_perspective import correctPerspective
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrBca (imageArray, app, bankStatementType) :
    page = 0
    data = {}
    
    cabang = None
    pemilikRekening = None
    alamat = None
    nomorRekening = None
    periode = None
    mataUang = None
    saldoAwal = None
    saldoAkhir = None
    mutasiKredit = None
    mutasiDebit = None
    totalMutasiKredit = None
    totalMutasiDebit = None

    thrCabang = None
    thbCabang = None
    thtCabang = None
    thlCabang = None
    
    thbSaldoAwal = None
    thlSaldoAwal = None
    thrSaldoAwal = None
    
    thbMutasiKredit = None
    thlMutasiKredit = None
    thrMutasiKredit = None
    
    thbTotalMutasiKredit = None
    thlTotalMutasiKredit = None
    thrTotalMutasiKredit = None
    
    thbMutasiDebit = None
    thlMutasiDebit = None
    thrMutasiDebit = None
    
    thbTotalMutasiDebit = None
    thlTotalMutasiDebit = None
    thrTotalMutasiDebit = None
    
    thbSaldoAkhir = None
    thlSaldoAkhir = None
    thrSaldoAkhir = None

    thrPemilikRekening = None
    thbPemilikRekening = None
    thtPemilikRekening = None
    thlPemilikRekening = None

    thrAlamat = None
    thbAlamat = None
    thtAlamat = None
    thlAlamat = None

    thrNomorRekening = None
    thbNomorRekening = None
    thtNomorRekening = None
    thlNomorRekening = None

    thrPeriode = None
    thbPeriode = None
    thtPeriode = None
    thlPeriode = None

    thrMataUang = None
    thbMataUang = None
    thtMataUang = None
    thlMataUang = None

    thbHeaderTable = None
    
    before = ''
    countSaldoAwal = 0
    
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    
    transactionData = []
    currentRow = 0
    textData = []
    textWithCol = {}

    for e in imageArray:
        thbTable = None
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
            bbox, text, score = e
    
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            rb = bbox[1][0]
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            cw = lb + int(abs(rb - lb) / 2)
            ch = tb + int(abs(bb - tb) / 2)
            
            if page == 1 :
                if ch < 0.1 * tinggiGambar and 'bca' in text.lower() :
                    thrCabang = lb + int(0.35 * lebarGambar)
                    thlCabang = lb - int(0.07 * lebarGambar)
                    thbCabang = bb + int(0.025 * tinggiGambar)
                    thtCabang = bb + int(0.01 * tinggiGambar)
                    
                    thrPemilikRekening = lb + int(0.35 * lebarGambar)
                    thlPemilikRekening = lb - int(0.07 * lebarGambar)
                    thbPemilikRekening = thbCabang + int(0.01 * tinggiGambar)
                    thtPemilikRekening = thbCabang
                    
                    thrAlamat = lb + int(0.35 * lebarGambar)
                    thlAlamat = lb - int(0.07* lebarGambar)
                    thbAlamat = bb + int(0.12 * tinggiGambar)
                    thtAlamat = thbPemilikRekening
                    
                    thrNomorRekening = rb + int(0.73 * lebarGambar)
                    thlNomorRekening = lb + int(0.62 * lebarGambar)
                    thbNomorRekening = bb + int(0.04 * tinggiGambar)
                    thtNomorRekening = bb
                    
                    thrPeriode = rb + int(0.73 * lebarGambar)
                    thlPeriode = lb + int(0.62 * lebarGambar)
                    thbPeriode = thbNomorRekening + int(0.03 * tinggiGambar)
                    thtPeriode = thbNomorRekening + int(0.014 * tinggiGambar)
                    
                    thrMataUang = rb + int(0.73 * lebarGambar)
                    thlMataUang = lb + int(0.62 * lebarGambar)
                    thbMataUang = thbPeriode + int(0.028 * tinggiGambar)
                    thtMataUang = thbPeriode
                    
                if thrCabang != None:
                    if (
                        (cw < thrCabang) 
                        and (ch <= thbCabang)   
                        and (ch >= thtCabang)
                        and (cw > thlCabang)
                    ) :
                        if cabang == None :
                            cabang = text
                            
                if thrPemilikRekening != None:
                    if (
                        (cw < thrPemilikRekening) 
                        and (ch <= thbPemilikRekening) 
                        and (ch >= thtPemilikRekening)
                        and (cw > thlPemilikRekening)
                    ) :
                        if pemilikRekening == None :
                            pemilikRekening = text
                            
                            
                if thrAlamat != None:
                    if (
                        (cw < thrAlamat) 
                        and (ch <= thbAlamat) 
                        and (ch >= thtAlamat)
                        and (cw > thlAlamat)
                    ) :
                        if alamat == None :
                            alamat = text
                            
                        else :
                            alamat = alamat + ' ' + text
                            
                if thrNomorRekening != None:
                    if (
                        (cw < thrNomorRekening) 
                        and (ch <= thbNomorRekening) 
                        and (ch >= thtNomorRekening)
                        and (cw > thlNomorRekening)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text
                            
                if thrPeriode != None:
                    if (
                        (cw < thrPeriode) 
                        and (ch <= thbPeriode) 
                        and (ch >= thtPeriode)
                        and (cw > thlPeriode)
                    ) :
                        if periode == None :
                            periode = text
                            
                if thrMataUang != None:
                    if (
                        (cw < thrMataUang) 
                        and (ch <= thbMataUang) 
                        and (ch >= thtMataUang)
                        and (cw > thlMataUang)
                    ) :
                        if mataUang == None :
                            mataUang = text
                            
            if 'saldo awal' in text.lower() or ('saldo' in before.lower() and 'awal' in text.lower()) :
                countSaldoAwal += 1
            
            if 'tanggal' in text.lower() and thbHeaderTable == None:
                thbHeaderTable = tb + int(0.013 * tinggiGambar)
                
            if countSaldoAwal >= 2 and thbTable == None and page == len(imageArray):
                thbTable = tb - int(0.001 * tinggiGambar)
                
                thbSaldoAwal = thbTable + int(0.014 * tinggiGambar)
                thlSaldoAwal = rb + int(0.03 * lebarGambar)
                thrSaldoAwal = rb + int(0.28 * lebarGambar)
                
                thbMutasiKredit = thbSaldoAwal + int(0.014 * tinggiGambar)
                thlMutasiKredit = rb + int(0.03 * lebarGambar)
                thrMutasiKredit = rb + int(0.23 * lebarGambar)
                
                thbTotalMutasiKredit = thbMutasiKredit
                thlTotalMutasiKredit = thrMutasiKredit
                thrTotalMutasiKredit = thlTotalMutasiKredit + int(0.15 * lebarGambar)
                
                thbMutasiDebit = thbMutasiKredit + int(0.014 * tinggiGambar)
                thlMutasiDebit = rb + int(0.03 * lebarGambar)
                thrMutasiDebit = rb + int(0.23 * lebarGambar)
                
                thbTotalMutasiDebit = thbMutasiDebit
                thlTotalMutasiDebit = thrMutasiDebit
                thrTotalMutasiDebit = thlTotalMutasiDebit + int(0.15 * lebarGambar)
                
                thbSaldoAkhir = thbMutasiDebit + int(0.014 * tinggiGambar)
                thlSaldoAkhir = rb + int(0.03 * lebarGambar)
                thrSaldoAkhir = rb + int(0.28 * lebarGambar)
                
            if 'bersambung' in text.lower() :
                thbTable = tb - int(0.001 * tinggiGambar)
                
            if thbSaldoAwal != None :
                if (
                    (cw < thrSaldoAwal) 
                    and (ch <= thbSaldoAwal) 
                    and (ch >= thbTable)
                    and (cw > thlSaldoAwal)
                ) :
                    if saldoAwal == None :
                        saldoAwal = text
                        
                    else  :
                        saldoAwal = saldoAwal + ' ' + text
                        
            if thbMutasiDebit != None :
                if (
                    (cw < thrMutasiDebit) 
                    and (ch <= thbMutasiDebit) 
                    and (ch >= thbMutasiKredit)
                    and (cw > thlMutasiDebit)
                ) :
                    if mutasiDebit == None :
                        mutasiDebit = text
                        
                    else :
                        mutasiDebit = mutasiDebit + ' ' + text
                        
            if thbMutasiKredit != None :
                if (
                    (cw < thrMutasiKredit) 
                    and (ch <= thbMutasiKredit) 
                    and (ch >= thbSaldoAwal)
                    and (cw > thlMutasiKredit)
                ) :
                    if mutasiKredit == None :
                        mutasiKredit = text
                        
                    else :
                        mutasiKredit = mutasiKredit + ' ' + text
            
            if thbSaldoAkhir != None :
                if (
                    (cw < thrSaldoAkhir) 
                    and (ch <= thbSaldoAkhir) 
                    and (ch >= thbMutasiDebit)
                    and (cw > thlSaldoAkhir)
                ) :
                    if saldoAkhir == None :
                        saldoAkhir = text
                        
                    else :
                        saldoAkhir = saldoAkhir + ' ' + text
                        
            if thbTotalMutasiDebit != None :
                if (
                    (cw < thrTotalMutasiDebit) 
                    and (ch <= thbTotalMutasiDebit) 
                    and (ch >= thbMutasiKredit)
                    and (cw > thlTotalMutasiDebit)
                ) :
                    if totalMutasiDebit == None :
                        totalMutasiDebit = text
                        
                    else :
                        totalMutasiDebit = totalMutasiDebit + ' ' + text
                    
            if thbTotalMutasiKredit != None :
                if (
                    (cw < thrTotalMutasiKredit) 
                    and (ch <= thbTotalMutasiKredit) 
                    and (ch >= thbSaldoAwal)
                    and (cw > thlTotalMutasiKredit)
                ) :
                    if totalMutasiKredit == None :
                        totalMutasiKredit = text
                        
                    else :
                        totalMutasiKredit = totalMutasiKredit + ' ' + text
                        
            before = text
                
        # if not isBankStatementCorrect :
        #     return 400
        
        for t in text_ :
            bbox, text, score = t
            
            bbox = [[int(coord[0]), int(coord[1])] for coord in bbox]
                    
            rb = bbox[1][0]
            lb = bbox[0][0]
            tb = bbox[1][1]
            bb = bbox[2][1]
            cw = lb + int(abs(rb - lb) / 2)
            ch = tb + int(abs(bb - tb) / 2)
            
            if 'tanggal' in text.lower() and cw < (thlAlamat + int(0.073 * tinggiGambar)) and currentRow == 0:
                thrTableCol1 = lb + int(0.063 * tinggiGambar)
                thrTableCol2 = thrTableCol1 + int(0.253 * tinggiGambar)
                thrTableCol3 = thrTableCol2 + int(0.0473 * tinggiGambar)
                thrTableCol4 = thrTableCol3 + int(0.149 * tinggiGambar)
                
            if thrTableCol1 != None and tb > thbHeaderTable and ch < thbTable :
                textWithCol['text'] = text
                
                if (cw < thrTableCol1) :
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
                    
                if (cw > thrTableCol4) :
                    textWithCol['col'] = 5
                    textWithCol['row'] = currentRow
                    
                textData.append(textWithCol.copy())
    
        transactionData.extend(bcaGetTransactionData(textData))
    
    data['kcp'] = cabang
    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['nomor_rekening'] = nomorRekening
    data['periode'] = periode
    data['mata_uang'] = mataUang
    data['saldo_awal'] = format_currency(convertToFloat(saldoAwal))
    data['saldo_akhir'] = format_currency(convertToFloat(saldoAkhir))
    data['mutasi_debit'] = format_currency(convertToFloat(mutasiDebit))
    data['mutasi_kredit'] = format_currency(convertToFloat(mutasiKredit))
    data['total_mutasi_debit'] = totalMutasiDebit
    data['total_mutasi_kredit'] = totalMutasiKredit
    data['transaction_data'] = transactionData
    data['total_debit'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    # data['analytics_data'] = getAnalysisData(data['transaction_data'])
    return data