import sys
import os
from PyPDF2 import PdfReader

def extract_attachments(pdf_path, output_folder):
    """
    Extract attachments from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Folder to save the extracted attachments.
    """
    try:
        # Open the PDF file
        reader = PdfReader(pdf_path)
        catalog = reader.trailer["/Root"].get_object()

        # Check for EmbeddedFiles in the PDF structure
        if "/Names" not in catalog or "/EmbeddedFiles" not in catalog["/Names"].get_object():
            print("No attachments found in the PDF.")
            return

        embedded_files = catalog["/Names"].get_object()["/EmbeddedFiles"].get_object()

        # If /Kids exists, process each one
        if "/Kids" in embedded_files:
            kids = embedded_files["/Kids"]
            file_specs = [kid.get_object() for kid in kids]
        else:
            # Directly process the EmbeddedFiles dictionary
            file_specs = [embedded_files]

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Iterate through and save each attachment
        for file_spec in file_specs:
            if "/Names" in file_spec:
                names_array = file_spec["/Names"]
                for i in range(0, len(names_array), 2):
                    name = names_array[i]
                    file_entry = names_array[i + 1].get_object()

                    file_name = name
                    file_data = file_entry["/EF"].get_object()["/F"].get_data()

                    file_path = os.path.join(output_folder, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                    print(f"Attachment '{file_name}' saved to '{file_path}'.")
    except Exception as e:
        print(f"Error while extracting attachments: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_attachments.py <pdf_path> <output_folder>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2]

    extract_attachments(pdf_file, output_dir)
