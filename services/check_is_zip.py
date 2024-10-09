def checkIsZip(uploaded_files):
    if uploaded_files[0].content_type == 'application/zip':
        return True

    return False