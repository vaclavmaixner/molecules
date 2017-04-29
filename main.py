import random
import math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#strukturyhumans
import molecule as molecule_import
#import graphics as graphics_import
import plot as myplt

NO_MOLECULES = 10
HEIGHT = 10
WIDTH = 10
ITERATIONS = 2
WAIT_TIME = 0.000001

delta_time = 0

list_of_molecules = []
direction_count_list = []

#vyrobi nahodne molekuly a nacpe je do

def setup_molecules(no_molecules):
    for k in range(0, NO_MOLECULES):
        pos_x = random.randint(0, HEIGHT)
        pos_y = random.randint(0, WIDTH)
        molecule = molecule_import.Molecule(k, pos_x, pos_y)
        list_of_molecules.append(molecule)

def setup_test_molecules():
    molecule1 = molecule_import.Molecule(1, 0, 0)
    molecule2 = molecule_import.Molecule(2, 0, 0)
    molecule3 = molecule_import.Molecule(3, HEIGHT, WIDTH)
    list_of_molecules.append(molecule1)
    list_of_molecules.append(molecule2)
    list_of_molecules.append(molecule3)


#vybere index molekuly nahodne ze seznamu vsech molekul
def choose_molecule():
    k = random.randint(0, len(list_of_molecules))
    print("Chosen molecule is of index:", k)
    return k

def countOverlap(difference_x, difference_y):
    #prechod od pocitani v poli do pocitani v kartezske soustave souradnic
    dy = difference_x
    dx = difference_y
    #print("we got in countoverlap",difference_x,"and ", dy)
    overlap = 0

    if (dx == 1 or dx == -1):
        if (dy == 2):
            overlap = 1
        elif (dy == 1):
            overlap = 2
        elif (dy == 0):
            overlap = 3
        elif (dy == -1):
            overlap = 2
        elif (dy == -2):
            overlap = 1
    elif (dx == 0):
        if (dy == 2):
            overlap = 2
        elif (dy == 1):
            overlap = 4
        elif (dy == 0):
            overlap = 6
        elif (dy == -1):
            overlap = 4
        elif (dy == -2):
            overlap = 2
    return overlap

def checkNeighbours(index_of_chosen_mol, x, y):
    sum_of_overlap = 0
    for index in range(0,len(list_of_molecules)):
        # difference_x=0
        # difference_y=0
        if (index != index_of_chosen_mol):
            potential_neighbour = list_of_molecules[index]
            difference_x = x - potential_neighbour.pos_x
            difference_y = y - potential_neighbour.pos_y
            #print(difference_x, "mezera", difference_y)

            # diff_x=-1 znamena, ze sousedici molekula sedi
            # nad nami vysetrovanou molekulou, y=-1 je napravo

            sum_of_overlap += countOverlap(difference_x,difference_y)
    return sum_of_overlap

def virtualMove(index_of_chosen_mol, direction):
    chosen_mol = list_of_molecules[index_of_chosen_mol]
    moved_mol = molecule_import.Molecule(1, 0, 0)
    #print(moved_mol.pos_x, moved_mol.pos_y)

    if direction==1:
        moved_mol.pos_x = chosen_mol.pos_x
        moved_mol.pos_y = chosen_mol.pos_y + 1
    elif direction==2:
        moved_mol.pos_x = chosen_mol.pos_x + 1
        moved_mol.pos_y = chosen_mol.pos_y
    elif direction==3:
        moved_mol.pos_x = chosen_mol.pos_x
        moved_mol.pos_y = chosen_mol.pos_y - 1
    elif direction==4:
        moved_mol.pos_x = chosen_mol.pos_x - 1
        moved_mol.pos_y = chosen_mol.pos_y
    #print("moved molecule", moved_mol.pos_x, " a y ", moved_mol.pos_y)

    chance = checkNeighbours(index_of_chosen_mol, moved_mol.pos_x, moved_mol.pos_y)
    move_chance = molecule_import.Movement_chance(direction,chance)
    #print("kontrola move_chance ma hodnotu ", move_chance.dir, " a sance je", move_chance.prob)
    return move_chance

def convertOverlapToProbability(overlapAfterMove, overlapInitial):
    BOLTZMANN = 8.617e-5 #prepsat do eV
    TEMPERATURE = 300
    ENERGY_EQ = 1

    # print(overlapAfterMove, "and the initial overlap is ", overlapInitial)
    delta_energy = overlapInitial - overlapAfterMove
    energy_act = ENERGY_EQ + delta_energy/2 + (delta_energy*delta_energy)/(16*ENERGY_EQ)
    probability = math.exp((energy_act)/(BOLTZMANN*TEMPERATURE))

    return probability


def moveChance(index_of_chosen_mol):
    chance_sum = 0

    #purge the previous direction count list
    #for i in range(0,len(direction_count_list)):
    #    del direction_count_list[i]


    #print("the chosen molecule is of index", index_of_chosen_mol)
    for direction in range(1,5):
        move_chance = virtualMove(index_of_chosen_mol, direction)
        #print("And the chance isssssssss: ", checkNeighbours(index_of_chosen_mol,0,0))
        convertedProbability = convertOverlapToProbability(move_chance.prob, checkNeighbours(index_of_chosen_mol,list_of_molecules[index_of_chosen_mol].pos_x,list_of_molecules[index_of_chosen_mol].pos_y))
        move_chance.prob = convertedProbability

        chance_sum += convertedProbability
        #print ("the chance to move for direction",move_chance.dir,"is ", move_chance.prob)

        current_dir_move = molecule_import.Direction_movement(index_of_chosen_mol, move_chance.dir, move_chance.prob)
        direction_count_list.append(current_dir_move)

    # print("the total probability is ", chance_sum)

def moveChanceForAll():
    for i in range(0,len(list_of_molecules)):
        moveChance(i)


def printDirectionCountList():
    for i in range(0,len(direction_count_list)):
        print("The index is " + str(direction_count_list[i].index) + ", the direction is ", end="")
        print(str(direction_count_list[i].dir) + ", the chance is " + str(direction_count_list[i].prob))

def graphics(iterations):
    # fig = plt.figure()
    plt.clf()
    OFFSET = 1

    plt.ion()
    plt.axis([0 - OFFSET, WIDTH + OFFSET, 0 - OFFSET - 1, HEIGHT + OFFSET - 1])

    currentAxis = plt.gca()


    # ax = fig.add_subplot(111)

    for index in range(0,len(list_of_molecules)):
        x = list_of_molecules[index].pos_x
        y = list_of_molecules[index].pos_y

        #jmeno molekuly v jejim prostredku
        #currentAxis.annotate(str(index), xy=(4, 0), xytext=(x + 1.5, y-1.1))
        currentAxis.annotate(str(index), xy=(4, 0), xytext=(x+0.4, y-0.6))

        #pro cyklicke okrajove podminky zavedeme modulo souradnice pro kazdy element bunky ve stylu:
        # 1 2 3
        # 4 5 6
        x1 = x % WIDTH
        y1 = y % HEIGHT
        x2 = (x + 1) % WIDTH
        y2 = y % HEIGHT
        x3 = (x + 2) % WIDTH
        y3 = y % HEIGHT

        x4 = x % WIDTH
        y4 = (y-1) % HEIGHT
        x5 = (x + 1) % WIDTH
        y5 = (y-1) % HEIGHT
        x6 = (x + 2) % WIDTH
        y6 = (y-1) % HEIGHT

        currentAxis.add_patch(Rectangle((x1, y1), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))
        currentAxis.add_patch(Rectangle((x2, y2), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))
        currentAxis.add_patch(Rectangle((x3, y3), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))
        currentAxis.add_patch(Rectangle((x4, y4), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))
        currentAxis.add_patch(Rectangle((x5, y5), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))
        currentAxis.add_patch(Rectangle((x6, y6), 1, -1, alpha=0.4, facecolor="red",edgecolor="black"))

        plt.plot([0, 0], [-1, HEIGHT-1], color='k', linestyle='-', linewidth=0.5)
        plt.plot([0, WIDTH], [-1, -1], color='k', linestyle='-', linewidth=0.5)
        plt.plot([WIDTH, WIDTH], [-1, HEIGHT-1], color='k', linestyle='-', linewidth=0.5)
        plt.plot([0, WIDTH], [HEIGHT-1, HEIGHT-1], color='k', linestyle='-', linewidth=0.5)

    plt.show()

    # print(delta_time)

    if iterations == ITERATIONS:
        plt.pause(4)
    else: plt.pause(WAIT_TIME)



def pseudoGraphics():
    surface = [["0" for i in range(HEIGHT+1)] for j in range(WIDTH+1)]

    for k in range(0,len(list_of_molecules)):
        surface[list_of_molecules[k].pos_x][list_of_molecules[k].pos_y] = "X"

    for i in range(0,HEIGHT+1):
        for j in range(0,WIDTH+1):
            print(surface[i][j]," ", end="")
        print(" ")

def check_cyclic_boundary_conditions():
    for i in range(0,len(list_of_molecules)):
        print("Before", list_of_molecules[i].pos_x, " and ", list_of_molecules[i].pos_y)
        list_of_molecules[i].pos_x = (list_of_molecules[i].pos_x) % WIDTH
        list_of_molecules[i].pos_y = (list_of_molecules[i].pos_y) % HEIGHT
        print("After", list_of_molecules[i].pos_x, " and ", list_of_molecules[i].pos_y)

def add_deposition_chance():
    deposition = molecule_import.Direction_movement((len(direction_count_list)*4 + 1), 0, 0.01)
    direction_count_list.append(deposition)

def makeOneChange():
    sumOfAllMoves = 0
    indexFinder = 0
    indexOfchosenEvent = 0

 #   add_deposition_chance()


    #secte vsechny cestnosti dohromady
    for i in range(0,len(direction_count_list)):
        sumOfAllMoves += direction_count_list[i].prob
    print(sumOfAllMoves)

    a = random.uniform(0.0, 1.0)
    # promenlivy cas, nastaveny tak, ze pro vysoce pravdebopodobnou udalost se to stane rychle a naopak
    delta_time = ((-1)*math.log(a)/sumOfAllMoves)

    #vybere dany ukazatel na cetnosti, ktery urci, jak udalost se uskutecni
    chosenCount = random.uniform(0.0, sumOfAllMoves)

    #prochazi vsechny udalosti s jejich cetnostmi a vybere tu, ktera sedi s ukazatelem
    for i in range(0,len(direction_count_list)):
        indexFinder += direction_count_list[i].prob
        #print("jaa",indexFinder, " ", chosenCount)
        if indexFinder >= chosenCount:
            indexOfchosenEvent = i
            break

    #actually move
    if direction_count_list[indexOfchosenEvent].dir == 1:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_y += 1
    elif direction_count_list[indexOfchosenEvent].dir == 2:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_x += 1
    elif direction_count_list[indexOfchosenEvent].dir == 3:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_y -= 1
    elif direction_count_list[indexOfchosenEvent].dir == 4:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_x -= 1

    check_cyclic_boundary_conditions()

    print(direction_count_list[indexOfchosenEvent].index, "and the direction is ", direction_count_list[indexOfchosenEvent].dir)
    return indexOfchosenEvent

def print_molecule_list():
    for l in range(0,len(list_of_molecules)):
        print('The positions of molecules are: ',str(list_of_molecules[l].pos_x) + " " + str(list_of_molecules[l].pos_y))

def Main():
    setup_molecules(NO_MOLECULES)



    #choose_molecule()
    #moveChanceForAll()
    #graphics()
    #pseudoGraphics()

    #print(makeOneChange(), " is the chosen index of event to be done")

    #printDirectionCountList()

    #convertOverlapToProbability(1)

    print("TEEEST ", checkNeighbours(2, 7, 7))


    #the main loop
    for i in range (0,ITERATIONS):
        moveChanceForAll()
        # pseudoGraphics()
        graphics(i)
        #graphics_import.graphics_main(list_of_molecules)
        #printDirectionCountList()
        print_molecule_list()
        makeOneChange()

        print("another run_________________________")
        del direction_count_list[:]
    plt.show(block=True)

#run the setup
Main()




#udalost se vybira tak, ze ze vsech molekul a ze vsech jejich pohybu se vybere jeden pohyb u jedny molekuly,
#test - udelat misto repulze pritazlivou silu
#pozdeji udelat prepocitavani pozic jenom lokalne, aby se usetril cas

#difuzivita 0,6, 300 Kelvin, 10e13 1/s prefaktor divny gamma

#plus depozice s konstanti psti
#urcit hranice, udela cyklicky
#vypocitat si tabulku prekryvu na pravdepodobnost
#nastavit si difuzivitu
