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
        r"(IMPORTE|I.V.A.|SUB-TOTAL|RETENCION I.S.R.|RET. I.V.A. SEGUN LEY|COMISIONES NETAS)\s+:(\d*\,?\d*.\d*)")
    text = pageObj.extractText()  # extracting text from page
    print(text)
    pdfFileObj.close()  # closing the pdf file object
    matches = dict(re.findall(pattern, text))
    print(matches)
    print("File scanned successfully!")
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
                print(f'Loading first page in PDF: ')
                val_unit += float(matches['IMPORTE'].replace(',', ''))
                iva_tras += float(matches['I.V.A.'].replace(',', ''))
                subtotal += float(matches['SUB-TOTAL'].replace(',', ''))
                isr += float(matches['RETENCION I.S.R.'].replace(',', ''))
                iva_ret += float(matches['RET. I.V.A. SEGUN LEY'].replace(',', ''))
                comision += float(matches['COMISIONES NETAS'].replace(',', ''))
                print(f'Please select the file again to load next page')
                matches, num_pages = scan(pdf, 1)
            val_unit += float(matches['IMPORTE'].replace(',', ''))
            iva_tras += float(matches['I.V.A.'].replace(',', ''))
            subtotal += float(matches['SUB-TOTAL'].replace(',', ''))
            isr += float(matches['RETENCION I.S.R.'].replace(',', ''))
            iva_ret += float(matches['RET. I.V.A. SEGUN LEY'].replace(',', ''))
            comision += float(matches['COMISIONES NETAS'].replace(',', ''))

        print('|Facturando para QUÁLITAS|')
        print(f'Valor Unitario: {val_unit}')
        print(f'Tasa de ISR: {isr/val_unit}')
        print(f'Tasa de IVA Ret.: {iva_ret/val_unit}')
        print(f'IVA Trasladado: {0.16*val_unit}')
        print(f'Subtotal: {subtotal}')
        print(f'Total Impuestos Trasladados: {iva_tras}')
        print(f'Total Impuestos Retenidos: {isr+iva_ret}')
        print(f'Total: {comision}')
    except Exception as error:
        print('ERROR: ', error)
