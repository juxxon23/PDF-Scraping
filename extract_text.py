import re # regular expressions
import json
import pandas as pd
import numpy as np
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def generate():
    exclude_words = ["interseccion", "bocatoma", "estacion", "monitoreo", "cañada", "nacimiento", "rio"]
    qdf = pd.read_csv('docs/nodos.csv')
    cols = qdf.columns
    number_nodes = qdf[cols[0]]
    name_nodes = [qdf.loc[qdf[cols[0]] == num_node, [cols[0], cols[2]]] for num_node in number_nodes] # Number - Name
    qr = {}
    for nam_node in name_nodes:
        for row in nam_node.index:
            ex_count = 0
            for ex in exclude_words:
                if ex in nam_node.loc[row][cols[2]]:
                    ex_count += 1
            if ex_count == 0:
                val = (nam_node.loc[row][cols[2]]).replace("quebrada", " ").strip()
                qr[int(nam_node.loc[row][cols[0]])] = [val]
    return qr


def add_dict(qr):
    for k in qr.keys():
        qr[k].append({})
    return qr


def push_elem_dict(qr, value):
    for k in qr.keys():
        qr[k][len(qr[k])-1][value] = 0
    return qr


def write_json(qr):
    with open("q_pdf_count.json", 'w') as new_file:
        json.dump(qr, new_file, indent=4, cls=NpEncoder)


def search():
    pdf_names = ["MODELACIONRIOROJO",
                 "MODELACIONRIOAZUL",
                 "modelaciondelacalidaddelaguariosanjuanmunicipiogenovaquindio",
                 "modelaciondelacalidaddelaguarioroblemunicipioscircasiamontenegroquindio",
                 "Informe-de-Evaluacion-de-Meta-Global-de-Carga-Contaminante-Ano-2021"]
    qr = generate()
    for pdf_name in pdf_names:
        qr = add_dict(qr)
        qr = push_elem_dict(qr, pdf_name)
        for page_layout in extract_pages(f"docs/crq/{pdf_name}.pdf"): #Recorre las paginas
            for element in page_layout: #Recorre los elementos de una pagina
                if isinstance(element, LTTextContainer):
                    pag = element.get_text().lower()
                    for k in qr.keys():
                        #q_count += pag.count(qr[k][0])
                        qr[k][len(qr[k])-1][pdf_name] += pag.count(qr[k][0]) #falta definir res
    return qr


qr1 = search()
write_json(qr1)
#print(qr1)






#cont = 0
#for i in q_nodes['nombre_fixed']:
#    if "quebrada" not in i:
#        print(i)
#        cont += 1
#for i in name_nodes:
#    print(i[cols[2]])
#q1_value = 'rio san juan'



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
#print(pdf_results)

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
