'''
Bill Generator for Qualitas Insurance Company
October/2020
by Noriaki Mawatari
'''
import re
import PyPDF2
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def scan(pdf, page=0):
    print(f'PDF #{pdf+1} loading...')
    Tk().withdraw()
    pdfFileObj = open(path := askopenfilename(), 'rb')  # creating a pdf file object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # creating a pdf reader object
    num_pages = pdfReader.numPages
    pageObj = pdfReader.getPage(page)  # creating a page object
    pattern = re.compile(
        r"(IMPORTE|I.V.A.|TOTAL|I.S.R.|LEY|NETAS)\s+:(\d*\,?\d*.\d*)")
    text = pageObj.extractText()  # extracting text from page
    print(f'\nVisualization of PDF´s text: {text}')
    pdfFileObj.close()  # closing the pdf file object
    matches = dict(re.findall(pattern, text))
    print(f'\nExtracted text from PDF: {matches}')
    if matches == dict():
        matches = dict([('IMPORTE', '0.00'), ('I.V.A.', '0.00'), ('TOTAL', '0.00'), ('I.S.R.', '0.00'), ('LEY', '0.00'),
                        ('NETAS', '0.00')])
    print("\nFile scanned successfully!")
    return matches, num_pages


if __name__ == '__main__':
    try:
        val_unit = 0.0
        iva_tras = 0.0
        subtotal = 0.0
        isr = 0.0
        iva_ret = 0.0
        comision = 0.0
        print("Running Bill Generator for Quálitas files")
        num_pdfs = int(input("Number of PDF´s to scan? "))

        for pdf in range(num_pdfs):
            matches, num_pages = scan(pdf)
            if num_pages == 2:
                print(f'\nLoading bonus page in PDF: ')
                val_unit += float(matches['IMPORTE'].replace(',', ''))
                iva_tras += float(matches['I.V.A.'].replace(',', ''))
                subtotal += float(matches['TOTAL'].replace(',', ''))
                isr += float(matches['I.S.R.'].replace(',', ''))
                iva_ret += float(matches['LEY'].replace(',', ''))
                comision += float(matches['NETAS'].replace(',', ''))
                print(f'Please select the file again to load next page')
                matches, num_pages = scan(pdf, 1)
            val_unit += float(matches['IMPORTE'].replace(',', ''))
            iva_tras += float(matches['I.V.A.'].replace(',', ''))
            subtotal += float(matches['TOTAL'].replace(',', ''))
            isr += float(matches['I.S.R.'].replace(',', ''))
            iva_ret += float(matches['LEY'].replace(',', ''))
            comision += float(matches['NETAS'].replace(',', ''))

        print('\n|Facturando para QUÁLITAS|')
        print(f'Valor Unitario: {val_unit}')
        print(f'Tasa de ISR: {round(isr/val_unit,6)}')
        print(f'Tasa de IVA Ret.: {round(iva_ret/val_unit,6)}')
        print(f'IVA Trasladado: {0.16*val_unit}')
        print(f'Subtotal: {subtotal}')
        print(f'Total Impuestos Trasladados: {iva_tras}')
        print(f'Total Impuestos Retenidos: {isr+iva_ret}')
        print(f'Total: {comision}')
    except Exception as error:
        print('ERROR: ', error)
