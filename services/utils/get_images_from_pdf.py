import os
import uuid
from pdf2image import convert_from_bytes

def getImagesFromPdf(pdf_file, app):
    extracted_images = []  # Menyimpan daftar file gambar yang dihasilkan

    try:
        images = convert_from_bytes(pdf_file.read(), dpi=500)

        for index, image in enumerate(images):
            unique_filename = f"{uuid.uuid4().hex}_page_{index + 1}.png"
            destination_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], unique_filename)

            image.save(destination_path, "PNG")

            extracted_images.append(unique_filename)

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return 400

    return extracted_images
