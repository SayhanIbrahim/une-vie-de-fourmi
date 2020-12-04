import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
import re
import numpy as np


salonlist = []  # tous les salon objects dans cette list
fournislist = []  # tous les fournis objects dans cette list
roomlist = []  # with capacity
roomlist1 = []  # without capacity
coridorlist = []  # pour tous les coridors
DicoEtapes = {}  # Pour Aloys


def open_doc_create_list(name):
    if name is '':
        name = 'fourmiliere_cinq'
    fichier = open(f'{name}.txt', 'r')
    for line in fichier:
        result = re.search('=', line)
        result1 = re.search('-', line)
        result2 = re.search('^S', line)
        result3 = re.search('{', line)
        if result:
            x = line.split("=")
            num_fourmis = int(x[1].split()[0])
        if result2 and not result1:
            if result3:
                roomlist1.append(line.split()[0])
                roomlist.append([line.split()[0], int(
                    line.split("{")[1].split("}")[0])])
            else:
                x = line.split()
                room_num = [x[0], 1]
                roomlist1.append(line.split()[0])
                roomlist.append(room_num)
        if result1:
            x = line.split(" - ")
            y = x[1].split()
            x.pop()
            x.append(y[0])
            coridorlist.append(x)
    roomlist1.append('Sd')
    roomlist1.insert(0, 'Sv')
    roomlist.append(['Sd', num_fourmis])
    roomlist.insert(0, ['Sv', num_fourmis])
    fichier.close()
    create_salon(roomlist)
    create_fournis(name_generator(num_fourmis))
    # print_graph(coridorlist)
    data_cleaner()
    capacity_correction()
    all_etaps(name, num_fourmis)
    AfficherFourmiliere()


class Salon(object):
    name = 'Sv'


class Fournis(object):
    name = 'F'


def name_generator(num):
    namelist = []
    for i in range(num):
        i = i+1
        namelist.append(f"f{i}")
    return namelist


def create_salon(roomlist):
    for room in roomlist:
        name = Salon()
        nom = room[0]
        capacity = room[1]
        setattr(name, 'name', nom)
        setattr(name, 'entree', [])
        setattr(name, 'sortie', [])
        setattr(name, 'salle', [])
        setattr(name, 'capacity', capacity)
        salonlist.append(name)


def create_fournis(namelist):
    for i in range(len(namelist)):
        name = Fournis()
        setattr(name, 'name', namelist[i])
        setattr(name, 'position', 'Sv')
        fournislist.append(name)
        salonlist[0].salle.append(namelist[i])


def register_entre_sorti():
    for coridor in coridorlist:
        index1 = roomlist1.index(coridor[0])
        index2 = roomlist1.index(coridor[1])
        salonlist[index1].sortie.append(coridor[1])
        salonlist[index2].entree.append(coridor[1])


def capacity_correction():
    salonlist1 = list(reversed(salonlist))
    for i in salonlist1:
        if i.name != 'Sd' and i.name != 'Sv':
            sortie = i.sortie
            total = 0
            for room in sortie:
                total = total+salonlist[roomlist1.index(room)].capacity
            if i.capacity > total:
                setattr(i, 'capacity', total)


def all_etaps(name, num_fourmis):
    ths = open(f"{name} solution.txt", "a")
    cerate_dict(0)
    count = 1
    while len(salonlist[-1].salle) < num_fourmis:
        line1 = f"+++ E{count} +++"
        ths.write(str(line1)+"\n")
        print(3*'+', f'E{count}', 3*'+')
        for i in fournislist:
            position = i.position
            nextposition = salonlist[roomlist1.index(position)].sortie
            boelean = True
            k = 0
            while boelean == True and k < len(nextposition):
                room = nextposition[k]
                if len(salonlist[roomlist1.index(room)].salle) < salonlist[roomlist1.index(room)].capacity:
                    setattr(i, 'position',
                            salonlist[roomlist1.index(room)].name)
                    salonlist[roomlist1.index(room)].salle.append(i.name)
                    salonlist[roomlist1.index(position)].salle.remove(i.name)
                    boelean = False
                    line = f"{i.name} - {position} - {i.position}"
                    print(str(line))
                    ths.write(str(line)+"\n")
                else:
                    boelean = True
                    k += 1
        cerate_dict(count)
        count = count+1
    ths.close()


def cerate_dict(count):
    name1 = f'etape{count}'
    name = {}
    for room in salonlist:
        name[str(room.name)] = len(room.salle)
    DicoEtapes[name1] = name


# def print_graph(coridorlist):
#     g = nx.Graph()
#     for coridor in coridorlist:
#         g.add_edge(coridor[0], coridor[1])
#     nx.draw_networkx(g, with_labels=True, font_size=8,
#                      alpha=0.5, node_color="#A86CF3")
#     plt.show()


def control_root1():
    global coridorlist
    if (['Sd', 'Sv'] or ['Sv', 'Sd']) in coridorlist:
        coridorlist = [['Sv', 'Sd']]
        return coridorlist
    return coridorlist


def data_cleaner():
    coridorlist = control_root1()
    len1 = len(coridorlist)
    datacounterdict = data_counter_list(data_cleaner_list())
    data_verify(datacounterdict)
    len2 = len(coridorlist)
    if len1 == len2:
        register_entre_sorti()
    else:
        data_cleaner()


def data_cleaner_list():
    datacleanerlist = []
    for i in coridorlist:
        datacleanerlist.extend(i)
    return datacleanerlist


def data_counter_list(datacleanerlist):
    datacounterdict = {}
    for room in roomlist:
        datacounterdict[room[0]] = datacleanerlist.count(room[0])
    return datacounterdict


def data_verify(datacounterdict):
    for i in datacounterdict:
        if int(datacounterdict[i]) == 1 and not (i == 'Sv' or i == 'Sd'):
            datacleaer(i)
        else:
            continue


def datacleaer(i):
    for coridor in coridorlist:
        if coridor[1] == i:
            coridorlist.remove(coridor)


def AfficherFourmiliere():
    global DicoEtapes
    G = nx.Graph()
    G.add_nodes_from(roomlist1)
    G.add_edges_from(coridorlist)
    nodePos = nx.spring_layout(G)
    Dicodeplacementfourmis = {}
    i = 0
    while i < len(DicoEtapes):
        Dico = DicoEtapes.get("etape"+str(i+1))
        if i == 0:
            listekeys = list(Dico.keys())
            listevalues = list(Dico.values())
            liste = []
            for j in range(len(listevalues)):
                if listevalues[j] != 0 and listekeys[j] != 'Sv':
                    liste.append(('Sv', listekeys[j]))
                    Dicodeplacementfourmis.update({"etape"+str(i+1): liste})
        if i != 0:
            listekeys = list(Dico.keys())
            listevalues = list(Dico.values())
            listevaluesi_1 = list(DicoEtapes.get("etape"+str(i)).values())
            liste = []
            for j in range(len(listevalues)):
                if listevalues[j] >= listevaluesi_1[j] and listevalues[j] != 0 and listekeys[j] != 'Sv' and listekeys[j] != 'Sd':
                    liste.append((listekeys[j-1], listekeys[j]))
                elif listevalues[j] > listevaluesi_1[j] and listevalues[j] != 0 and listekeys[j] == 'Sd':
                    liste.append((listekeys[j-1], listekeys[j]))
                Dicodeplacementfourmis.update({"etape"+str(i+1): liste})
        i = i+1

    nligne = 0
    ncolonne = 3
    if len(DicoEtapes)//3 == 0:
        nligne = 1
    elif len(DicoEtapes) % 3 == 0:
        nligne = len(DicoEtapes)//3
    else:
        nligne = (len(DicoEtapes)//3+1)
    fig, ax = plt.subplots(nligne, ncolonne, num=1)
    indexes = []
    for etape in range(len(DicoEtapes)):
        DicoSalles = list(DicoEtapes.values())[etape]
        ix = np.unravel_index(etape, ax.shape)
        indexes.append(ix)
        nx.draw(G, nodePos, with_labels=True, font_size=8,
                alpha=0.8, node_color="#A86CF3", ax=ax[ix])
        # extent = ax[etape].get_window_extent().transformed(
        #     fig.dpi_scale_trans.inverted())
        # fig.savefig(f'{name} etape {etape}.png', bbox_inches=extent)
        for sommet, nombrefourmis in DicoSalles.items():
            ax[ix].annotate(nombrefourmis, xy=nodePos.get(sommet), xytext=(0, 20), textcoords='offset points',
                            bbox=dict(boxstyle="round", fc="cyan"))
    (x, y) = ix

    if y < ncolonne-1:
        for k in [y+1, len(indexes[0])]:
            ax[x, k].set_visible(False)

    plt.show()


name = input('name of document is : ')
open_doc_create_list(name)
