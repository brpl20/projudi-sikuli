import os
from openai import OpenAI
from PyPDF2 import PdfReader
from PIL import Image
from pytesseract import image_to_string
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Trello credentials
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")

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

def create_trello_card(title, description, pdf_path):
    url = f"https://api.trello.com/1/cards"
    
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': TRELLO_LIST_ID,
        'idBoard': TRELLO_BOARD_ID,
        'name': title,
        'desc': description
    }
    
    response = requests.post(url, params=query)
    
    if response.status_code == 200:
        card_id = response.json()['id']
        attach_pdf_to_card(card_id, pdf_path)
        print(f"Card created successfully: {response.json()['url']}")
    else:
        print(f"Failed to create card: {response.text}")

def attach_pdf_to_card(card_id, pdf_path):
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    
    files = {'file': open(pdf_path, 'rb')}
    params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    
    response = requests.post(url, params=params, files=files)
    
    if response.status_code == 200:
        print(f"PDF attached successfully to the card")
    else:
        print(f"Failed to attach PDF: {response.text}")

def process_pdf_files(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(input_path)

            prompt = f"Aqui está o texto extraído:\n\n{text}"
            result = ask_chatgpt(prompt)
            json_object['response'] = result

            # Create Trello card
            card_title = f"Análise do processo: {filename}"
            create_trello_card(card_title, result, input_path)

            # Still save the result to a local file
            output_path = os.path.join(output_folder, f"{filename}.txt")
            with open(output_path, "w") as output_file:
                output_file.write(result)

process_pdf_files(input_folder)