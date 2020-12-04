import glob
import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
import re
import copy
import numpy as np
from PIL import Image


chemeinlist = []
salonlist = []
fournislist = []
roomlist = []  # with capacity
roomlist1 = []  # without capacity
coridorlist = []
DicoEtapes = {}


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
    data_cleaner()
    capacity_correction()
    all_etaps(name, num_fourmis)
    crete_gif(name)


class Salon(object):
    name = 'Sv'
    sortie = []
    entree = []
    salle = []


class Fournis(object):
    name = 'F'


def name_generator(num):
    namelist = []
    for i in range(num):
        i = i+1
        name = f"f{i}"
        namelist.append(name)
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
    cerate_dict(count=0)
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
    AfficherFourmiliere(name)


def cerate_dict(count):
    name1 = f'etape{count}'
    name = {}
    for room in salonlist:
        name[str(room.name)] = len(room.salle)
    DicoEtapes[name1] = name


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


def AfficherFourmiliere(name):
    global DicoEtapes
    lignesfichier = open(f'{name}.txt').read().split()
    Sommets = []
    Arretes = []
    nombrefourmis = 0

    for i in range(len(lignesfichier)):
        if lignesfichier[i][0] == 'f' or lignesfichier[i][0] == 'F':
            nombrefourmis = lignesfichier[i][2:]
        if lignesfichier[i][0] == 'S' and lignesfichier[i] not in Sommets:
            Sommets.append(lignesfichier[i])
        if lignesfichier[i] == '-':
            arrete = (lignesfichier[i-1], lignesfichier[i+1])
            if arrete not in Arretes:
                Arretes.append(arrete)

    G = nx.Graph()
    G.add_nodes_from(Sommets)
    G.add_edges_from(Arretes)
    nodePos = nx.spring_layout(G)
    fig = plt.gca()
    titres = ['étape '+str(i+1) for i in range(0, len(DicoEtapes))]
    cnt = 0
    for etape in range(len(DicoEtapes)):
        DicoSalles = list(DicoEtapes.values())[etape]
        nx.draw(G, nodePos, with_labels=True, font_size=8,
                alpha=0.8, node_color="#A86CF3")
        liste = []
        fig.set_title(titres[etape], fontsize=10)
        for sommet, nombrefourmis in DicoSalles.items():
            if nombrefourmis == 0:
                couleur = 'cyan'
            else:
                couleur = 'red'
            ann = plt.annotate(nombrefourmis, xy=nodePos.get(sommet), xytext=(
                0, 20), textcoords='offset points', bbox=dict(boxstyle="round", fc=couleur))
            liste.append(ann)
        plt.savefig(f"{name} étape_{cnt}.png", format="PNG")
        plt.pause(2)
        for a in liste:
            if cnt != len(DicoEtapes)-1:
                a.remove()
        cnt = cnt+1
    plt.show()


def crete_gif(name):
    frames = []
    imgs = glob.glob("*.png")
    list.sort(imgs, key=lambda x: int(x.split('_')[2].split('.png')[0]))
    for i in imgs:
        newframe = Image.open(i)
        frames.append(newframe)
    # Sort the images by #, this may need to be tweaked for your use case
    frames[0].save(f'{name}.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=500, loop=0)


name = input('name of document is : ')
open_doc_create_list(name)
