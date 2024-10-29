import re
import html

def clean_urls(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to match the URLs
    url_pattern = r'https://www\.tjrs\.jus\.br/site_php/precatorios/lista_precatorios_credores\.php\?[^"\'<>\s]+'

    # Find all matches
    encoded_urls = re.findall(url_pattern, content)

    # Decode HTML entities and write the cleaned URLs to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for encoded_url in encoded_urls:
            decoded_url = html.unescape(encoded_url)
            file.write(decoded_url + '\n')

    print(f"Cleaned URLs have been written to {output_file}")

# Usage
input_file = 'lista.html'  # Replace with your input file name
output_file = 'cleaned_urls.txt'  # Replace with your desired output file name

clean_urls(input_file, output_file)