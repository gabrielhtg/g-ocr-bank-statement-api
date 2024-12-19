import os
import uuid
from matplotlib.dviread import Page
from werkzeug.utils import secure_filename
from format_currency import format_currency

from services.bri_services.get_analysis_data import briAnalysisData
from services.bri_services.get_total_debit import getTotalDebit
from services.bri_services.get_total_kredit import getTotalKredit
from services.bri_services.get_transaction_data import briGetTransactionData
from services.utils.convert_to_float import convertToFloat
from services.utils.correct_perspective import correctPerspective
from services.utils.delete_image import deleteImage
from services.utils.do_orc_easyocr import doEasyOcr
from services.utils.exception_handler import exceptionHandler
from services.utils.get_image_height import getImageHeight
from services.utils.get_image_width import getImageWidth

def doOcrBriPdf(imageArray, app, isZip, isPdf, logger, username) :
    pemilikRekening = None
    alamat = None
    nomorRekening = None
    namaProduk = None
    valuta = None
    tanggalLaporan = None
    periodeTransaksi = None
    unitKerja = None
    alamatUnitKerja = None
    saldoAwal = None
    totalTransaksiDebit = None
    totalTransaksiKredit = None
    saldoAkhir = None
    
    periodeLaporan = None
    nomorNasabah = None
    cabang = None
    pemilikRekening = None
    alamat = None

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

    thrNamaProduk = None
    thbNamaProduk = None
    thtNamaProduk = None
    thlNamaProduk = None

    thrValuta = None
    thbValuta = None
    thtValuta = None
    thlValuta = None

    thrTanggalLaporan = None
    thbTanggalLaporan = None
    thtTanggalLaporan = None
    thlTanggalLaporan = None

    thrPeriodeLaporan = None
    thbPeriodeLaporan = None
    thtPeriodeLaporan = None
    thlPeriodeLaporan = None

    thrUnitKerja = None
    thbUnitKerja = None
    thtUnitKerja = None
    thlUnitKerja = None

    thrAlamatUnitKerja = None
    thbAlamatUnitKerja = None
    thtAlamatUnitKerja = None
    thlAlamatUnitKerja = None
    
    thrSaldoAwal = None
    thbSaldoAwal = None
    thtSaldoAwal = None
    thlSaldoAwal = None

    thrTotalTransaksiDebit = None
    thbTotalTransaksiDebit = None
    thtTotalTransaksiDebit = None
    thlTotalTransaksiDebit = None

    thrTotalTransaksiKredit = None
    thbTotalTransaksiKredit = None
    thtTotalTransaksiKredit = None
    thlTotalTransaksiKredit = None

    thrSaldoAkhir = None
    thbSaldoAkhir = None
    thtSaldoAkhir = None
    thlSaldoAkhir = None
    
    data = {}
    thbHeaderTable = None
    thbTable = None
    thrTableCol1 = None
    thrTableCol2 = None
    thrTableCol3 = None
    thrTableCol4 = None
    thrTableCol5 = None
    thrTableCol6 = None

    currentRow = 0
    textData = []
    textWithCol = {}
    transactionData = []
    page = 0
    
    countText = 0
    
    for e in imageArray:
        page += 1
        textData.clear()
        
        if isZip :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        if isPdf :
            filename = secure_filename(e)
            file_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], filename)
            perspectiveCorrectedImage = correctPerspective(file_path)
            
        else :
            file = e
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            perspectiveCorrectedImage = correctPerspective(file_path)
        
        logger.info(f"{username} : Processing {filename}")
        print('Processing', filename)
        
        lebarGambar = getImageWidth(perspectiveCorrectedImage)
        tinggiGambar = getImageHeight(perspectiveCorrectedImage)
        
        if int(lebarGambar) > int(tinggiGambar) :
            return exceptionHandler(
                'Image detected landscape. Photo images in Portrait form',
                400,
                e
            )

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
                'cimb' in text.lower() or
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
                if 'bri' in text.lower() and ch < 0.3 * tinggiGambar:
                    thlPemilikRekening = lb - int(0.06 * lebarGambar)
                    thrPemilikRekening = thlPemilikRekening + int(0.34 * lebarGambar)
                    thtPemilikRekening = tb + int(0.125 * tinggiGambar)
                    thbPemilikRekening = thtPemilikRekening + int(0.026 * tinggiGambar)
                    
                    thlAlamat = thlPemilikRekening
                    thrAlamat = thrPemilikRekening
                    thtAlamat = thbPemilikRekening
                    thbAlamat = thtAlamat + int(0.055 * tinggiGambar)
                    
                if 'kening' in text.lower() and ch < 0.3 * tinggiGambar :
                    thlNomorRekening = rb + int(0.05 * lebarGambar)
                    thrNomorRekening = rb + int(0.3 * lebarGambar)
                    thtNomorRekening = tb - int(0.005 * tinggiGambar)
                    thbNomorRekening = bb + int(0.005 * tinggiGambar)
                    
                if 'oduk' in text.lower() and ch < 0.4 * tinggiGambar :
                    thlNamaProduk = rb + int(0.05 * lebarGambar)
                    thrNamaProduk = rb + int(0.3 * lebarGambar)
                    thtNamaProduk = tb - int(0.005 * tinggiGambar)
                    thbNamaProduk = bb + int(0.005 * tinggiGambar)
                    
                if 'valuta' in text.lower() and ch < 0.4 * tinggiGambar :
                    thlValuta = rb + int(0.08 * lebarGambar)
                    thrValuta = rb + int(0.3 * lebarGambar)
                    thtValuta = tb - int(0.005 * tinggiGambar)
                    thbValuta = bb + int(0.005 * tinggiGambar)
                    
                if 'tang' in text.lower() and ch < 0.2 * tinggiGambar :
                    thlTanggalLaporan = rb + int(0.03 * lebarGambar)
                    thrTanggalLaporan = rb + int(0.3 * lebarGambar)
                    thtTanggalLaporan = tb - int(0.005 * tinggiGambar)
                    thbTanggalLaporan = bb + int(0.005 * tinggiGambar)
                    
                if 'aksi' in text.lower() and ch < 0.3 * tinggiGambar :
                    thlPeriodeTransaksi = rb + int(0.03 * lebarGambar)
                    thrPeriodeTransaksi = rb + int(0.3 * lebarGambar)
                    thtPeriodeTransaksi = tb - int(0.005 * tinggiGambar)
                    thbPeriodeTransaksi = bb + int(0.005 * tinggiGambar)
                    
                if 'kerja' in text.lower() and 'alamat' not in text.lower() and ch < 0.4 * tinggiGambar :
                    thlUnitKerja = rb + int(0.03 * lebarGambar)
                    thrUnitKerja = rb + int(0.3 * lebarGambar)
                    thtUnitKerja = tb - int(0.005 * tinggiGambar)
                    thbUnitKerja = bb + int(0.005 * tinggiGambar)
                    
                if 'alamat' in text.lower() and ch < 0.4 * tinggiGambar :
                    thlAlamatUnitKerja = rb + int(0.03 * lebarGambar)
                    thrAlamatUnitKerja = rb + int(0.3 * lebarGambar)
                    thtAlamatUnitKerja = tb - int(0.005 * tinggiGambar)
                    thbAlamatUnitKerja = bb + int(0.02 * tinggiGambar)
                    
                if thrPemilikRekening != None:
                    if (
                        (cw < thrPemilikRekening) 
                        and (cw > thlPemilikRekening) 
                        and (ch > thtPemilikRekening)
                        and (ch < thbPemilikRekening)
                    ) :
                        if pemilikRekening == None :
                            pemilikRekening = text
                            
                        else :
                            if pemilikRekening == None:
                                pemilikRekening = text
                            
                if thrAlamat != None:
                    if (
                        (cw < thrAlamat) 
                        and (cw > thlAlamat) 
                        and (ch > thtAlamat)
                        and (ch < thbAlamat)
                    ) :
                        if alamat == None :
                            alamat = text.strip()
                            
                        else : 
                            alamat = alamat + ' ' + text.strip()
                
                if thrNomorRekening != None:
                    if (
                        (cw < thrNomorRekening) 
                        and (cw > thlNomorRekening) 
                        and (ch > thtNomorRekening)
                        and (ch < thbNomorRekening)
                    ) :
                        if nomorRekening == None :
                            nomorRekening = text.strip()
                            
                if thrNamaProduk != None:
                    if (
                        (cw < thrNamaProduk) 
                        and (cw > thlNamaProduk) 
                        and (ch > thtNamaProduk)
                        and (ch < thbNamaProduk)
                    ) :
                        if namaProduk == None :
                            namaProduk = text.strip()
                            
                if thrValuta != None:
                    if (
                        (cw < thrValuta) 
                        and (cw > thlValuta) 
                        and (ch > thtValuta)
                        and (ch < thbValuta)
                    ) :
                        if valuta == None :
                            valuta = text.strip()
                            
                if thrTanggalLaporan != None:
                    if (
                        (cw < thrTanggalLaporan) 
                        and (cw > thlTanggalLaporan) 
                        and (ch > thtTanggalLaporan)
                        and (ch < thbTanggalLaporan)
                    ) :
                        if tanggalLaporan == None :
                            tanggalLaporan = text.strip()
                            
                if thrPeriodeTransaksi != None:
                    if (
                        (cw < thrPeriodeTransaksi) 
                        and (cw > thlPeriodeTransaksi) 
                        and (ch > thtPeriodeTransaksi)
                        and (ch < thbPeriodeTransaksi)
                    ) :
                        if periodeTransaksi == None :
                            periodeTransaksi = text.strip()
                            
                        else :
                            periodeTransaksi = periodeTransaksi + ' - ' + text.strip()
                            
                if thrUnitKerja != None:
                    if (
                        (cw < thrUnitKerja) 
                        and (cw > thlUnitKerja) 
                        and (ch > thtUnitKerja)
                        and (ch < thbUnitKerja)
                    ) :
                        if unitKerja == None :
                            unitKerja = text.strip()
                            
                if thrAlamatUnitKerja != None:
                    if (
                        (cw < thrAlamatUnitKerja) 
                        and (cw > thlAlamatUnitKerja) 
                        and (ch > thtAlamatUnitKerja)
                        and (ch < thbAlamatUnitKerja)
                    ) :
                        if alamatUnitKerja == None :
                            alamatUnitKerja = text.strip()
            
            try :       
                if 'tanggal' in text.lower() and 'ran' in text.lower() and currentRow == 0 and ch > 0.3 * tinggiGambar:
                    thbHeaderTable = tb + int(0.025 * tinggiGambar)
                    thbTable = tb + int(0.51 * tinggiGambar)
                    thrTableCol1 = rb + int(0.005 * lebarGambar)
                    thrTableCol2 = thrTableCol1 + int(0.272 * lebarGambar)
                    thrTableCol3 = thrTableCol2 + int(0.073 * lebarGambar)
                    thrTableCol4 = thrTableCol3 + int(0.154 * lebarGambar)
                    thrTableCol5 = thrTableCol4 + int(0.146 * lebarGambar)
                
                if page > 1 :
                    if 'tanggal' in text.lower() and 'ran' in text.lower() :
                        thbHeaderTable = tb + int(0.025 * tinggiGambar)
                        
                        thrTableCol1 = rb + int(0.005 * lebarGambar)
                        thrTableCol2 = thrTableCol1 + int(0.263 * lebarGambar)
                        thrTableCol3 = thrTableCol2 + int(0.069 * lebarGambar)
                        thrTableCol4 = thrTableCol3 + int(0.154 * lebarGambar)
                        thrTableCol5 = thrTableCol4 + int(0.152 * lebarGambar)
                        
                    if 'saldo awal' in text.lower() :
                        thbTable = tb + int(0.005 * tinggiGambar)
                        thtTotalTransaksiDebit = thtSaldoAwal
                        thtTotalTransaksiKredit = thtSaldoAwal
                        thtSaldoAkhir = thtSaldoAwal
                        
                        thtSaldoAwal = bb + int(0.013 * tinggiGambar)
                        thlSaldoAwal = lb - int(0.073 * lebarGambar)
                        thrSaldoAwal = rb + int(0.073 * lebarGambar) 
                        thbSaldoAwal = thtSaldoAwal + int(0.02 * tinggiGambar) 
                        
                        thlTotalTransaksiDebit = thrSaldoAwal
                        thrTotalTransaksiDebit = thrSaldoAwal + int(0.23 * lebarGambar) 
                        thtTotalTransaksiDebit = bb + int(0.013 * tinggiGambar)
                        thbTotalTransaksiDebit = thtSaldoAwal + int(0.02 * tinggiGambar)
                        
                        thlTotalTransaksiKredit = thrTotalTransaksiDebit
                        thrTotalTransaksiKredit = thrTotalTransaksiDebit + int(0.21 * lebarGambar) 
                        thtTotalTransaksiKredit = bb + int(0.013 * tinggiGambar)
                        thbTotalTransaksiKredit = thtSaldoAwal + int(0.02 * tinggiGambar)
                        
                        thlSaldoAkhir = thrTotalTransaksiKredit
                        thrSaldoAkhir = thrTotalTransaksiKredit + int(0.28 * lebarGambar) 
                        thtSaldoAkhir = bb + int(0.013 * tinggiGambar)
                        thbSaldoAkhir = thtSaldoAwal + int(0.02 * tinggiGambar)
                        
                    if thrSaldoAwal != None:
                        if (
                            (cw < thrSaldoAwal) 
                            and (cw > thlSaldoAwal) 
                            and (ch > thtSaldoAwal)
                            and (ch < thbSaldoAwal)
                        ) :
                            if saldoAwal == None :
                                saldoAwal = format_currency(convertToFloat(text))
                                
                    if thrTotalTransaksiDebit != None:
                        if (
                            (cw < thrTotalTransaksiDebit) 
                            and (cw > thlTotalTransaksiDebit) 
                            and (ch > thtTotalTransaksiDebit)
                            and (ch < thbTotalTransaksiDebit)
                        ) :
                            if totalTransaksiDebit == None :
                                totalTransaksiDebit = format_currency(convertToFloat(text))
                                
                    if thrTotalTransaksiKredit != None:
                        if (
                            (cw < thrTotalTransaksiKredit) 
                            and (cw > thlTotalTransaksiKredit) 
                            and (ch > thtTotalTransaksiKredit)
                            and (ch < thbTotalTransaksiKredit)
                        ) :
                            if totalTransaksiKredit == None :
                                totalTransaksiKredit = format_currency(convertToFloat(text))
                                
                    if thrSaldoAkhir != None:
                        if (
                            (cw < thrSaldoAkhir) 
                            and (cw > thlSaldoAkhir) 
                            and (ch > thtSaldoAkhir)
                            and (ch < thbSaldoAkhir)
                        ) :
                            if saldoAkhir == None :
                                saldoAkhir = format_currency(convertToFloat(text))
                        
                if thbHeaderTable != None and tb > thbHeaderTable and ch < thbTable :
                    # if currentRow == 0 :
                    #     currentRow += 1

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
                        
                    if (cw > thrTableCol4 and cw < thrTableCol5) :
                        textWithCol['col'] = 5
                        textWithCol['row'] = currentRow
                        
                    if (cw > thrTableCol5) :
                        textWithCol['col'] = 6
                        textWithCol['row'] = currentRow
                        
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
        
        transactionData.extend(briGetTransactionData(textData, filename))
        deleteImage(file_path)

    data['pemilik_rekening'] = pemilikRekening
    data['alamat'] = alamat
    data['nomor_rekening'] = nomorRekening
    data['nama_produk'] = namaProduk
    data['valuta'] = valuta
    data['tanggal_laporan'] = tanggalLaporan
    data['periode_transaksi'] = periodeTransaksi
    data['saldo_awal'] = saldoAwal
    data['saldo_akhir'] = saldoAkhir
    data['total_transaksi_debit'] = totalTransaksiDebit
    data['total_transaksi_kredit'] = totalTransaksiKredit
    data['transaction_data'] = transactionData
    data['unit_kerja'] = unitKerja
    data['alamat_unit_kerja'] = alamatUnitKerja
    data['total_debit'] = getTotalDebit(transactionData)
    data['total_kredit'] = getTotalKredit(transactionData)
    data['analytics_data'] = briAnalysisData(data['transaction_data'])
    data['banyak_halaman'] = len(imageArray)
    return 200, data