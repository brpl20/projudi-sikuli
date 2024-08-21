import os
from openai import OpenAI
from PyPDF2 import PdfReader
from PIL import Image
from pytesseract import image_to_string

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

input_folder = "."
output_folder = "output"

json_object = {}

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page_num in range(min(4, len(reader.pages))):
        page = reader.pages[page_num]
        text += page.extract_text() + "\n"

    return text

def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extraia o número do processo, os dados do advogado e se tem honorários específicos para ele, valor, dados do cliente do texto fornecido"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def process_pdf_files(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(input_path)

            prompt = f"Aqui está o txto extraído:\n\n{text}"
            result = ask_chatgpt(prompt)
            json_object['response'] = result


            output_path = os.path.join(output_folder, f"{filename}.txt")
            with open(output_path, "w") as output_file:
                output_file.write(result)

process_pdf_files(input_folder)
