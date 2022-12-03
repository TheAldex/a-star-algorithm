import datetime
import math
import networkx as nx
from tkinter import Button, Canvas, Label, PhotoImage, Tk, Toplevel, messagebox, ttk
from PIL import Image, ImageTk

# --------------------------------------------------------------------------------------------------------------------------------
# DATOS
# Lista estaciones
l1 = ["Piraeus", "Faliro", "Moschato", "Kallithea", "Tavros", "Petralona", "Thissio", "Monastiraki", "Omonia", "Victoria", "Attiki",
      "Aghios Nikolaos", "Kato Patissia", "Aghios Eleftherios", "Ano Patissia", "Perissos", "Pefkakia", "Nea Ionia", "Iraklio", "Irini",
      "Neratziotissa", "Maroussi", "KAT", "Kifissia"]

l2 = ["Aghios Antonios", "Sepolia", "Attiki", "Larissa Station", "Metaxourghio", "Omonia", "Panepistimio", "Syntagma", "Akropoli",
      "Sygrou - Fix", "Neos Kosmos", "Aghios Ioannis", "Dafni", "Aghios Dimitrios"]

l3 = ["Egaleo", "Eleonas", "Kerameikos", "Monastiraki", "Syntagma", "Evangelismos", "Megaro Moussikis", "Ambelokipi", "Panormou",
      "Katehaki", "Ethniki Amyna", "Holargos", "Nomismatokopio", "Aghia Paraskevi", "Halandri", "Doukissis Plakentias", "Pallini",
      "Paiania - Kantza", "Koropi", "Airport"]

transbordos = ["Attiki", "Omonia", "Monastiraki", "Syntagma"]

# Coordenadas de cada estación de la línea 1
coordL1 = [  # verde
    [37.94823850613788, 23.64315408285978],
    [37.9451479545681, 23.66522510003948],
    [37.944314639017264, 23.6780228846546],
    [37.96052252591585, 23.697396473018113],
    [37.962651992557234, 23.703304769309177],
    [37.968797418927856, 23.7092896576727],
    [37.97690381355721, 23.72071682883635],
    [37.98422982753675, 23.727365547670388],  # Monastiraki 107
    [37.98439440622449, 23.728670542327293],  # omonia 108
    [37.99317366581129, 23.730443307163007],
    [37.999510676546244, 23.722893989963133],  # atikki  110
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

# Coordenadas de cada estación de la línea 2
coordL2 = [  # roja
    [38.006838626856, 23.699566830686127],
    [38.00273946681484, 23.71350533028026],
    [37.999510676546244, 23.722893989963133],  # attiki 202
    [37.99209656962052, 23.72108144602919],
    [37.98692004297806, 23.72107721534306],
    [37.98439440622449, 23.728670542327293],  # omonia 205
    [37.98058961718604, 23.7329942269854],
    [37.97466748997125, 23.735179269313868],  # syntagma 207
    [37.96884315445523, 23.7296007],
    [37.964730362866355, 23.726703786507297],
    [37.95725278747033, 23.727116886507297],
    [37.95675237540244, 23.73464052671532],
    [37.94941410696725, 23.737201842328467],
    [37.9407216868299, 23.740651626985407],

]

# Coordenadas de cada estación de la línea 3
coordL3 = [  # azul
    [37.99312672457056, 23.681853444485967],
    [37.98799138458003, 23.692493826371965],
    [37.97879068094447, 23.711468777911087],
    [37.98422982753675, 23.727365547670388],  # monastiraki 303
    [37.97485841331983, 23.73572221287824],  # syntagma 304
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
        'Panepistimio': [['2'], (294, 592)],
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
# ALGORITMO A*
Grafo = nx.Graph()

long1 = len(l1)
long2 = len(l2)
long3 = len(l3)

for i in range(long1):
    Grafo.add_node(l1[i], cor=coordL1[i])  # n-name c-coordenada code
    if (i > 0):
        Grafo.add_edge(l1[i-1], l1[i], cc='verde')  # cc-color

for i in range(long2):
    if l2[i] not in l1:
        Grafo.add_node(l2[i], cor=coordL2[i])
        if (i > 0):
            Grafo.add_edge(l2[i-1], l2[i], cc='rojo')

for i in range(long3):
    if (not (l3[i] in l1 and l3[i] in l2)):
        Grafo.add_node(l3[i], cor=coordL3[i])
        if (i > 0):
            Grafo.add_edge(l3[i-1], l3[i], cc='azul')

# Función que describe el algoritmo A*
def AEstrella(Graph, org, dest):
    visitados = [org]
    novisitados = []
    current = org  # current node being checked
    path = nx.Graph()  # path
    g = {org: 0}  # real distance
    # Euclidean distance
    h = {org: distancia(Graph.nodes[org]['cor'], Graph.nodes[org]['cor'])}
    f = {org: g[org]+h[org]}  # f=g+h
    parents = {}

    while (current != dest):
        # list with all the current node's neighbours
        neighbours = list(Graph.neighbors(current))
        for node in neighbours:
            # if neighbour isn't in visitados or novisitados, add to neighbourlist
            if (not (node in visitados) and not (node in novisitados)):
                # if neighbour isn't in novisitados, add to novisitados
                novisitados.append(node)
                # sets current node as parent of the neighbour
                parents[node] = current

        for i in novisitados:
            parentToCheck = parents[i]  # current node's parent
            parent = parentToCheck

            # list with current node's neighbours
            nn = list(Graph.neighbors(i))

            otherParents = list()  # list with current node's parents
            for j in nn:
                if (j in visitados):  # nodes are parents only if they are in the visitados
                    otherParents.append(j)

            for j in otherParents:
                if (g[j] < g[parentToCheck]):  # choose optimal parent according to its g's
                    parents[current] = j  # sets current's node optimal parent
                    parent = j  # upgrade saved parent of the current node

            coordI = Graph.nodes[i]['cor']  # current node's coordinates
            # current node's parent coordinates
            coordP = Graph.nodes[parent]['cor']
            coordD = Graph.nodes[dest]['cor']  # destination's coordinates

            # transbordos
            # if there's a transfer, we add more cost to g (depending on the transfer's distance)
            if (i in transbordos and parent in transbordos):
                g[i] = distancia(coordI, coordP)
            else:
                g[i] = 0  # otherwise we don't add extra cost

            # G from start to current node
            g[i] += g[parent] + distancia(coordI, coordP)  # add parent's g
            # h is the euclidean distance from current node to destination
            h[i] = distancia(coordI, coordD)
            f[i] = g[i]+h[i]  # f=g+h

        current = novisitados[0]  # change current node
        for i in novisitados:
            if f[i] < f[current]:  # current node is the one
                current = i

        visitados.append(current)  # puts current node on visitados
        novisitados.remove(current)  # removes current node from novisitados

    # designing path
    while (current != org):
        path.add_node(current)  # add current node to path
        current = parents[current]  # go back to its parent
    path.add_node(org)  # add start node

    distance = g[dest]*1000  # trip distance in meters

    weekend = [5, 6]
    date = datetime.date.today()  # current date
    day = datetime.date.isoweekday(date)  # current week day
    
    if (day in weekend):
        # time in minutes; speed=35km/h; mean frequency weekends: 5 minutos
        time = tiempo(g[dest], 68) + (path.number_of_nodes()-1)*5
    else:
        # time in minutes; speed=35km/h; mean frequency week: 3 minutos
        time = tiempo(g[dest], 68) + (path.number_of_nodes()-1)*3
    return path, distance, time

# --------------------------------------------------------------------------------------------------------------------------------
# FUNCIONES GENERALES
# Calcula la distancia eucídea entre 2 pixeles (puntos)
def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

# Función para calcular el tiempo total del camino
def tiempo(km, vel):
    return (km/vel)*60

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
# MAIN
def main():
    # Función a ejecutar al apretar el botón "BUSCAR MEJOR RUTA"
    def onClick():
        # Valores de origen y destino introducidos
        start = origen.get()
        end = destino.get()

        print(AEstrella(Grafo, start, end)[0].nodes())

        reset = []

        # Si no se introduce origen
        if start == '':
            messagebox.showerror(
                'ERROR', 'Error: Debe introducirse una estación de origen')

        # Si no se introduce destino
        elif end == '':
            messagebox.showerror(
                'ERROR', 'Error: Debe introducirse una estación de destino')

        # Se ha introducido origen y destino
        else:
            # Origen no existe
            if start not in values:
                messagebox.showerror(
                    'ERROR', 'Error: La estación de origen introducida no existe')

            # Destino no existe
            elif end not in values:
                messagebox.showerror(
                    'ERROR', 'Error: La estación de destino introducida no existe')

            # Origen y destino existen
            elif start in values and end in values:
                # Popup (nueva ventana) al pulsar el botón
                popup = Toplevel()
                popup.title("MAPA DE RUTA")

                # Dimensiones del popup
                popup.geometry(f'900x908+100+0')
                popup.resizable(True, True)

                # Creamos el lienzo donde dibujar el camino
                canvas = Canvas(popup, width=900, height=986)

                # Imagen del mapa
                bg = PhotoImage(file='images/mapa.png')
                # Establecemos la imagen
                canvas.create_image(450, 454, image=bg)

                dist_text = "LA DISTANCIA A RECORRER ES " + \
                    str(math.ceil(AEstrella(Grafo, start, end)[1])) + " METROS"
                time_text = "EL TIEMPO A EMPLEAR PARA IR DE " + start.upper() + " A " + end.upper() + \
                    " ES " + \
                    str(math.ceil(
                        AEstrella(Grafo, start, end)[2])) + " MINUTOS"

                # Textos de la distancia recorrida y el tiempo empleado en la ruta
                canvas.create_text(450, 30, text=dist_text,
                                   fill="black", font=('Arial 13 bold'))
                canvas.create_text(450, 50, text=time_text,
                                   fill="black", font=('Arial 13 bold'))

                # Empaquetamos el lienzo
                canvas.pack()

                # Borrar lo dibujado en el lienzo
                for e in reset:
                    canvas.delete(e)

                # Borrar los caminos guardados
                reset.clear()

                # Calcular el camino mínimo y convertirlo en una lista
                path = reverse_list(
                    list(AEstrella(Grafo, start, end)[0].nodes()))
                prev = path[0]

                # Dibujar el camino en el lienzo
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
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 433, 260,
                                                        fill='#155e29', width=5))
                        reset.append(canvas.create_line(433, 260, c_curr[0], c_curr[1],
                                                        fill='#155e29', width=5))

                    elif i in ['Victoria', 'Attiki'] and prev in ['Victoria', 'Attiki']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 268, 514,
                                                        fill='#155e29', width=5))
                        reset.append(canvas.create_line(268, 514, c_curr[0], c_curr[1],
                                                        fill='#155e29', width=5))

                    elif i in ['Metaxourghio', 'Omonia'] and prev in ['Metaxourghio', 'Omonia']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 228, 565,
                                                        fill='#a51b0b', width=5))
                        reset.append(canvas.create_line(228, 565, c_curr[0], c_curr[1],
                                                        fill='#a51b0b', width=5))

                    elif i in ['Kerameikos', 'Monastiraki'] and prev in ['Kerameikos', 'Monastiraki']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 180, 612,
                                                        fill='#2510a3', width=5))
                        reset.append(canvas.create_line(180, 612, c_curr[0], c_curr[1],
                                                        fill='#2510a3', width=5))

                    elif i in ['Thissio', 'Petralona'] and prev in ['Thissio', 'Petralona']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 267, 679,
                                                        fill='#155e29', width=5))
                        reset.append(canvas.create_line(267, 679, c_curr[0], c_curr[1],
                                                        fill='#155e29', width=5))

                    elif i in ['Piraeus', 'Faliro'] and prev in ['Piraeus', 'Faliro']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 125, 820,
                                                        fill='#155e29', width=5))
                        reset.append(canvas.create_line(125, 820, c_curr[0], c_curr[1],
                                                        fill='#155e29', width=5))

                    elif i in ['Syntagma', 'Akropoli'] and prev in ['Syntagma', 'Akropoli']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 321, 630,
                                                        fill='#a51b0b', width=5))
                        reset.append(canvas.create_line(321, 630, c_curr[0], c_curr[1],
                                                        fill='#a51b0b', width=5))

                    elif i in ['Evangelismos', 'Megaro Moussikis'] and prev in ['Evangelismos', 'Megaro Moussikis']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 453, 613,
                                                        fill='#2510a3', width=5))
                        reset.append(canvas.create_line(453, 613, c_curr[0], c_curr[1],
                                                        fill='#2510a3', width=5))

                    elif i in ['Doukissis Plakentias', 'Pallini'] and prev in ['Doukissis Plakentias', 'Pallini']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 736, 391,
                                                        fill='#2510a3', width=5))
                        reset.append(canvas.create_line(736, 391, c_curr[0], c_curr[1],
                                                        fill='#2510a3', width=5))

                    elif i in ['Koropi', 'Airport'] and prev in ['Koropi', 'Airport']:
                        reset.append(canvas.create_oval(
                            c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                        reset.append(canvas.create_line(c_prev[0], c_prev[1], 756, 635,
                                                        fill='#2510a3', width=5))
                        reset.append(canvas.create_line(756, 635, c_curr[0], c_curr[1],
                                                        fill='#2510a3', width=5))

                    # No hay curva en el mapa
                    else:
                        if l_curr == ['1'] or l_prev == ['1'] or (i == 'Omonia' and (prev == 'Monastiraki' or prev == 'Victoria')) or (i == 'Monastiraki' and prev == 'Omonia'):
                            reset.append(canvas.create_oval(
                                c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                            reset.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#155e29', width=5))

                        elif l_curr == ['2'] or l_prev == ['2'] or (i == 'Syntagma' and (prev == 'Panepistimio' or prev == 'Akropoli')):
                            reset.append(canvas.create_oval(
                                c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                            reset.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#a51b0b', width=5))

                        elif l_curr == ['3'] or l_prev == ['3'] or (i == 'Syntagma' and (prev == 'Monastiraki' or prev == 'Evangelismos')) or (i == 'Monastiraki' and prev == 'Syntagma'):
                            reset.append(canvas.create_oval(
                                c_prev[0], c_prev[1], c_prev[0], c_prev[1], width=10))
                            reset.append(canvas.create_line(
                                c_prev[0], c_prev[1], c_curr[0], c_curr[1], fill='#2510a3', width=5))
                    reset.append(canvas.create_oval(
                        c_curr[0], c_curr[1], c_curr[0], c_curr[1], width=10))

                    prev = i

                popup.mainloop()

            else:
                messagebox.showerror('¡Lo sentimos! Ha ocurrido un error')

    # Función a ejecutar al apretar el botón "MOSTRAR MAPA"
    def showMap():
        # Popup (nueva ventana) al pulsar el botón
        map = Toplevel()
        map.title("MAPA DE METRO")

        # Abrimos la imagen y la empaquetamos
        map_image = ImageTk.PhotoImage(Image.open('images/mapa.png'))
        Label(map, image=map_image).pack()

        map.mainloop()

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
    master.iconbitmap = (r'images/logo.ico')

    # Imagen del logo del metro de Atenas
    image = Image.open('images/logo.png')
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

    # Texto de origen
    selO = Label(master, text="Seleccione estación de origen",
                 font=('calibri', 13))
    selO.pack()

    # Input de origen
    origen = ttk.Combobox(master, value=values)
    origen.current(0)
    origen.bind("<<ComboboxSelected>>")
    origen.pack()

    # Texto destino
    selD = Label(master, text="Seleccione estación de destino",
                 font=('calibri', 13))
    selD.pack()

    # Input destino
    destino = ttk.Combobox(master, value=values)
    destino.current(0)
    destino.bind("<<ComboboxSelected>>")
    destino.pack()

    # Separador
    salto = Label(master, text="")
    salto.pack()

    # Función para cambiar el estado del botón
    def on_enter(e):
        alg_button["bg"] = "gray"

    # Función para cambiar el estado del botón
    def on_leave(e):
        alg_button["bg"] = "SystemButtonFace"

    # Botón para calcular el camino
    alg_button = Button(master, text="BUSCAR MEJOR RUTA",
                        font=('calibri', 10, 'bold'), cursor="hand", command=onClick)

    # Acciones al pasar el cursor para el botón "BUSCAR MEJOR RUTA"
    alg_button.bind("<Enter>", on_enter)
    alg_button.bind("<Leave>", on_leave)

    # Función para cambiar el estado del botón
    def on_enter(e):
        show_button["bg"] = "gray"

    # Función para cambiar el estado del botón
    def on_leave(e):
        show_button["bg"] = "SystemButtonFace"

    # Botón para mostrar el mapa vacío
    show_button = Button(master, text="MOSTRAR MAPA",
                         font=('calibri', 10, 'bold'), cursor="hand", command=showMap)

    # Acciones al pasar el cursor para el botón "MOSTRAR MAPA"
    show_button.bind("<Enter>", on_enter)
    show_button.bind("<Leave>", on_leave)

    # Empaquetamos los botones
    alg_button.pack()
    show_button.pack()

    master.mainloop()


# --------------------------------------------------------------------------------------------------------------------------------
# EJECUCIÓN DEL MAIN (PROGRAMA)
if __name__ == '__main__':
    main()
