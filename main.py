import math
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
import networkx as nx
import datetime


# --------------------------------------------------------------------------------------------------------------------------------
# FUNCIONES GENERALES
# Calcula la distancia eucídea entre 2 pixeles (puntos)
def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

# Función para calcular el tiempo total del camino
def tiempo(km, vel):
        return (km/vel)*60

# Resetea los valores de g y f del mapa (para poder hacer llamadas sucesivas a aStar)
def reset():
    for e in mapa.keys():
        ee = mapa.get(e)
        ee[2] = 1000000
        ee[3] = 1000000
        
# Función para invertir una lista
def reverse_list(arr):
    left = 0
    right = len(arr)-1
    while (left < right):
        # Swap
        temp = arr[left]
        arr[left] = arr[right]
        arr[right] = temp
        left += 1
        right -= 1
 
    return arr

# --------------------------------------------------------------------------------------------------------------------------------
# DATOS
Grafo = nx.Graph() 

# Lista estaciones
l1 = ["Piraeus","Faliro","Moschato","Kallithea","Tavros","Petralona","Thissio","Monastiraki","Omonia","Victoria","Attiki",
"Aghios Nikolaos","Kato Patissia","Aghios Eleftherios","Ano Patissia","Perissos","Pefkakia","Nea Ionia","Iraklio","Irini",
"Neratziotissa","Maroussi","Kat","Kifissia"]

l2 = ["Aghios Antonios","Sepolia","Attiki","St.Larissis","Metaxourghio","Omonia","Panepistimio","Syntagma","Akropoli",
"Sygrou - Fix","Neos Kosmos","Aghios Ioannis","Dafni","Aghios Dimitrios"]

l3 = ["Egaleo","Eleonas","Kerameikos","Monastiraki","Syntagma","Evangelismos","Megaro Moussikis","Ambelokipi","Panormou",
"Katehaki","Ethniki Amyna","Holargos","Nomismatokopio","Aghia Paraskevi","Halandri","Doukissis Plakentias","Pallini",
"Paiania - Kantza","Koropi","Airport"]

coordL1 = [ #verde
    [37.94823850613788, 23.64315408285978],
    [37.9451479545681, 23.66522510003948],
    [37.944314639017264, 23.6780228846546],
    [37.96052252591585, 23.697396473018113],
    [37.962651992557234, 23.703304769309177],
    [37.968797418927856, 23.7092896576727],
    [37.97690381355721, 23.72071682883635],
    [37.98422982753675, 23.727365547670388],  #Monastiraki 107 
    [37.98439440622449, 23.728670542327293], #omonia 108 
    [37.99317366581129, 23.730443307163007],
    [37.999510676546244, 23.722893989963133], #atikki  110 
    [38.00702044361351, 23.72773245767271],
    [38.01121696941966, 23.729171071163652],
    [38.02017553816614, 23.731821842327292],
    [38.024606358140865, 23.735964000238635],
    [38.03282095724069, 23.744627084654592],
    [38.03728040233875, 23.75022264418176],
    [38.041496945556325, 23.754790271163657],
    [38.04641478367594, 23.76623100185446],
    [38.043842242038075, 23.782925847890684],
    [38.04518864001822, 23.793099955821173],
    [38.05637630275381, 23.80502291534307],
    [38.0648704104849, 23.80942425582117],
    [38.07385906445477, 23.808288642328474],
]

coordL2 = [ #roja
    [38.006838626856, 23.699566830686127],
    [38.00273946681484, 23.71350533028026],
    [37.999510676546244, 23.722893989963133], #attiki 202
    [37.99209656962052, 23.72108144602919],
    [37.98692004297806, 23.72107721534306],
    [37.98439440622449, 23.728670542327293],  #omonia 205
    [37.98058961718604, 23.7329942269854],
    [37.97466748997125, 23.735179269313868], #syntagma 207
    [37.96884315445523, 23.7296007],
    [37.964730362866355, 23.726703786507297],
    [37.95725278747033, 23.727116886507297],
    [37.95675237540244, 23.73464052671532],
    [37.94941410696725, 23.737201842328467],
    [37.9407216868299, 23.740651626985407],

]

coordL3 = [ #azul
    [37.99312672457056, 23.681853444485967],
    [37.98799138458003, 23.692493826371965],
    [37.97879068094447, 23.711468777911087],
    [37.98422982753675, 23.727365547670388],  #monastiraki 303
    [37.97485841331983, 23.73572221287824],   #syntagma 304
    [37.97789320982388, 23.747513053498594],
    [37.979405375082905, 23.752794280344904],
    [37.99006871784915, 23.763502847941332],
    [37.9875310831905, 23.757003064810554],
    [37.97842556393126, 23.725482261108393],
    [38.000172341569225, 23.785697353358984],
    [38.004662696067356, 23.794765912879182],
    [38.009459377101955, 23.805660839866047],
    [38.01694440206896, 23.812643268701787],
    [38.02198729600681, 23.82118582159681],
    [38.024637240817626, 23.834343611030846],
    [38.006443606192946, 23.869669102563552],
    [37.9923274312594, 23.728648633681974],
    [37.913094624155384, 23.8957992686985],
    [37.935733311979725, 23.948431699581214],
]

# key = nombre de estación
# values = lista de listas de números de línea y coordenadas en el canvas
mapa = {'Aghia Paraskevi': [['3'], (624, 443)],
        'Aghios Antonios': [['2'], (143, 386)],
        'Aghios Dimitrios': [['2'], (321, 852)],
        'Aghios Eleftherios': [['1'], (299, 391)],
        'Aghios Ioannis': [['2'], (321, 777)],
        'Aghios Nikolaos': [['1'], (245, 446)],
        'Airport': [['3'], (822, 635)],
        'Akropoli': [['2'], (321, 664)],
        'Ambelokipi': [['3'], (491, 578)],
        'Ano Patissia': [['1'], (325, 366)],
        'Attiki': [['1', '2'], (224, 468)],
        'Dafni': [['2'], (321, 815)],
        'Doukissis Plakentias': [['3'], (683, 386)],
        'Egaleo': [['3'], (67, 506)],
        'Eleonas': [['3'], (120, 561)],
        'Ethniki Amyna': [['3'], (556, 510)],
        'Evangelismos': [['3'], (400, 614)],
        'Faliro': [['1'], (140, 807)],
        'Halandri': [['3'], (646, 421)],
        'Holargos': [['3'], (579, 488)],
        'Iraklio': [['1'], (420, 270)],
        'Irini': [['1'], (511, 260)],
        'Kallithea': [['1'], (200, 751)],
        'KAT': [['1'], (636, 168)],
        'Katehaki': [['3'], (534, 532)],
        'Kato Patissia': [['1'], (273, 418)],
        'Kerameikos': [['3'], (162, 602)],
        'Kifissia': [['1'], (677, 126)],
        'Koropi': [['3'], (745, 603)],
        'Larissa Station': [['2'], (224, 511)],
        'Maroussi': [['1'], (595, 209)],
        'Megaro Moussikis': [['3'], (468, 601)],
        'Metaxourghio': [['2'], (223, 546)],
        'Monastiraki': [['1', '3'], (270, 615)],
        'Moschato': [['1'], (172, 779)],
        'Nea Ionia': [['1'], (396, 294)],
        'Neos Kosmos': [['2'], (321, 740)],
        'Neratziotissa': [['1'], (547, 256)],
        'Nomismatokopio': [['3'], (602, 466)],
        'Omonia': [['1', '2'], (269, 570)],
        'Paiania - Kantza': [['3'], (745, 470)],
        'Pallini': [['3'], (745, 411)],
        'Panepistimio': [['2'], (298, 594)],
        'Panormou': [['3'], (513, 556)],
        'Pefkakia': [['1'], (374, 317)],
        'Perissos': [['1'], (348, 341)],
        'Petralona': [['1'], (258, 692)],
        'Piraeus': [['1'], (27, 821)],
        'Sepolia': [['2'], (183, 428)],
        'Sygrou - Fix': [['2'], (321, 702)],
        'Syntagma': [['2', '3'], (317, 614)],
        'Tavros': [['1'], (228, 721)],
        'Thissio': [['1'], (269, 662)],
        'Victoria': [['1'], (269, 533)]
        }

# --------------------------------------------------------------------------------------------------------------------------------
# FUNCIÓN DEL ALGORITMO A*

long1 = len(l1)
long2 = len(l2)
long3 = len(l3)

for i in range(long1):
    Grafo.add_node(l1[i], cor = coordL1[i]) #n-name c-coordenada code
    
    if(i >= 1): 
     Grafo.add_edge(l1[i-1], l1[i], cc = 'verde') #cc-color

for i in range(long2):
    Grafo.add_node(l2[i], cor = coordL2[i])
    
    if(i >= 1): 
     Grafo.add_edge(l2[i-1], l2[i], cc = 'rojo')
    
for i in range(long3):
    Grafo.add_node(l3[i], cor = coordL3[i])
    
    if(i >= 1): 
        Grafo.add_edge(l3[i-1], l3[i], cc ='azul')

def AEstrella(Grafo, origen, fin):
    visitados = [origen]  # Lista de posibles nodos a explorar
    novisitados = []  # Lista de nodos explorados
    actual = origen
    camino = nx.Graph()  # resultado

    g = {origen: 0}  # Valor real de la distancia del origen al elemento
    # Aproximacion del elemento al nodo fin
    h = {origen: distancia(
        Grafo.nodes[origen]['cor'], Grafo.nodes[fin]['cor'])}
    f = {origen: g[origen]+h[origen]}
    padre = {}  # Nodo padre

    # Bucle hasta que encuentra el nodo final
    while (not (actual == fin)):
        vecinos = list(Grafo.neighbors(actual))

        # De todos los nodos adyacentes eliminamos los que ya teniamos antes
        for x in vecinos:
            if ((x in novisitados) or (x in visitados)):
                vecinos.remove(x)

        # Metemos los nuevos posibles nodos en la lista novisitados
        novisitados.extend(vecinos)

        for x in visitados:
            if (x in novisitados):
                novisitados.remove(x)

        # Bucle que calcula los padres, la g, h y f de la lista novisitados
        for x in novisitados:
            # Si acabamos de añadir el nodo a novisitados ponemos como padre al nodo actual
            if (x in vecinos):
                padre[x] = actual
                
            # Comprobamos si hay un posible mejor nodo padre
            adyacentes = list(Grafo.neighbors(x))
            for y in adyacentes:
                if ((y in visitados) and (g[y] < g[padre[x]])):
                    padre[actual] = y
                    
            # El valor de g es el g del padre + la distancia del nodo al padre
            g[x] = g[padre[x]] + \
                distancia(Grafo.nodes[padre[x]]['cor'], Grafo.nodes[x]['cor'])
                
            # Actualizamos la g con el transbordo
            transbordo = True
            if (x in l1 and padre[x] in l1):
                transbordo = False
            if (x in l2 and padre[x] in l2):
                transbordo = False
            if (x in l3 and padre[x] in l3):
                transbordo = False

            if (transbordo):
                weekend = [5, 6]  # fines de semana [Saturday, Sunday]
                date = datetime.date.today()
                day = datetime.date.isoweekday(date)
                now = datetime.datetime.now().hour  # dia fecha y hora
                
                if (day == 5 or day == 6):
                    g[x] += 7
                    
                else:
                    g[x] += 3  # entre 3 y 10 mins

            # Calculamos ahora la h y la f
            h[x] = distancia(Grafo.nodes[x]['cor'], Grafo.nodes[fin]['cor'])
            f[x] = g[x]+h[x]

        # Cambiamos la posicion a la del menor f
        menor = f[novisitados[0]]
        actual = novisitados[0]
        for x in novisitados:
            if f[x] < menor:
                actual = x
                menor = f[x]

        # Metemos la posicion actual en la lista visitados
        novisitados.remove(actual)
        visitados.append(actual)

    # Recorremos el camino al reves, guiados por los nodos padre
    while (actual != origen):
        camino.add_node(actual)
        actual = padre[actual]
        
    camino.add_node(origen)  # Añadimos el origen tambien

    # Hallamos la distancia y el tiempo estimado
    dist = g[fin]*1000

    time = tiempo(g[fin], 80) + (camino.number_of_nodes()-1)*0.7

    return camino, dist, time

# --------------------------------------------------------------------------------------------------------------------------------
# MAIN
def main():
    # Función a ejecutar al apretar el botón
    def onClick():
        # Popup (nueva ventana) al pulsar el botón
        popup = Toplevel()
        popup.title("MAPA DE RUTA")
        
        # Dimensiones del popup
        popup.geometry(f'900x908+100+0')
        popup.resizable(True, True)

        # Creamos el lienzo donde dibujar el camino
        canvas = Canvas(popup, width=900, height=986)
        canvas.pack()
        
        # Imagen del mapa
        bg = PhotoImage(file='mapa.png')
        # Establecemos la imagen
        canvas.create_image(450, 454, image=bg)

        borrar_linea = []

        # Valores de origen y destino introducidos
        start = origen.get()
        end = destino.get()
        
        # Si no se introduce origen
        if start == "":
            print("No existe estación origen.")
            
        # Si no se introduce destino
        elif end == "":
            print("No existe estación destino.")
            
        # Se ha introducido origen y destino
        else:
            # Origen y destino existen
            if start in values and end in values:
                # Borrar los caminos antiguos del mapa
                for e in borrar_linea:
                    canvas.delete(e)
                    
                borrar_linea.clear()
                # Calcular el mínimo camino
                path = reverse_list(list(AEstrella(Grafo, start, end)[0].nodes()))
                prev = path[0]
                
                # Representar el camino
                for i in path[1:]:
                    try:
                        l_curr = mapa.get(i)[0]
                        l_prev = mapa.get(prev)[0]
                        c_curr = mapa.get(i)[1]
                        c_prev = mapa.get(prev)[1]
                        
                    except TypeError as e:
                        print(e)
                        
                    # Si hay curva en el mapa
                    if i in ['Iraklio', 'Irini'] and prev in ['Iraklio', 'Irini']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 433, 260,
                                                               fill='#155e29', width=5))
                        borrar_linea.append(canvas.create_line(433, 260, c_curr[0], c_curr[1],
                                                               fill='#155e29', width=5))
                        
                    elif i in ['Victoria', 'Attiki'] and prev in ['Victoria', 'Attiki']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 268, 514,
                                                               fill='#155e29', width=5))
                        borrar_linea.append(canvas.create_line(268, 514, c_curr[0], c_curr[1],
                                                               fill='#155e29', width=5))
                        
                    elif i in ['Metaxourghio', 'Omonia'] and prev in ['Metaxourghio', 'Omonia']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 228, 565,
                                                               fill='#a51b0b', width=5))
                        borrar_linea.append(canvas.create_line(228, 565, c_curr[0], c_curr[1],
                                                               fill='#a51b0b', width=5))
                        
                    elif i in ['Kerameikos', 'Monastiraki'] and prev in ['Kerameikos', 'Monastiraki']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 180, 612,
                                                               fill='#2510a3', width=5))
                        borrar_linea.append(canvas.create_line(180, 612, c_curr[0], c_curr[1],
                                                               fill='#2510a3', width=5))
                        
                    elif i in ['Thissio', 'Petralona'] and prev in ['Thissio', 'Petralona']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 267, 679,
                                                               fill='#155e29', width=5))
                        borrar_linea.append(canvas.create_line(267, 679, c_curr[0], c_curr[1],
                                                               fill='#155e29', width=5))
                        
                    elif i in ['Piraeus', 'Faliro'] and prev in ['Piraeus', 'Faliro']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 125, 820,
                                                               fill='#155e29', width=5))
                        borrar_linea.append(canvas.create_line(125, 820, c_curr[0], c_curr[1],
                                                               fill='#155e29', width=5))
                        
                    elif i in ['Syntagma', 'Akropoli'] and prev in ['Syntagma', 'Akropoli']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 321, 630,
                                                               fill='#a51b0b', width=5))
                        borrar_linea.append(canvas.create_line(321, 630, c_curr[0], c_curr[1],
                                                               fill='#a51b0b', width=5))
                        
                    elif i in ['Evangelismos', 'Megaro Moussikis'] and prev in ['Evangelismos', 'Megaro Moussikis']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 453, 613,
                                                               fill='#2510a3', width=5))
                        borrar_linea.append(canvas.create_line(453, 613, c_curr[0], c_curr[1],
                                                               fill='#2510a3', width=5))
                        
                    elif i in ['Doukissis Plakentias', 'Pallini'] and prev in ['Doukissis Plakentias', 'Pallini']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 736, 391,
                                                               fill='#2510a3', width=5))
                        borrar_linea.append(canvas.create_line(736, 391, c_curr[0], c_curr[1],
                                                               fill='#2510a3', width=5))
                        
                    elif i in ['Koropi', 'Airport'] and prev in ['Koropi', 'Airport']:
                        borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], 756, 635,
                                                               fill='#2510a3', width=5))
                        borrar_linea.append(canvas.create_line(756, 635, c_curr[0], c_curr[1],
                                                               fill='#2510a3', width=5))
                        
                    # No hay curva en el mapa
                    else:
                        if l_curr == ['1'] or l_prev == ['1'] or (i == 'Omonia' and (prev == 'Monastiraki' or prev == 'Victoria')) or (i == 'Monastiraki' and prev == 'Omonia'):
                            borrar_linea.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#155e29', width=5))
                            
                        elif l_curr == ['2'] or l_prev == ['2'] or (i == 'Syntagma' and (prev == 'Panepistimio' or prev == 'Akropoli')):
                            borrar_linea.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#a51b0b', width=5))
                            
                        elif l_curr == ['3'] or l_prev == ['3'] or (i == 'Syntagma' and (prev == 'Monastiraki' or prev == 'Evangelismos')) or (i == 'Monastiraki' and prev == 'Syntagma'):
                            borrar_linea.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#2510a3', width=5))
                        #borrar_linea.append(canvas.create_line(c_prev[0], c_prev[1], c_prev[0]+1, c_prev[1], fill='ff9100', width=10))
                        
                    prev = i

            # Origen no existe
            elif start not in values:
                print("La estación origen no existe.")

            # Destino no existe
            elif end not in values:
                print("La estación destino no existe.")

            else:
                print("ERROR")

        popup.mainloop()

    # INICIO DE APLICACIÓN
    # Ventana
    master = Tk()
    # Márgenes
    master.config(bd=20)
    master.title("METRO ATENAS")
    
    # Dimensiones de la imagen de fondo (mapa.png)
    master.geometry("400x300")
    master.resizable(True, True)

    # Imagen de la ventana principal
    master.iconbitmap = (r'logo.ico')

    # Imagen del logo del metro de Atenas
    image = Image.open("logo.png")
    # Ajuste del tamaño de la imagen
    logo = image.resize((65, 65))
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


# --------------------------------------------------------------------------------------------------------------------------------
# EJECUCIÓN DEL MAIN (PROGRAMA)
if __name__ == '__main__':
    main()
