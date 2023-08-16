import re # regular expressions
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal


pdf_results = []
q1_value = 'rio san juan'
# Recorre cada pagina y extrae sus elementos
for page_layout in extract_pages("MODELACIONRIOROJO.pdf"):
    q_count = 0
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            pag = element.get_text().lower()
            q_count += pag.count(q1_value)
    res = (len(pdf_results) + 1, q_count)
    pdf_results.append(res)

"""
No hay diferencia respecto a la funcion activa,
se siguen escapando incidencias. Sin embargo es interesante notar la
estructura jerarquica que utiliza pdfminer-six.
for page_layout in extract_pages("MODELACIONRIOROJO.pdf"):
    q_count = 0
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                if isinstance(text_line, LTTextLineHorizontal):
                    pag = text_line.get_text().lower()
                    q_count += pag.count(q1_value)
    res = (len(pdf_results) + 1, q_count)
    pdf_results.append(res)

"""
print(pdf_results)

#text = extract_text("PGARQUINDIO2020-2039_P372.pdf").lower()
#
#Ejemplo con expresiones regulares
#pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}") #any letter Mayus/Minus, le sigue una coma y por ultimo, un espacio.
# La solución es utilizar la notación de cadena de caracteres sin formato de Python para expresiones regulares;
# las barras invertidas no se manejan de ninguna manera especial en una cadena literal con el prefijo 'r'
# regular expression example
#matches = pattern.findall(text)
#print(matches)
#
#Ejemplo de match con expresion regular
#print(re.match(r'[Qq]uebrada[A-z]+', text))
#
#Ejemplo de Conteo
#q1_finder = 'quebradabarroblanco'
#q2_finder = 'qbarroblanco'
#q1_counts = text.count(q1_finder)
#q2_counts = text.count(q2_finder)
#print(q1_counts, q2_counts)
