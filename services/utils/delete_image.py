import os


def deleteImage(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Gagal menghapus file {file_path}: {str(e)}")