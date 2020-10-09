'''
Bill Generator for Qualitas Insurance Company
Tkinter Version
October/2020
by Noriaki Mawatari
'''
from tkinter import *


def Facturar():
    IVATras.set(float(0.16) * float(D.get()))
    IVARet.set(float(IVAR.get()) / float(D.get()))
    ISR_P.set(float(ISR.get()) / float(D.get()))
    Subtotal.set(float(D.get()) + float(IVAT.get()))
    ImpRet.set(float(IVAR.get()) + float(ISR.get()))
    MTN.set(float(D.get()) + float(IVAT.get()) - float(ISR.get()) - float(IVAR.get()))

# Función que guarda datos
def Guardar():
    D.set(float(D1.get()) + float(D2.get()) + float(D3.get()))
    IVAT.set(float(IVAT1.get()) + float(IVAT2.get()) + float(IVAT3.get()))
    ISR.set(float(ISR1.get()) + float(ISR2.get()) + float(ISR3.get()))
    IVAR.set(float(IVAR1.get()) + float(IVAR2.get()) + float(IVAR3.get()))

# Función que limpia
def borrar():
    D1.set("")
    D2.set("")
    D3.set("")
    D.set("")
    IVAR1.set("")
    IVAR2.set("")
    IVAR3.set("")
    IVAR.set("")
    ISR1.set("")
    ISR2.set("")
    ISR3.set("")
    ISR.set("")
    IVAT1.set("")
    IVAT2.set("")
    IVAT3.set("")
    IVAT.set("")
    Subtotal.set("")
    ISR_P.set("")
    MTN.set("")
    ImpRet.set("")

root = Tk()             #Se crea la interfaz con Tkinter
root.title("Generador de Facturas de Qualitas AGENTE 05886")

D1 = StringVar()
D2 = StringVar()
D3 = StringVar()
D = StringVar()         #Importe
IVAT1 = StringVar()
IVAT2 = StringVar()
IVAT3 = StringVar()
IVAT = StringVar()      #IVA Trasladado
IVATras = StringVar()
IVAR1 = StringVar()
IVAR2 = StringVar()
IVAR3 = StringVar()
IVAR = StringVar()      #IVA Retenido
IVARet = StringVar()
ISR1 = StringVar()
ISR2 = StringVar()
ISR3 = StringVar()
ISR = StringVar()
ISR_P = StringVar()     # % de ISR
Subtotal = StringVar()
MTN = StringVar()
ImpRet = StringVar()

## Creación de menú
menubar = Menu(root)
root.config(menu = menubar)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nueva Factura", command=borrar)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Ayuda")
helpmenu.add_separator()
helpmenu.add_command(label="Acerca de...")

menubar.add_cascade(label = "Archivo", menu = filemenu)
menubar.add_cascade(label = "Ayuda", menu = helpmenu)

## Creacion de los frames

inputframe = Frame(root)
inputframe.pack(side = LEFT)

outputframe = Frame(root)
outputframe.pack(side = RIGHT)

column2 = Frame(inputframe)
column2.pack(side = LEFT)

column3 = Frame(column2)
column3.pack(side = LEFT)

## Columna 1er Decena del Mes

Label(column3, text="1er Importe:").pack(anchor = "w")
Entry(column3, justify="center", textvariable = D1).pack(anchor = "w")

Label(column3, text="IVA Trasladado:").pack(anchor = "w")
Entry(column3, justify="center", textvariable = IVAT1).pack(anchor = "w")

Label(column3, text="ISR:").pack(anchor = "w")
Entry(column3, justify="center", textvariable = ISR1).pack(anchor = "w")

Label(column3, text="IVA Retenido:").pack(anchor = "w")
Entry(column3, justify="center", textvariable = IVAR1).pack(anchor = "w")

Label(column3, text="").pack(anchor="w")
Button(column3, text="Guardar Datos", command=Guardar).pack(side="bottom")

## Columna 2da Decena del Mes

Label(column2, text="2do Importe:").pack(anchor = "w")
Entry(column2, justify="center", textvariable = D2).pack(anchor = "w")

Label(column2, text="IVA Trasladado:").pack(anchor = "w")
Entry(column2, justify="center", textvariable = IVAT2).pack(anchor = "w")

Label(column2, text="ISR:").pack(anchor = "w")
Entry(column2, justify="center", textvariable = ISR2).pack(anchor = "w")

Label(column2, text="IVA Retenido:").pack(anchor = "w")
Entry(column2, justify="center", textvariable = IVAR2).pack(anchor = "w")



## Columna 3er Decena del Mes

Label(inputframe, text="3er Importe:").pack(anchor = "w")
Entry(inputframe, justify="center", textvariable = D3).pack(anchor = "w")

Label(inputframe, text="IVA Trasladado:").pack(anchor = "w")
Entry(inputframe, justify="center", textvariable = IVAT3).pack(anchor = "w")

Label(inputframe, text="ISR:").pack(anchor = "w")
Entry(inputframe, justify="center", textvariable = ISR3).pack(anchor = "w")

Label(inputframe, text="IVA Retenido:").pack(anchor = "w")
Entry(inputframe, justify="center", textvariable = IVAR3).pack(anchor = "w")

Label(inputframe, text="").pack(anchor="w")
Button(inputframe, text="Generar Factura", command=Facturar).pack(side="bottom")

## Resultados

Label(outputframe, text="Importe:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=D).pack()

Label(outputframe, text="IVA Trasladado:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=IVAT).pack()

Label(outputframe, text="Subtotal:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=Subtotal).pack()

Label(outputframe, text="% de ISR:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=ISR_P).pack()

Label(outputframe, text="% de IVA Retenido:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=IVARet).pack()

Label(outputframe, text="Impuestos Retenidos (ISR):").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=ISR).pack()

Label(outputframe, text="Impuestos Retenidos (IVA):").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=IVAR).pack()

Label(outputframe, text="Total de Imp. Trasladados:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=IVAT).pack()

Label(outputframe, text="Total de Imp. Retenidos:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=ImpRet).pack()

Label(outputframe, text="Comisiones Netas:").pack(anchor = "w")
Entry(outputframe, justify="center", textvariable=MTN).pack()
Label(outputframe, text="").pack(anchor="w")


root.mainloop() #Siempre va abajo de todo

