import math
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk

# "error" para seleccionar la estacion origen o destino
get_estacion_precision = 10
# multiplicador para cuando hay transbordo
h_multiplier = 1000
# key = nombre de estación
# values = lista de estaciones colindantes, errores y coordenadas en el canvas
mapa = {'Aghia Paraskevi': [['3'], ['Halandri', 'Nomismatokopio'], 1000000, 1000000, (624, 443)],
        'Aghios Antonios': [['2'], ['Sepolia'], 1000000, 1000000, (143, 386)],
        'Aghios Dimitrias · Alexandros Panogulis': [['2'], ['Dafni'], 1000000, 1000000, (321, 852)],
        'Aghios Eleftherios': [['1'], ['Ano Patissia', 'Kato Patissia'], 1000000, 1000000, (299, 391)],
        'Aghios Ioannis': [['2'], ['Neos Kosmos', 'Dafni'], 1000000, 1000000, (321, 777)],
        'Aghios Nikolaos': [['1'], ['Attiki', 'Kato Patissia'], 1000000, 1000000, (245, 446)],
        'Airport': [['3'], ['Koropi'], 1000000, 1000000, (822, 635)],
        'Akropoli': [['2'], ['Syntagma', 'Sygrou - Fix'], 1000000, 1000000, (321, 664)],
        'Ambelokipi': [['3'], ['Panormou', 'Megaro Moussikis'], 1000000, 1000000, (491, 578)],
        'Ano Patissia': [['1'], ['Perissos', 'Aghios Eleftherios'], 1000000, 1000000, (325, 366)],
        'Attiki': [['1', '2'], ['Victoria', 'Aghios Nikolaos', 'Sepolia', 'Larissa Station'], 1000000, 1000000, (224, 468)],
        'Dafni': [['2'], ['Aghios Ioannis', 'Aghios Dimitrias · Alexandros Panogulis'], 1000000, 1000000, (321, 815)],
        'Doukissis Plokentias': [['3'], ['Halandri', 'Pallini'], 1000000, 1000000, (683, 386)],
        'Egaleo': [['3'], ['Eleonas'], 1000000, 1000000, (67, 506)],
        'Eleonas': [['3'], ['Kerameikos', 'Egaleo'], 1000000, 1000000, (120, 561)],
        'Ethniki Amyna': [['3'], ['Holargos', 'Katehaki'], 1000000, 1000000, (556, 510)],
        'Evangelismos': [['3'], ['Megaro Moussikis', 'Syntagma'], 1000000, 1000000, (400, 614)],
        'Faliro': [['1'], ['Moschato', 'Piraeus'], 1000000, 1000000, (140, 807)],
        'Halandri': [['3'], ['Doukissis Plokentias', 'Aghia Paraskevi'], 1000000, 1000000, (646, 421)],
        'Holargos': [['3'], ['Ethniki Amyna', 'Nomismatokopio'], 1000000, 1000000, (579, 488)],
        'Iraklio': [['1'], ['Nea Ionia', 'Irini'], 1000000, 1000000, (420, 270)],
        'Irini': [['1'], ['Neratziotissa', 'Iraklio'], 1000000, 1000000, (511, 260)],
        'Kallithea': [['1'], ['Tavros', 'Moschato'], 1000000, 1000000, (200, 751)],
        'KAT': [['1'], ['Kifissia', 'Maroussi'], 1000000, 1000000, (636, 168)],
        'Katehaki': [['3'], ['Ethniki Amyna', 'Panormou'], 1000000, 1000000, (534, 532)],
        'Kato Patissia': [['1'], ['Aghios Nikolaos', 'Aghios Eleftherios'], 1000000, 1000000, (273, 418)],
        'Kerameikos': [['3'], ['Monastiraki', 'Eleonas'], 1000000, 1000000, (162, 602)],
        'Kifissia': [['1'], ['KAT'], 1000000, 1000000, (677, 126)],
        'Koropi': [['3'], ['Airport', 'Paiania - Kantza'], 1000000, 1000000, (745, 603)],
        'Larissa Station': [['2'], ['Attiki', 'Metaxourghio'], 1000000, 1000000, (224, 511)],
        'Maroussi': [['1'], ['KAT', 'Neratziotissa'], 1000000, 1000000, (595, 209)],
        'Megaro Moussikis': [['3'], ['Ambelokipi', 'Evangelismos'], 1000000, 1000000, (468, 601)],
        'Metaxourghio': [['2'], ['Omonia', 'Larissa Station'], 1000000, 1000000, (223, 546)],
        'Monastiraki': [['1', '3'], ['Omonia', 'Thissio', 'Kerameikos', 'Syntagma'], 1000000, 1000000, (270, 615)],
        'Moschato': [['1'], ['Kallithea', 'Faliro'], 1000000, 1000000, (172, 779)],
        'Nea Ionia': [['1'], ['Pefkakia', 'Iraklio'], 1000000, 1000000, (396, 294)],
        'Neos Kosmos': [['2'], ['Sygrou - Fix', 'Aghios Ioannis'], 1000000, 1000000, (321, 740)],
        'Neratziotissa': [['1'], ['Irini', 'Maroussi'], 1000000, 1000000, (547, 256)],
        'Nomismatokopio': [['3'], ['Aghia Paraskevi', 'Holargos'], 1000000, 1000000, (602, 466)],
        'Omonia': [['1', '2'], ['Victoria', 'Panepistimio', 'Metaxourghio', 'Monastiraki'], 1000000, 1000000, (269, 570)],
        'Paiania - Kantza': [['3'], ['Koropi', 'Pallini'], 1000000, 1000000, (745, 470)],
        'Pallini': [['3'], ['Paiania - Kantza', 'Doukissis Plokentias'], 1000000, 1000000, (745, 411)],
        'Panepistimio': [['2'], ['Omonia', 'Syntagma'], 1000000, 1000000, (298, 594)],
        'Panormou': [['3'], ['Katehaki', 'Ambelokipi'], 1000000, 1000000, (513, 556)],
        'Pefkakia': [['1'], ['Nea Ionia', 'Perissos'], 1000000, 1000000, (374, 317)],
        'Perissos': [['1'], ['Pefkakia', 'Ano Patissia'], 1000000, 1000000, (348, 341)],
        'Petralona': [['1'], ['Thissio', 'Tavros'], 1000000, 1000000, (258, 692)],
        'Piraeus': [['1'], ['Faliro'], 1000000, 1000000, (27, 821)],
        'Sepolia': [['2'], ['Aghios Antonios', 'Attiki'], 1000000, 1000000, (183, 428)],
        'Sygrou - Fix': [['2'], ['Akropoli', 'Neos Kosmos'], 1000000, 1000000, (321, 702)],
        'Syntagma': [['2', '3'], ['Panepistimio', 'Akropoli', 'Evangelismos', 'Monastiraki'], 1000000, 1000000, (317, 614)],
        'Tavros': [['1'], ['Petralona', 'Kallithea'], 1000000, 1000000, (228, 721)],
        'Thissio': [['1'], ['Monastiraki', 'Petralona'], 1000000, 1000000, (269, 662)],
        'Victoria': [['1'], ['Attiki', 'Omonia'], 1000000, 1000000, (269, 533)]}

# MAIN
def main():
    # Función a ejecutar al apretar el botón
    def onClick():
        print("ok")
    
    # INICIO DE APLICACIÓN
    # Ventana
    master = Tk()
    # Márgenes
    master.config(bd=20)
    master.title("METRO ATENAS")
    # Dimensiones de la imagen de fondo (mapa.png)
    master.geometry("400x300")
    master.resizable(True, True)
    
    # Imagen del logo del metro de Atenas
    image = Image.open("logo.png")
    # Ajuste del tamaño de la imagen
    logo = image.resize((65,65))
    test = ImageTk.PhotoImage(logo)
    
    # Bienvenida a la aplicación (imagen anterior)
    welcome = Label(master, text="", image=test)
    welcome.image = test
    welcome.pack()
    
    # Separador
    salto = Label(master, text="")
    salto.pack()
    
    # Valores de los desplegables
    values = [*mapa]
    
    # Personalizamos los textos
    label_style = Style()
    label_style.configure('W.Label', font=('calibri', 13))
    
    # Texto de origen
    selO = Label(master, text="Seleccione estación de origen", style='W.Label')
    selO.pack()
    # Input de origen
    origen = ttk.Combobox(master, value=values)
    origen.current(0)
    origen.bind("<<ComboboxSelected>>")
    origen.pack()
    
    # Texto destino
    selD = Label(master, text="Seleccione estación de destino", style='W.Label')
    selD.pack()
    # Input destino
    destino = ttk.Combobox(master, value=values)
    destino.current(0)
    destino.bind("<<ComboboxSelected>>")
    destino.pack()
    
    # Separador
    salto = Label(master, text="")
    salto.pack()
    
    # Personalizamos el botón
    button_style = Style()
    button_style.configure('W.TButton', font=('calibri', 10, 'bold'))
    
    # Botón para calcular el camino
    button = Button(master, text="BUSCAR MEJOR RUTA", style='W.TButton', command=onClick)
    button.pack()
    
    master.mainloop()
    
if __name__ == '__main__':
    main()