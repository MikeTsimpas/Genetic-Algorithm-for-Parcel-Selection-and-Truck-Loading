import numpy as np
import random as rd
from random import randint

# Start of exercise
#_______________________________________________________________________________________________________________________________________________
np.random.seed(0)
rd.seed(0)

def cal_fitness(paketa, fortigo, population):
    fitness = np.empty(population.shape[0])
    truck_loads_list = []
    for i in range(population.shape[0]):
        sinoliki_aksia = 0
        # Δημιουργούμε την truck_loads και θα την εμφανίσουμε και αργότερα
        truck_loads = [{'Length': fortigo[truck_index]['Lenght'], 'Width': fortigo[truck_index]['Width'],'Height': fortigo[truck_index]['Height'], 'Maximum_Weight': fortigo[truck_index]['Maximum_Weight'], 'Current_Weight': 0, 'Parcels': []} for truck_index in range(len(fortigo))]
        valid_solution = True
        for j in range(population.shape[1]):
            if population[i, j] == 1:
                parcel_added = False
                for truck_index, truck in enumerate(truck_loads):
                    if (truck['Current_Weight'] + paketa[j]['Weight'] <= fortigo[truck_index]['Maximum_Weight'] and
                        truck['Length'] >= paketa[j]['Lenght'] and
                        truck['Height'] >= paketa[j]['Height'] and
                        truck['Width'] >= paketa[j]['Width']):
                        truck['Current_Weight'] += paketa[j]['Weight']
                        truck['Parcels'].append(j + 1)
                        sinoliki_aksia += paketa[j]['Price']
                        parcel_added = True
                        break
                if not parcel_added:
                    valid_solution = False
                    break
        if not valid_solution:
            sinoliki_aksia = 0
        fitness[i] = sinoliki_aksia
        truck_loads_list.append(truck_loads)
    return fitness.astype(int), truck_loads_list
#________________________________________________________________________________________________________________

def selection(fitness, num_parents, population):
    fitness = list(fitness)
    parents = np.empty((num_parents, population.shape[1]))
    for i in range(num_parents):
        max_fitness = np.where(fitness == np. max(fitness))
        parents[i, :] = population[max_fitness[0][0], :]
        fitness[max_fitness[0][0]] = -999999
    return parents
#________________________________________________________________________________________________________________

def crossover(parents, number_of_offsprings):
    offsprings = np.empty((number_of_offsprings, parents.shape[1]))
    crossover_point = int(parents.shape[1] / 2)
    crossover_rate = 0.8                                                            
    i = 0
    while i < number_of_offsprings:
        parent1_index = i % parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]
        x = rd.random()
        if x <= crossover_rate:
            offsprings[i, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
            offsprings[i, crossover_point:] = parents[parent2_index, crossover_point:]
        else:
            offsprings[i, :] = parents[parent1_index, :]
        i += 1
    return offsprings
#________________________________________________________________________________________________________________

def mutation(offsprings):
    mutants = np.empty((offsprings.shape))
    mutation_rate = 0.4
    for i in range(offsprings.shape[0]):
        random_timi = rd.random()
        mutants[i, :] = offsprings[i, :]
        if random_timi < mutation_rate:
            int_random_timi = randint(0, offsprings.shape[1] - 1)
            mutants[i, int_random_timi] = 1 - mutants[i, int_random_timi]                                                   
    return mutants
#________________________________________________________________________________________________________________

def optimize(paketa, fortigo_info, population_size=10, generations=50):
    plithos_paketon = len(paketa)
    population = np.random.randint(2, size=(population_size, plithos_paketon))

    for generation in range(generations):
        fitness, truck_loads_list = cal_fitness(paketa, fortigo_info, population)
        num_parents = population_size // 2
        parents = selection(fitness, num_parents, population)
        offsprings = crossover(parents, population_size - num_parents)
        mutants = mutation(offsprings)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants

    best_fitness = np.where(fitness == np.max(fitness))
    best_solution = population[best_fitness[0][0], :]
    best_truck_loads = truck_loads_list[best_fitness[0][0]]

    return best_solution, best_truck_loads


# Main Program
#_______________________________________________________________________________________________________________________________________________
def main():
    paketa = []
    plithos_paketon = int(input("\nPlease enter the number of the parcels that you wish to transfer: "))
    for i in range(plithos_paketon):
        mikos = float(input("\nPlease enter the parcel's length (in meters): "))
        platos = float(input("Please enter the parcel's width (in meters): "))
        ipsos = float(input("Please enter the parcel's height (in meters): "))
        baros = float(input("Please enter the parcel's weight (in kilograms): "))
        timoula = float(input("Please enter the parcel's price: "))
        paketa.append({'Lenght': mikos, 'Width': platos, 'Height': ipsos, 'Weight': baros, 'Price': timoula})

    fortigo_info = []
    plithos_fortigon = int(input("\nPlease enter the number of the trucks provided: "))
    for i in range(plithos_fortigon):
        mikos = float(input("\nPlease enter the truck's length (in meters): "))
        platos = float(input("Please enter the truck's width (in meters): "))
        ipsos = float(input("Please enter the truck's height (in meters): "))
        max_baros = float(input("Please enter the truck's maximum weight (in kilograms): "))
        fortigo_info.append({'Lenght': mikos, 'Width': platos, 'Height': ipsos, 'Maximum_Weight': max_baros, 'Current_Weight': 0, 'Parcels': []})

    print("\n------------------------------------------------------------------------------------------------------------")
    print("The list of parcel(s) is as follows:\n")
    print("Item No.        Length          Width           Height          Weight          Price")
    for item_no, parcel in enumerate(paketa, start=1):
        print(f"{item_no}\t\t{parcel['Lenght']}\t\t{parcel['Width']}\t\t{parcel['Height']}\t\t{parcel['Weight']}\t\t{parcel['Price']}")

    best_solution, best_truck_loads = optimize(paketa, fortigo_info)
    sinoliki_timi = sum(parcel['Price'] for i, parcel in enumerate(paketa) if best_solution[i] == 1)

    print("\n------------------------------------------------------------------------------------------------------------")
    print("The truck's info after the parcel(s) is the following:\n")
    for truck in best_truck_loads:
        for key, value in truck.items():
            print(f"{key}: {value}")
        print()

    print("------------------------------------------------------------------------------------------------------------")
    print("Best solution found:\n")
    for i, paketa in enumerate(paketa):
        if best_solution[i] == 1:
            print(f"Parcel {i + 1}: {paketa}")
    print("\n------------------------------------------------------------------------------------------------------------")
    print("The total value of the items that can fit into the trucks is: ", sinoliki_timi, "\n")



if __name__ == "__main__":
    main()



"""
________________________________________________________________________________________________________________
How the program is executed with 5 packages (two in the truck and the other two in the other while the last stays out of the trucks

miketsimpas@Michaels-MacBook-Air ~ % /usr/local/bin/python3 /Users/miketsimpas/Documents/Uni/VScode/Python/MachineLearning/2nd_P
roject.py

Please enter the number of the parcels that you wish to transfer: 5 

Please enter the parcel's length (in meters): 2
Please enter the parcel's width (in meters): 2
Please enter the parcel's height (in meters): 10
Please enter the parcel's weight (in kilograms): 10
Please enter the parcel's price: 10

Please enter the parcel's length (in meters): 2
Please enter the parcel's width (in meters): 2
Please enter the parcel's height (in meters): 10
Please enter the parcel's weight (in kilograms): 10
Please enter the parcel's price: 10

Please enter the parcel's length (in meters): 100
Please enter the parcel's width (in meters): 100
Please enter the parcel's height (in meters): 100
Please enter the parcel's weight (in kilograms): 100
Please enter the parcel's price: 100

Please enter the parcel's length (in meters): 2
Please enter the parcel's width (in meters): 2
Please enter the parcel's height (in meters): 12
Please enter the parcel's weight (in kilograms): 10
Please enter the parcel's price: 10

Please enter the parcel's length (in meters): 2
Please enter the parcel's width (in meters): 5
Please enter the parcel's height (in meters): 10
Please enter the parcel's weight (in kilograms): 10
Please enter the parcel's price: 10

Please enter the number of the trucks provided: 2

Please enter the truck's length (in meters): 4
Please enter the truck's width (in meters): 4
Please enter the truck's height (in meters): 10
Please enter the truck's maximum weight (in kilograms): 20

Please enter the truck's length (in meters): 15
Please enter the truck's width (in meters): 15
Please enter the truck's height (in meters): 12
Please enter the truck's maximum weight (in kilograms): 20

------------------------------------------------------------------------------------------------------------
The list of parcel(s) is as follows:

Item No.        Length          Width           Height          Weight          Price
1               2.0             2.0             10.0            10.0            10.0
2               2.0             2.0             10.0            10.0            10.0
3               100.0           100.0           100.0           100.0           100.0
4               2.0             2.0             12.0            10.0            10.0
5               2.0             5.0             10.0            10.0            10.0

------------------------------------------------------------------------------------------------------------
The truck's info after the parcel(s) is the following:

Length: 4.0
Width: 4.0
Height: 10.0
Maximum_Weight: 20.0
Current_Weight: 20.0
Parcels: [1, 2]

Length: 15.0
Width: 15.0
Height: 12.0
Maximum_Weight: 20.0
Current_Weight: 20.0
Parcels: [4, 5]

------------------------------------------------------------------------------------------------------------
Best solution found:

Parcel 1: {'Lenght': 2.0, 'Width': 2.0, 'Height': 10.0, 'Weight': 10.0, 'Price': 10.0}
Parcel 2: {'Lenght': 2.0, 'Width': 2.0, 'Height': 10.0, 'Weight': 10.0, 'Price': 10.0}
Parcel 4: {'Lenght': 2.0, 'Width': 2.0, 'Height': 12.0, 'Weight': 10.0, 'Price': 10.0}
Parcel 5: {'Lenght': 2.0, 'Width': 5.0, 'Height': 10.0, 'Weight': 10.0, 'Price': 10.0}

------------------------------------------------------------------------------------------------------------
The total value of the items that can fit into the trucks is:  40.0 

miketsimpas@Michaels-MacBook-Air ~ % 


"""
