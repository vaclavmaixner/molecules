import random
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#struktury
import molecule as molecule_import
import plot as myplt

NO_MOLECULES = 2
HEIGHT = 3
WIDTH = 3
list_of_molecules = []
direction_count_list = []

#vyrobi nahodne molekuly a nacpe je do

def setup_molecules(no_molecules):
    for k in range(0, no_molecules):
        pos_x = random.randint(0, HEIGHT)
        pos_y = random.randint(0, WIDTH)
        molecule = molecule_import.Molecule(k, pos_x, pos_y)
        list_of_molecules.append(molecule)


#vybere index molekuly nahodne ze seznamu vsech molekul
def choose_molecule():
    k = random.randint(0, len(list_of_molecules))
    print("Chosen molecule is of index:", k)
    return k

def countOverlap(difference_x, difference_y):
    dx = difference_x
    dy = difference_y
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
        difference_x=0
        difference_y=0
        if (index != index_of_chosen_mol):
            potential_neighbour = list_of_molecules[index]
            difference_x = x - potential_neighbour.pos_x
            difference_y = y - potential_neighbour.pos_y
            #print(difference_x, "mezera", difference_y)
            sum_of_overlap += countOverlap(difference_x,difference_y)
    return sum_of_overlap

def virtualMove(index_of_chosen_mol, direction):
    chosen_mol = list_of_molecules[index_of_chosen_mol]
    moved_mol = molecule_import.Molecule(1, 0, 0)
    #print(moved_mol.pos_x, moved_mol.pos_y)

    if direction==1:
        moved_mol.pos_x = chosen_mol.pos_x - 1
        moved_mol.pos_y = chosen_mol.pos_y
    elif direction==2:
        moved_mol.pos_x = chosen_mol.pos_x
        moved_mol.pos_y = chosen_mol.pos_y + 1
    elif direction==3:
        moved_mol.pos_x = chosen_mol.pos_x + 1
        moved_mol.pos_y = chosen_mol.pos_y
    elif direction==4:
        moved_mol.pos_x = chosen_mol.pos_x
        moved_mol.pos_y = chosen_mol.pos_y - 1
    #print("moved molecule", moved_mol.pos_x, " a y ", moved_mol.pos_y)

    chance = checkNeighbours(index_of_chosen_mol, moved_mol.pos_x, moved_mol.pos_y)
    move_chance = molecule_import.Movement_chance(direction,chance)
    #print("kontrola move_chance ma hodnotu ", move_chance.dir, " a sance je", move_chance.prob)
    return move_chance


def moveChance(index_of_chosen_mol):
    chance_sum = 0
    #print("the chosen molecule is of index", index_of_chosen_mol)
    for direction in range(1,5):
        move_chance = virtualMove(index_of_chosen_mol, direction)
        chance_sum += move_chance.prob
        #print ("the chance to move for direction",move_chance.dir,"is ", move_chance.prob)

        current_dir_move = molecule_import.Direction_movement(index_of_chosen_mol, move_chance.dir, move_chance.prob)
        direction_count_list.append(current_dir_move)

    print("the total probability is ", chance_sum)

def printDirectionCountList():
    for i in range(0,len(direction_count_list)):
        print("The index is " + str(direction_count_list[i].index) + ", the direction is ", end="")
        print(str(direction_count_list[i].dir) + ", the chance is " + str(direction_count_list[i].prob))


def graphics():
    OFFSET = 3

    plt.ion()
    fig = plt.figure()
    plt.axis([0-OFFSET, HEIGHT+OFFSET, 0-OFFSET, WIDTH+OFFSET])
    currentAxis = plt.gca()

    for index in range(0,len(list_of_molecules)):
        x = list_of_molecules[index].pos_x
        y = list_of_molecules[index].pos_y
        currentAxis.add_patch(Rectangle((x, y), -1, -1, alpha=0.4, facecolor="red"))

        plt.show()
        plt.pause(0.0001)
    plt.show(block=True)

def pseudoGraphics():
    surface = [["0" for i in range(HEIGHT+1)] for j in range(WIDTH+1)]

    for k in range(0,len(list_of_molecules)):
        surface[list_of_molecules[k].pos_x][list_of_molecules[k].pos_y] = "X"

    for i in range(0,HEIGHT+1):
        for j in range(0,WIDTH+1):
            print(surface[i][j]," ", end="")
        print(" ")

def moveChanceForAll():
    for i in range(0,len(list_of_molecules)):
        moveChance(i)

def makeOneChange():
    sumOfAllMoves = 0
    indexFinder = 0
    indexOfchosenEvent = 0

    for i in range(0,len(direction_count_list)):
        sumOfAllMoves += direction_count_list[i].prob

    chosenCount = random.randint(0, sumOfAllMoves)

    for i in range(0,len(direction_count_list)):
        indexFinder += direction_count_list[i].prob
        print("jaa",indexFinder, " ", chosenCount)
        if indexFinder >= chosenCount:
            indexOfchosenEvent = i
            break

    #actually move
    if direction_count_list[indexOfchosenEvent].dir == 1:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_x -= 1
    elif direction_count_list[indexOfchosenEvent].dir == 2:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_y += 1
    elif direction_count_list[indexOfchosenEvent].dir == 3:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_x += 1
    elif direction_count_list[indexOfchosenEvent].dir == 4:
        list_of_molecules[direction_count_list[indexOfchosenEvent].index].pos_y -= 1

    return indexOfchosenEvent



def Main():
    setup_molecules(2)

    for l in range(0,len(list_of_molecules)):
        print(str(list_of_molecules[l].pos_x) + " " + str(list_of_molecules[l].pos_y))

    #choose_molecule()
    moveChanceForAll()
    #graphics()
    pseudoGraphics()

    print(makeOneChange(), " is the chosen index of event to be done")

    printDirectionCountList()

#run the setup
Main()
