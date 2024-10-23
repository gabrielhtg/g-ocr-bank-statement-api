def checkIsZip(uploaded_files):
    if '.zip' in uploaded_files[0].filename:
        return True

    return False