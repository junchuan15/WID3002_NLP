import fitz  # PyMuPDF

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
    return text

# Function to save text to a file
def save_text_to_file(text, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text saved to '{output_file}'")
    except IOError as e:
        print(f"File write failed: {e}")

# Main function to process multiple PDFs
def process_pdfs(pdf_paths, output_files):
    for pdf_path, output_file in zip(pdf_paths, output_files):
        text = extract_text_from_pdf(pdf_path)
        save_text_to_file(text, output_file)

# List of PDF files to process and their corresponding output JSON files
pdf_paths = [
    "C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\Security Section.pdf",
    "C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\LIBRARY UM WOW.pdf",
    "C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\INTRODUCTION OF UM CLINIC-ZM.pdf",
    "C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\CDE for UM-WOW 2023.pdf",
    "C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\um wow schedule.pdf"
]


output_files = [
    "security_briefing.txt",
    "universiti_malaya_library.txt",
    "um_clinic.txt",
    "counseling_disability.txt",
    "week_of_welcome.txt"
]

# Process the PDFs
process_pdfs(pdf_paths, output_files)

