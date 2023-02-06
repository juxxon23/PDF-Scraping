import re # regular expressions
from pdfminer.high_level import extract_pages, extract_text

# Recorre cada pagina y extrae sus elementos
for page_layout in extract_pages("PGARQUINDIO2020-2039_P372.pdf"):
    for element in page_layout:
        print(element)

text = extract_text("PGARQUINDIO2020-2039_P372.pdf")
print(text)


# regular expression example
# pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}") #any letter Mayus/Minus, le sigue una coma y por ultimo, un espacio.
# matches = pattern.findall(text)
# print(matches)
