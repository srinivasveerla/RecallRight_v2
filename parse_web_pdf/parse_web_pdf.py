# import PyPDF2
#
# # Open the PDF file in read-binary mode
# with open('Newwhitepaper_Prompt Engineering_v4.pdf', 'rb') as pdf_file:
#     # Create a PDF reader object
#     RecallRight_v2 = PyPDF2.PdfReader(pdf_file)
#
#     # Get the number of pages in the PDF
#     num_pages = len(RecallRight_v2.pages)
#
#     print(num_pages)
#     # Extract text from the first page
#     for i in range(num_pages):
#         text = RecallRight_v2.pages[i].extract_text()
#
#         print(text)
#         if i==10:
#             break

# import requests
#
# # URL to send the GET request to
# url = "https://www.superannotate.com/blog/llm-fine-tuning"
#
# # Send a GET request to the URL
# response = requests.get(url)
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Write the response content to a file named 'extracted.txt'
#     with open("extracted.txt", "wb") as f:
#         f.write(response.content)
#     print("Content successfully written to 'extracted.txt'.")
# else:
#     print(f"Failed to retrieve content. HTTP Status Code: {response.status_code}")


from bs4 import BeautifulSoup
import re


def extract_content(html_file):
    """
    Extracts and cleans meaningful content from HTML files while removing boilerplate elements.

    Args:
        html_file (str): Path to the HTML file.

    Returns:
        str: Cleaned text content.
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Remove unwanted elements
    unwanted_tags = [
        'script', 'style', 'nav', 'footer', 'header', 'aside',
        'noscript', 'iframe', 'ad', 'advertisement', 'banner',
        'cookie-notice', 'popup', 'social-share', 'comments'
    ]

    # Remove elements by tag name
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    # Remove elements by common class names and IDs
    unwanted_patterns = re.compile(
        r'(advertisement|banner|sidebar|footer|header|menu|nav|social|share|comment|popup|modal|cookie|newsletter)',
        re.IGNORECASE)
    for element in soup.find_all(class_=unwanted_patterns):
        element.decompose()
    for element in soup.find_all(id=unwanted_patterns):
        element.decompose()

    # Try to find the main content area
    main_content = None
    priority_containers = [
        soup.find('article'),
        soup.find('main'),
        soup.find('div', {'id': 'main-content'}),
        soup.find('div', {'class': 'main-content'}),
        soup.find('div', {'role': 'main'}),
        soup.find('div', {'class': 'content'}),
        soup.find('div', {'id': 'content'})
    ]

    for container in priority_containers:
        if container:
            main_content = container
            break

    # If no main content area found, use body
    if not main_content:
        main_content = soup.body

    # Extract text if main_content exists
    if main_content:
        text = main_content.get_text(separator='\n')
    else:
        return ""

    # Clean the extracted text
    def clean_text(text):
        # Remove multiple newlines and whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # Remove extra whitespace from each line
        lines = [line.strip() for line in text.splitlines()]

        # Remove empty lines and very short lines (likely menu items)
        lines = [line for line in lines if len(line) > 15 or re.search(r'[.!?]$', line)]

        # Remove lines that are likely navigation/menu items
        lines = [line for line in lines if not re.match(r'^(home|about|contact|search|menu)', line.lower())]

        # Join lines back together
        text = '\n'.join(lines)

        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)

        return text.strip()

    cleaned_text = clean_text(text)
    return cleaned_text


def extract_content_from_multiple_files(file_list):
    """
    Extract content from multiple HTML files.

    Args:
        file_list (list): List of HTML file paths.

    Returns:
        dict: Dictionary with filenames as keys and extracted content as values.
    """
    results = {}
    for file_path in file_list:
        try:
            content = extract_content(file_path)
            results[file_path] = content
        except Exception as e:
            results[file_path] = f"Error processing file: {str(e)}"
    return results


if __name__ == '__main__':
    # Example usage
    html_file = 'extracted.txt'
    extracted_text = extract_content(html_file)
    print(extracted_text)

    # For multiple files
    # files = ['file1.html', 'file2.html', 'file3.html']
    # results = extract_content_from_multiple_files(files)
    # for file, content in results.items():
    #     print(f"\nContent from {file}:")
    #     print(content)