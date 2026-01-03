import os
import re
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import warnings

# Ignore XML parsing warnings common in EbookLib
warnings.filterwarnings('ignore')

def get_images(filename):
    book = epub.read_epub(filename)
    # Export all images from the Book
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        with open(os.path.basename(image.get_name()), "wb") as f:
            f.write(image.get_content())

def clean_text(text):
    """
    Clean text for training set preparation:
    1. Remove author/header lines like "Слава Сэ"
    2. Remove chapter headings like "Глава первая", "Глава вторая", etc.
    3. Remove excessive newlines (keep single newlines for paragraph separation)
    4. Remove copyright notices and asterisk separators
    """
    # Split text into lines for line-by-line processing
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip if line is empty
        if not stripped_line:
            continue
            
        # 1. First, try to remove copyright patterns from the line
        # This handles patterns like "© Слава Сэ, 2014© ООО «Издательство АСТ», 2014"
        copyright_removed = re.sub(r'©[^©]*©[^©]*\d{4}', '', stripped_line)
        
        # 2. Remove individual copyright patterns
        copyright_removed = re.sub(r'©\s*[^,]*,\s*\d{4}', '', copyright_removed)
        
        # 3. Remove publisher patterns
        copyright_removed = re.sub(r'©\s*ООО\s*«[^»]+»\s*,\s*\d{4}', '', copyright_removed)
        copyright_removed = re.sub(r'©\s*ООО\s*«[^»]+»\s*\d{4}', '', copyright_removed)
        
        # 4. Remove asterisk separators (like "* * *")
        # This handles cases where asterisks are attached to text
        copyright_removed = re.sub(r'\*\s*\*\s*\*', '', copyright_removed)
        
        # Clean up any leftover asterisks
        copyright_removed = re.sub(r'\s*[*·•\-_=]+\s*', ' ', copyright_removed)
        
        # Strip again after removals
        copyright_removed = copyright_removed.strip()
        
        # If line became empty after copyright removal, skip it
        if not copyright_removed:
            continue
            
        # Skip author/header lines (case insensitive)
        if re.match(r'^Слава\s+Сэ$', copyright_removed, re.IGNORECASE):
            continue
            
        # Skip book titles in parentheses (like "Ева (сборник)")
        if re.match(r'^[\w\s]+\(\s*[\w\s]+\s*\)$', copyright_removed):
            continue
            
        # Skip single-word lines that might be headers
        if len(copyright_removed.split()) <= 2 and copyright_removed.isupper():
            continue
            
        # Remove chapter headings
        if re.match(r'^Глава\s+[\w\d]+.*$', copyright_removed, re.IGNORECASE):
            continue
            
        # Remove chapter headings with Roman numerals
        if re.match(r'^Глава\s+[IVXLCDM]+.*$', copyright_removed, re.IGNORECASE):
            continue
            
        # Remove numeric chapter headings
        if re.match(r'^Глава\s+[0-9]+.*$', copyright_removed, re.IGNORECASE):
            continue
            
        # Remove lines that are only symbols or very short after cleaning
        if re.match(r'^[\s*·•\-_=]+$', copyright_removed):
            continue
            
        # Keep the line if it's not empty after cleaning
        if copyright_removed:
            # Additional cleanup: remove any leftover copyright symbols
            final_line = re.sub(r'^\s*©\s*', '', copyright_removed)
            cleaned_lines.append(final_line.strip())
    
    # Join lines back together
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Remove excessive newlines (replace 3 or more newlines with 2 newlines)
    cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)
    
    # Final cleanup: remove any lines that are only asterisks/symbols
    cleaned_text = re.sub(r'^\s*[*·•\-_=]+\s*$', '', cleaned_text, flags=re.MULTILINE)
    
    # Remove any completely empty lines that might have been created
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    
    return cleaned_text.strip()


def ascending_epub_convert_clean(filename, target, clean=True):
    """
    Extract chapters in reading order and save to file
    
    Args:
        filename: Path to EPUB file
        target: Path to output text file
        clean: If True, clean the text (remove headers, chapter headings, excessive newlines)
    """
    book = epub.read_epub(filename)
    spine_items = book.spine
    spine_ids = [item[0] for item in spine_items]

    # Get all documents
    all_docs = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    # Create a dictionary for quick lookup
    docs_dict = {doc.get_id(): doc for doc in all_docs}

    # Sort documents according to spine order
    documents = []
    for item_id in spine_ids:
        if item_id in docs_dict:
            documents.append(docs_dict[item_id])
    
    with open(target, "a", encoding="utf-8") as f:
        # Iterrate over sorted 
        for item in documents:
            # Get the raw HTML content
            raw_content = item.get_body_content()
                
            # Parse with BeautifulSoup to get plain text
            soup = BeautifulSoup(raw_content, 'html.parser')
            text = soup.get_text()
            
            # Clean the text if requested
            if clean:
                text = clean_text(text)
            
            # Append parsed text to file.txt
            f.write(text)


if __name__=="__main__":

    epub_files_list = [
        "Soldatenko_Eva.250281.fb2.epub",
        "Soldatenko_Kogda-utonet-cherepaha.529623.fb2.epub",
        "Soldatenko_Malenkaya-opera.629214.fb2.epub",
        "Soldatenko_Razvody-sbornik-.565292.fb2.epub",
        "Soldatenko_Santehnik_1_Santehnik-ego-kot-zhena-i-drugie-podrobnosti.194865.fb2.epub",
        "Soldatenko_Santehnik_2_Santehnik-Tvoyo-moyo-koleno.347883.fb2.epub",
        "Soldatenko_Santehnik_3_Posledniy-santehnik.430691.fb2.epub",
        "Soldatenko_Santehnik_4_Santehnik-s-pylu-i-s-zharom.533217.fb2.epub",
        "Soldatenko_Ves-santehnik-v-odnoy-stopke.393617.fb2.epub",
        "Soldatenko_Zhiraf.227925.fb2.epub"
    ]

    for i in range(len(epub_files_list)):
        epub_file = Path("..", "data", "epub_pesen", epub_files_list[i])
        txt_file_name = Path("..", "data", "txt_pesen", f"{epub_files_list[i].split(".epub")[0]}.txt")
        ascending_epub_convert_clean(epub_file, txt_file_name)
    
