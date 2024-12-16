import os
import uuid
from flask import jsonify, request

from services.bca_services.ocr_service import doOcrBca
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.return_fail_message import returnFailMessage

def bcaController(app, logger) :
    username = request.headers.get('X-Username')
    
    logger.info(f"{username} : '/proceed-bca', methods=['POST']")
    
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    
    if request.form.get('zip-password') :
        zipPassword = request.form.get('zip-password')
    
    # variable ini menyimpan apakah file yang diupload adalah 
    # file zip atau bukan. 
    isZip = False
    isPdf = False
    isPdfModified = None
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        isPdf = checkIsPdf(uploadedFiles)
        
    if isZip:
        logger.info(f"{username} : Proceed BCA Zip")
        logger.info(f"{username} : Zip filename {uploadedFiles[0].filename}")
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            logger.error(f"{username} : 'Gagal mengekstrak zip! Password salah!. Return 400")
            return returnFailMessage('Gagal mengekstrak zip! Password salah!', 400)

        else :
            statusCode, data = doOcrBca(fileList, app, isZip, isPdf, username, logger)

            if statusCode != 200 :
                logger.error(f"{username} : {data}, {statusCode}")
                return returnFailMessage(data, statusCode)
            
    elif isPdf :
        logger.info(f"{username} : Proceed BCA PDF")
        logger.info(f"{username} : PDF filename {uploadedFiles[0].filename}")
        fileList = getImagesFromPdf(uploadedFiles[0], app)
        
        unique_filename = f"{uuid.uuid4().hex}_{uploadedFiles[0].filename}"
        destination_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], unique_filename)
        uploadedFiles[0].save(destination_path)
        stat = os.stat(destination_path)
        
        if stat.st_mtime == stat.st_ctime :
            isPdfModified = False
            
        else :
            isPdfModified = True
            
        os.remove(destination_path)
        
        statusCode, data = doOcrBca(fileList, app, isZip, isPdf, username, logger)

        if statusCode != 200 :
            logger.error(f"{username} : {data}, {statusCode}")
            return returnFailMessage(data, statusCode)
        
    else :
        logger.info(f"{username} : Proceed BCA Images")
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrBca(sortedData, app, isZip, isPdf, username, logger)
        
        if statusCode != 200 :
            logger.error(f"{username} : {data}, {statusCode}")
            return returnFailMessage(data, statusCode)
    
    logger.info(f"{username} : Proceed BCA Success, {statusCode}")
    return jsonify({
        'message' : 'ok',
        'data' : {
            'kcp' : data['kcp'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'nomor_rekening' : data['nomor_rekening'],
            'periode' : data['periode'],
            'mata_uang' : data['mata_uang'],
            'saldo_awal' : data['saldo_awal'],
            'saldo_akhir' : data['saldo_akhir'],
            'mutasi_debit' : data['mutasi_debit'],
            'mutasi_kredit' : data['mutasi_kredit'],
            'total_mutasi_debit' : data['total_mutasi_debit'],
            'total_mutasi_kredit' : data['total_mutasi_kredit'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debit'],
            'total_kredit' : data['total_kredit'],
            'analytics_data': data['analytics_data'],
            'is_pdf_modified' : isPdfModified,
            # 'account_validation': validationResponse
        }
    }), statusCode