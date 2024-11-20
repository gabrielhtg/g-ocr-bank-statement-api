import os
import uuid
from flask import jsonify, request

from services.bri_services.bri_ocr_service import doOcrBri
from services.bri_services.bri_ocr_service_pdf import doOcrBriPdf
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.return_fail_message import returnFailMessage

def briController(app) :
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    
    if request.form.get('zip-password') :
        zipPassword = request.form.get('zip-password')
    
    # variable ini menyimpan apakah file yang diupload adalah 
    # file zip atau bukan. 
    isZip = False
    isPdf = False
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        isPdf = checkIsPdf(uploadedFiles)
        
    if isZip:
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
        
        unique_filename = f"{uuid.uuid4().hex}_{uploadedFiles[0].filename}"
        destination_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], unique_filename)
        uploadedFiles[0].save(destination_path)
        stat = os.stat(destination_path)
        
        if stat.st_mtime == stat.st_ctime :
            isPdfModified = False
            
        else :
            isPdfModified = True
            
        os.remove(destination_path)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            statusCode, data = doOcrBri(fileList, app, isZip, isPdf)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    elif isPdf:
        fileList = getImagesFromPdf(uploadedFiles[0], app)
            
        statusCode, data = doOcrBriPdf(fileList, app, isZip, isPdf)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrBri(sortedData, app, isZip, isPdf)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'nomor_rekening' : data['nomor_rekening'],
            'nama_produk' : data['nama_produk'],
            'valuta' : data['valuta'],
            'tanggal_laporan' : data['tanggal_laporan'],
            'periode_transaksi' : data['periode_transaksi'],
            'transaction_data' : data['transaction_data'],
            'total_debit' : data['total_debit'],
            'total_kredit' : data['total_kredit'],
            'analytics_data' : data['analytics_data'],
            'unit_kerja' : data['unit_kerja'],
            'alamat_unit_kerja' : data['alamat_unit_kerja'],
            'saldo_awal' : data['saldo_awal'],
            'saldo_akhir' : data['saldo_akhir'],
            'total_transaksi_debit' : data['total_transaksi_debit'],
            'total_transaksi_kredit' : data['total_transaksi_kredit'],
            'is_pdf_modified' : isPdfModified
        }
    })