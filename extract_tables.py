import tabula

def run():
    tables = tabula.read_pdf('PGARQUINDIO2020-2039_P372.pdf', pages='all')
    print(tables[0])
    print(tables[1])

if __name__ == '__main__':
    run()
