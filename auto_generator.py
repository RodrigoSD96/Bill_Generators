import re
import time
import PyPDF2
from tkinter import Tk
from selenium import webdriver
from tkinter.filedialog import askopenfilename
from selenium.webdriver.support.ui import Select


def axa_scan(text):
    pattern = re.compile(r"(Vida|No Vida|Acreditado|I.S.R.|Retenido)\s*:\s*\-*\$*(\d*\,?\d*.\d*)")
    match = dict(re.findall(pattern, text))
    return match


def q_scan(pdf, page=0):
    print(f'PDF #{pdf+1} loading...')
    Tk().withdraw()
    pdfFileObj = open(path := askopenfilename(), 'rb')  # creating a pdf file object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # creating a pdf reader object
    num_pages = pdfReader.numPages
    pageObj = pdfReader.getPage(page)  # creating a page object
    pattern = re.compile(r"(IMPORTE|I.V.A.|TOTAL|I.S.R.|LEY|NETAS)\s+:(\d*\,?\d*.\d*)")
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


def sat(company, m_y='nodate', d=0.0, v=0.0, isr=0.0, iva_ret=0.0):
    # Driver access
    gc = webdriver.Chrome('./chromedriver')
    gc.maximize_window()
    gc.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

    # Login
    btn_e_firma = gc.find_element_by_id('buttonFiel').click()
    btn_cer = gc.find_element_by_id('btnCertificate').click()
    btn_key = gc.find_element_by_id('btnPrivateKey').click()
    time.sleep(10)
    # password = gc.find_element_by_id('privateKeyPassword').send_keys('*****')
    btn_send = gc.find_element_by_id('submit').click()

    # Accessing to CFDI generator
    cfdi = gc.find_element_by_xpath(
        "//a[@href='https://pacsat.facturaelectronica.sat.gob.mx/Comprobante/CapturarComprobante']").click()

    # Selecting client
    client = Select(gc.find_element_by_name('Receptor.RfcCargado'))
    if company == 'SP':
        client.select_by_value('SPO830427DQ1 SEGUROS EL POTOSI, S.A.')
    elif company == 'Q':
        client.select_by_value('QCS931209G49 QUALITAS COMPAÑIA DE SEGUROS SA DE CV')
    elif company == 'A':
        client.select_by_value('ASE931116231 AXA SEGUROS SA DE CV')
    else:
        print('Error, compañía no registrada.')
    time.sleep(3)
    use = Select(gc.find_element_by_name('Receptor.UsoCFDIMoral'))
    use.select_by_value('G03 Gastos en general')
    time.sleep(3)
    next_tab = gc.find_element_by_xpath("//button[contains(@onclick,'clickTab')]").click()
    if company == 'SP':
        pay_condition = gc.find_element_by_id('CondicionesDePago').send_keys('Al contado')
    else:
        pay_condition = gc.find_element_by_id('CondicionesDePago').send_keys('En una sola exhibición')
    if d != 0:
        # Daños
        new_concept = gc.find_element_by_id('btnMuestraConcepto').click()
        service = gc.find_element_by_id('ClaveProdServ').send_keys(
            '80141600 Actividades de ventas y promoción de negocios')
        time.sleep(1)
        if company == 'Q':
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y + ' Agente 05886')
        elif company == 'A':
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y + ' Agente 124109')
        else:
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y)
        gc.find_element_by_id('ValorUnitario').clear()
        value = gc.find_element_by_id('ValorUnitario').send_keys(str(d))

        # ISR
        impuestos = gc.find_element_by_xpath("//a[contains(@onclick,'deshabilitaBotonAceptar')]").click()
        time.sleep(1)
        edit_isr = gc.find_element_by_xpath(
            "//table[@id='tablaConRetenciones']//tr[@indice='0']//span[@title='Editar']").click()
        # gc.find_element_by_id('Retenciones_Base').clear()
        # base = gc.find_element_by_id('Retenciones_Base').send_keys(str(d+v))
        gc.find_element_by_id('Retenciones_TasaOCuota').clear()
        percentage_isr = gc.find_element_by_id('Retenciones_TasaOCuota').send_keys(str(isr / d))
        refresh_isr = gc.find_element_by_id('btnAgregaConImpuestoRetenido').click()

        # IVA Retenido
        edit_iva = gc.find_element_by_xpath(
            "//table[@id='tablaConRetenciones']//tr[@indice='1']//span[@title='Editar']").click()
        gc.find_element_by_id('Retenciones_TasaOCuota').clear()
        percentage_iva = gc.find_element_by_id('Retenciones_TasaOCuota').send_keys(str(iva_ret / d))
        refresh_iva = gc.find_element_by_id('btnAgregaConImpuestoRetenido').click()

        # Finish edition of DAÑOS
        moveto_concept = gc.find_element_by_xpath("//a[@id='tabConceptosPrincipal']")
        gc.execute_script("arguments[0].click();", moveto_concept)
        time.sleep(1)
        add_concept = gc.find_element_by_xpath("//div[@id='tabConceptos']//button[@id='btnAceptarModal']").click()
        time.sleep(3)

    if company == 'SP' or company == 'A':
        # Vida
        gc.execute_script("scrollBy(0,-1000);")
        time.sleep(1)
        new_concept2 = gc.find_element_by_id('btnMuestraConcepto').click()
        service2 = gc.find_element_by_id('ClaveProdServ').send_keys('80141601 Servicios de promoción de ventas')
        time.sleep(1)
        if company == 'Q':
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y + ' Agente 05886')
        elif company == 'A':
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y + ' Agente 124109')
        else:
            description = gc.find_element_by_id('Descripcion').send_keys(' ' + m_y)
        gc.find_element_by_id('ValorUnitario').clear()
        value2 = gc.find_element_by_id('ValorUnitario').send_keys(str(v))

        # ISR
        impuestos2 = gc.find_element_by_xpath("//a[contains(@onclick,'deshabilitaBotonAceptar')]").click()
        time.sleep(1)
        if d == 0:
            edit_isr2 = gc.find_element_by_xpath(
                "//table[@id='tablaConRetenciones']//tr[@indice='0']//span[@title='Editar']").click()
            gc.find_element_by_id('Retenciones_TasaOCuota').clear()
            percentage_isr2 = gc.find_element_by_id('Retenciones_TasaOCuota').send_keys(str(isr / v))
            refresh_isr2 = gc.find_element_by_id('btnAgregaConImpuestoRetenido').click()
        # Finish edition of VIDA
        moveto_concept2 = gc.find_element_by_xpath("//a[@id='tabConceptosPrincipal']")
        gc.execute_script("arguments[0].click();", moveto_concept2)
        time.sleep(1)
        add_concept2 = gc.find_element_by_xpath("//div[@id='tabConceptos']//button[@id='btnAceptarModal']").click()
        time.sleep(3)

    # Time to verify quantities
    time.sleep(20)

    # Finish bill
    sellar = gc.find_element_by_xpath("//button[contains(@onclick,'sellar')]").click()

    # Sign
    last_password = gc.find_element_by_id('privateKeyPassword').send_keys('mawatary2019')
    btns = gc.find_elements_by_xpath("//span[@class='btn btn-default']")
    for span in btns:
        span.click()
    time.sleep(10)
    btn_confirm = gc.find_element_by_id('btnValidaOSCP').click()
    print('Facturation done!!!!')
    btn_sign = gc.find_element_by_id('btnFirmar').click()
    dl_pdf = gc.find_element_by_xpath('//span[@title="Descargar archivo XML"]')
    dl_xml = gc.find_element_by_xpath('//span[@title="Descargar representación impresa"]')
    time.sleep(200)


if __name__ == '__main__':
    try:
        print("Welcome to Bill Generator by Noriaki Mawatari")
        print('Companies:\nQ) Qualitas\nSP) Seguros el Potosí\nA) Axa Seguros')
        company = input('For which company do you want to make the bill:')
        m_y = input('Date:')

        if company == 'A':
            axa_content = open('./files/Axa.txt').read()
            print(f'Content:{axa_content}')
            matches = axa_scan(axa_content)
            d = float(matches['No Vida'].replace(',', ''))
            v = float(matches['Vida'].replace(',', ''))
            iva_tras = float(matches['Acreditado'].replace(',', ''))
            isr = float(matches['I.S.R.'].replace(',', ''))
            iva_ret = float(matches['Retenido'].replace(',', ''))
            print('\n|Facturando para AXA|')
            print(f'Comisión de Daños: {d}')
            print(f'Comisión de Vida: {v}')
            print(f'IVA Trasladado/Acreditado: {0.16 * d}')
            print(f'IVA Retenido: {iva_ret}')
            print(f'ISR: {isr}')
            if d != 0:
                print(f'Tasa de IVA Ret.: {round(iva_ret / d, 7)}')
                print(f'Tasa de ISR Daños: {round(isr / d, 7)}')
            else:
                print('Tasa de IVA Ret.: 0.0')
                print('Tasa de IVA Ret.: 0.0')
            print(f'Tasa de ISR Vida: {round(isr / v, 7)}')
            print(f'Subtotal: {d + v}')
            print(f'Total Impuestos Trasladados: {iva_tras}')
            print(f'Total Impuestos Retenidos: {isr + iva_ret}')
            print(f'Total: {v + d + iva_tras - iva_ret - isr}')
            sat(company, m_y, d=d, v=v, isr=isr, iva_ret=iva_ret)
        elif company == 'Q':
            val_unit = 0.0
            iva_tras = 0.0
            subtotal = 0.0
            isr = 0.0
            iva_ret = 0.0
            comision = 0.0
            print("Running Bill Generator for Quálitas files")
            num_pdfs = int(input("Number of PDF´s to scan? "))

            for pdf in range(num_pdfs):
                matches, num_pages = q_scan(pdf)
                if num_pages >= 2:
                    print(f'\nLoading next page in PDF: ')
                    val_unit += float(matches['IMPORTE'].replace(',', ''))
                    iva_tras += float(matches['I.V.A.'].replace(',', ''))
                    subtotal += float(matches['TOTAL'].replace(',', ''))
                    isr += float(matches['I.S.R.'].replace(',', ''))
                    iva_ret += float(matches['LEY'].replace(',', ''))
                    comision += float(matches['NETAS'].replace(',', ''))
                    print(f'Please select the file again to load next page')
                    matches, num_pages = q_scan(pdf, 1)

                    if num_pages >= 3:
                        print(f'\nLoading next page in PDF: ')
                        val_unit += float(matches['IMPORTE'].replace(',', ''))
                        iva_tras += float(matches['I.V.A.'].replace(',', ''))
                        subtotal += float(matches['TOTAL'].replace(',', ''))
                        isr += float(matches['I.S.R.'].replace(',', ''))
                        iva_ret += float(matches['LEY'].replace(',', ''))
                        comision += float(matches['NETAS'].replace(',', ''))
                        print(f'Please select the file again to load next page')
                        matches, num_pages = q_scan(pdf, 2)
                val_unit += float(matches['IMPORTE'].replace(',', ''))
                iva_tras += float(matches['I.V.A.'].replace(',', ''))
                subtotal += float(matches['TOTAL'].replace(',', ''))
                isr += float(matches['I.S.R.'].replace(',', ''))
                iva_ret += float(matches['LEY'].replace(',', ''))
                comision += float(matches['NETAS'].replace(',', ''))

            print('\n|Facturando para QUÁLITAS|')
            print(f'Valor Unitario: {round(val_unit, 2)}')
            print(f'ISR: {round(isr, 2)}')
            print(f'Tasa de ISR: {round(isr / val_unit, 6)}')
            print(f'Ret. I.V.A. Segun Ley: {round(iva_ret, 2)}')
            print(f'Tasa de IVA Ret.: {round(iva_ret / val_unit, 6)}')
            print(f'IVA Trasladado: {0.16 * val_unit}')
            print(f'Subtotal: {subtotal}')
            print(f'Total Impuestos Trasladados: {iva_tras}')
            print(f'Total Impuestos Retenidos: {isr + iva_ret}')
            print(f'Comisión neta: {comision}')

            sat(company, m_y, d=val_unit, isr=isr, iva_ret=iva_ret)

        elif company == 'SP':
            print('Facturando para Seguros el Potosí')

    except Exception as error:
        print('ERROR: ', error)
