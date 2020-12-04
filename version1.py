import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt
import re
import copy
import random

chemeinlist = []
salonlist = []
fournislist = []
roomlist = []  # with contenjan
roomlist1 = []  # without contenjan
coridorlist = []


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
    createSalon(namegenerator('S', len(roomlist1)))
    createFournis(namegenerator('F', num_fourmis))
    print_graph(coridorlist)
    control_root1(coridorlist)
    print(coridorlist)
    # take_root()


class Salon(object):
    name = 'Sv'


class Fournis(object):
    name = 'F'


def namegenerator(name, num):
    namelist = []
    for i in range(num):
        name = f"{name}{i}"
        namelist.append(name)
    return namelist


def createSalon(namelist):
    for i in range(len(namelist)):
        name = Salon()
        setattr(name, 'name', namelist[i])
        salonlist.append(name)


def createFournis(namelist):
    for i in range(len(namelist)):
        name = Fournis()
        setattr(name, 'name', namelist[i])
        fournislist.append(name)


def print_graph(coridorlist):
    g = nx.Graph()
    for coridor in coridorlist:
        g.add_edge(coridor[0], coridor[1])
    nx.draw_networkx(g, with_labels=True, font_size=8,
                     alpha=0.5, node_color="#A86CF3")
    plt.show()


def take_root(exit='Sd'):
    exit = 'Sd'
    chemein = ['Sd']
    for i in range(len(coridorlist)):
        root = count_entre(exit)
        rootfinder(root, chemein)


def count_entre(exit):
    root = []
    for coridor in coridorlist:
        if coridor[1] == exit:
            root.append(coridor)
    return root


def rootfinder(root, chemein):
    for rota in root:
        chemein1 = copy.deepcopy(chemein)
        chemein1.append(rota[0])
        if control_root2(chemein1) == False:
            count_entre(rota[0])
        else:
            take_root(exit=rota[0])


def root_finder(chemein, root):
    for j in range(len(root)):
        chemein1 = copy.deepcopy(chemein)
        rota = root[j]
        chemein1.append(rota[0])
        exit = rota[0]
        if chemein1 in chemeinlist:
            take_root(roomlist, coridorlist, exit)
        if control_root2(chemein1):
            take_root(roomlist, coridorlist, exit)
        k = 0


def take_root1(roomlist, coridorlist, num):
    i = 0
    exit = 'Sd'
    chemein = ['Sd']
    k = 0
    entre = roomlist[num]
    while k < len(roomlist):
        chemein_essayer_list = copy.deepcopy(coridorlist)
        for i in range(len(roomlist)):
            if [entre, exit] in chemein_essayer_list:
                chemein.append(entre)
                exit = entre
                if chemein in chemeinlist:
                    num = num+1
                    take_root(roomlist, coridorlist, num)
                if control_root2(chemein):
                    num = num+1
                    take_root(roomlist, coridorlist, num)
                k = 0
            else:
                entre = roomlist[i]
                k = k + 1


def take_root2(roomlist, coridorlist):
    num1 = len(roomlist)
    rows, cols = num1, num1
    my_matrix = [([0]*cols) for i in range(rows)]
    for coridor in coridorlist:
        my_matrix[roomlist.index(coridor[0])][roomlist.index(coridor[1])] = 1
    for i in my_matrix:
        print(i)


def control_root1(coridorlist):
    if ['Sv', 'Sd'] in coridorlist:
        print('unique solution')
        return True


def control_root2(chemein):
    if ('Sv' in chemein) and ('Sd' in chemein) and (chemein not in chemeinlist):
        chemeinlist.append(chemein)
        print(chemeinlist)
        return True


name = input('name of document is : ')
open_doc_create_list(name)
print(chemeinlist)
