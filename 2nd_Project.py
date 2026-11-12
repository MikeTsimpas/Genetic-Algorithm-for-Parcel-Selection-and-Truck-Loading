"""
Τσίμπας Μιχαήλ (2121067 - 7o Εξάμηνο)
2o Project Υπολογιστική Νοημοσύνη και Μηχανική Μάθηση - Τελευτάιο Ψηφίο AM = 7
------------------------------------------------------------------------------
Σύνολο Δεδομένων που Χρησιμοποιήθηκαν:
[...]

Σύνολο APIs που Χρησιμοποιήθηκαν:
Python Standard Library, Numpy, Random

------------------------------------------------------------------------------
Ti exoume:

Paketo -> (Mikos, Platos, Ypsos) / Timi_Metaforas | Input Values
Fortigo -> Dimentions(Mikos, Platos, Ypsos) / Max_Baros

To problima linetai se two-dimentional epipedo xorou,
Den bazoume paketa to ena pano sto allo
Brisko posa paketa metaferontai kai pose oxi
Genetiko algorithm, OXI swarm intelligence gia to best price
------------------------------------------------------------------------------
"""

import numpy as np
import random as rd
from random import randint

# ΑΡΧΉ ΆΣΚΗΣΗΣ
#_______________________________________________________________________________________________________________________________________________
np.random.seed(0)
rd.seed(0)

def cal_fitness(paketa, fortigo, population):                                                                               # Ξεκινάμε την συνάρτηση cal_fitness
    fitness = np.empty(population.shape[0])                                                                                 # Φτιάχνουμε έναν κενό πίνακα για να αποθηκεύσουμε τις fitness τιμες
    truck_loads_list = []                                                                                                   # Φτιάχνουμε ένα κενό truck_loads_list για να το χρησιμοποιήσουμε στην συνάρτηση
    for i in range(population.shape[0]):                                                                                    # Κάνουμε επανάλυψη για κάθε λύση στο popylation 
        sinoliki_aksia = 0                                                                                                  # Αρχικοποιούμε την συνολική αξία των δεμάτων -θα την βρούμε αργότερα-
        # Δημιουργούμε την truck_loads και θα την εμφανίσουμε και αργότερα
        truck_loads = [{'Length': fortigo[truck_index]['Lenght'], 'Width': fortigo[truck_index]['Width'],'Height': fortigo[truck_index]['Height'], 'Maximum_Weight': fortigo[truck_index]['Maximum_Weight'], 'Current_Weight': 0, 'Parcels': []} for truck_index in range(len(fortigo))]
        valid_solution = True
        for j in range(population.shape[1]):                                                                                # Για κάθε πακέτο
            if population[i, j] == 1:                                                                                       # Εαν υπάρχει αυτό το πακέτο στην λύση αυτή
                parcel_added = False
                for truck_index, truck in enumerate(truck_loads):                                                           # Για κάθε φορτηγό
                    if (truck['Current_Weight'] + paketa[j]['Weight'] <= fortigo[truck_index]['Maximum_Weight'] and         # Εαν το βάρος που έχει τώρα το φορτηγό μαζί με το βάρος του πακέτου είναι μικρότερο από το μέγιστο βάρος του φορτηγού
                        truck['Length'] >= paketa[j]['Lenght'] and                                                          # Και το μέγεθος του φορτηγού είναι μεγαλύτερο από το μέγευος του πακέτου
                        truck['Height'] >= paketa[j]['Height'] and                                                          # Και το ύψος του φορτηγού είναι μεγαλύτερο από το ύψος του πακέτοθ
                        truck['Width'] >= paketa[j]['Width']):                                                              # Και το πλάτος του φορτηγού είναι μεγαλύτερο από το πλάτος του πακέτου
                        truck['Current_Weight'] += paketa[j]['Weight']                                                      # Τότε βάλε το βάρος του πακέτου στο βάρος που έχει τώρα το φορτηγό
                        truck['Parcels'].append(j + 1)                                                                      # Βάζουμε το πακέτο στο φορτηγό
                        sinoliki_aksia += paketa[j]['Price']                                                                # Βάζουμε στην τελική συνολική αξία την αξία του δέματος που μόλις βάλαμε
                        parcel_added = True
                        break
                if not parcel_added:
                    valid_solution = False
                    break
        if not valid_solution:
            sinoliki_aksia = 0
        fitness[i] = sinoliki_aksia
        truck_loads_list.append(truck_loads)
    return fitness.astype(int), truck_loads_list                                                                            # Τέλος επιστρέφουμε στο πρόγραμμα τις κατάλληλες μεταβλητές (την λίστα του φορτηγού και το fitness)
#________________________________________________________________________________________________________________

def selection(fitness, num_parents, population):                                                                            # Ξεκινάμε την συνάρτηση selection
    fitness = list(fitness)                                                                                                 # Μετατρέπουμε τον fitness πίνακα σε λίστα
    parents = np.empty((num_parents, population.shape[1]))                                                                  # Δημιουργούμε έναν κενό πίνακα για να αποθηκεύσουμε τα επιλεγέμα parents
    for i in range(num_parents):                                                                                            # Μέσω επανάλληψης ανάλογα με τον ααριυμό των parents
        max_fitness = np.where(fitness == np. max(fitness))                                                                 # Βρίσκουμε το μέγιστο fitness στην λίστα
        parents[i, :] = population[max_fitness[0][0], :]                                                                    # Αντιγράφουμε το population με την μέγιστη τιμή στον πίνακα parent
        fitness[max_fitness[0][0]] = -999999                                                                                # Βάζουμε μια πολύ μικρή τιμή ώστε να την ξεπεράσει
    return parents                                                                                                          # Επιστρέφουμε το parents
#________________________________________________________________________________________________________________

def crossover(parents, number_of_offsprings):                                                                               # Ξεκινάμε την συνάρτηση crossover
    offsprings = np.empty((number_of_offsprings, parents.shape[1]))                                                         # Δημιουργούμε ένα κενό πίνακαμε διαστάσεις (number_of_offsprings, parents.shape[1])
    crossover_point = int(parents.shape[1] / 2)                                                                             # Βρίσκουμε το crossover στο μεσαίο σημείο
    crossover_rate = 0.8                                                            
    i = 0
    while i < number_of_offsprings:                                                                                         # Όσο το i είναι μικρότερο του number_of_offsprings
        parent1_index = i % parents.shape[0]                                                                                # Ο Parent 1 παίρνει την τιμή του parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]                                                                          # O Parent 2 παίρνει την επόμενη τιμή του -//-
        x = rd.random()                                                                                                     # Φτιάχνουμε έναν τυχαίο αριθμό (ή 0 ή 1)
        if x <= crossover_rate:                                                                                             # Εανείναι μικρότερο ή ίσο με το crossover_rate (0.8 από πρίν που το ορίσαμε)
            offsprings[i, 0:crossover_point] = parents[parent1_index, 0:crossover_point]                                    # Το πρώτο μέρος παίρνει το parent 1
            offsprings[i, crossover_point:] = parents[parent2_index, crossover_point:]                                      # Το δεύτερο μέρος παίρνει το parent 2
        else:                                                                                                               # Αλλθώς...
            offsprings[i, :] = parents[parent1_index, :]                                                                    # Το παίρνει όλο το parent 1
        i += 1                                                                                                              # i+1 και πάμε για την επόμενη επανάληψη 
    return offsprings                                                                                                       # Και επιστρέφουμε τον πίνακα offsprings που φτιάξαμε
#________________________________________________________________________________________________________________

def mutation(offsprings):                                                                                                   # Ξεκινάμε την συνάρτηση mutation
    mutants = np.empty((offsprings.shape))                                                                                  # Δημιουργούμε έναν κενό πίνακα
    mutation_rate = 0.4 
    for i in range(offsprings.shape[0]):                                                                                    # Ξεκινάμε επανάληψη για κάυε offspring 
        random_timi = rd.random()                                                                                           # Δημιουργούμε μια random τιμή
        mutants[i, :] = offsprings[i, :]                                                                                    # Αντιγράφουμε το συγκεκριμένο offspring στο mutants
        if random_timi < mutation_rate:                                                                                     # Αμα η τυχαία τιμή είναι μικρότερη του mutation_rate (0.4)
            int_random_timi = randint(0, offsprings.shape[1] - 1)                                                           # Καλούμε την rantint με παράμετρο 0 και το άνω μέρος του offspring -1
            mutants[i, int_random_timi] = 1 - mutants[i, int_random_timi]                                                   
    return mutants
#________________________________________________________________________________________________________________

def optimize(paketa, fortigo_info, population_size=10, generations=50):                                                     # Ξεκινάμε την συνάρτηση optimize
    plithos_paketon = len(paketa)                                                                                           # Βγάζουμε το πλήθος των πακέτων
    population = np.random.randint(2, size=(population_size, plithos_paketon))                                              # Δημιουργούμε πίνακα με διαστάσεις population_size, plithos_paketon

    for generation in range(generations):                                                                                   # Επανάληψη σχετικά με το genetarions
        fitness, truck_loads_list = cal_fitness(paketa, fortigo_info, population)                                           # Καλούμε την optimize function με παραμέτρους (paketa, fortigo_info και population)
        num_parents = population_size // 2                                                                                  # Βρίσκουμε τον αριθμό των parents μέσω division του population_size και του 2
        parents = selection(fitness, num_parents, population)                                                               # Καλούμε την συνάρτηση selection με τις καράλληλες παραμέτρους
        offsprings = crossover(parents, population_size - num_parents)                                                      # Καλούμε την συνάρτηση crossover με -//-
        mutants = mutation(offsprings)                                                                                      # Καλούμε την σθνάρτηση mutation με -//-
        population[0:parents.shape[0], :] = parents                                                                         # Αντικαθιστούμε το πρώτο μέρος του population με με το parents και το υπόλοιπο με το mutants
        population[parents.shape[0]:, :] = mutants

    best_fitness = np.where(fitness == np.max(fitness))                                                                     # Βρίσκουμε τους δείκτες των στοιχείων του πίνακα fitness που έχουν maximum value
    best_solution = population[best_fitness[0][0], :]                                                                       # Βάζουμε στην best solution το population του best_fitness[0][0]
    best_truck_loads = truck_loads_list[best_fitness[0][0]]                                                                 # Βάζουμε στο best_truck_loads το truck_loads_list του best_fitness[0][0]

    return best_solution, best_truck_loads


# Κυρίως Πρόγραμμα
#_______________________________________________________________________________________________________________________________________________
def main():                                                                                                                                         # Ξεκινάμε το κύριο πρόγραμμα μάς
    paketa = []
    plithos_paketon = int(input("\nPlease enter the number of the parcels that you wish to transfer: "))                                            # Ρωτάμε στον χρήστη πόσα πακέτα επιθυμεί να εισάγει
    for i in range(plithos_paketon):                                                                                                                # Κάνουμε επανάληψη ανάλογα με τα πακέτα που πληκτρολόγησε
        mikos = float(input("\nPlease enter the parcel's length (in meters): "))                                                                    # Προσθέτει ο μήκος κάθε πακέτου
        platos = float(input("Please enter the parcel's width (in meters): "))                                                                      # Προσθέτει το πλάτος
        ipsos = float(input("Please enter the parcel's height (in meters): "))                                                                      # Το ύψος του
        baros = float(input("Please enter the parcel's weight (in kilograms): "))                                                                   # Το βάρους
        timoula = float(input("Please enter the parcel's price: "))                                                                                 # Και τέλος την τιμή του
        paketa.append({'Lenght': mikos, 'Width': platos, 'Height': ipsos, 'Weight': baros, 'Price': timoula})                                       # Και τα βάζει όλα στο paketa

    fortigo_info = []
    plithos_fortigon = int(input("\nPlease enter the number of the trucks provided: "))                                                             # Κάνουμε το ίδιο για το φορτιγό, στην αρχή ρωτάμε το πλήθος των φορτηγών
    for i in range(plithos_fortigon):                                                                                                               # Και κάνουμε επανάληψη ανάλογα με το πλήθος των φορτηγών
        mikos = float(input("\nPlease enter the truck's length (in meters): "))                                                                     # Προσθέτουμε το ύψος του
        platos = float(input("Please enter the truck's width (in meters): "))                                                                       # Προσθέτουμε το πλάτος του
        ipsos = float(input("Please enter the truck's height (in meters): "))                                                                       # Το ύψος του
        max_baros = float(input("Please enter the truck's maximum weight (in kilograms): "))                                                        # Και τέλος το μέγιστο βάρος που μπορεί να κουβαλήσει
        fortigo_info.append({'Lenght': mikos, 'Width': platos, 'Height': ipsos, 'Maximum_Weight': max_baros, 'Current_Weight': 0, 'Parcels': []})   # Τέλος βάζουμε όλα τα στοιχεία που μας έδωσε ο χρήστης στο ανάλογο φορτηγό

    print("\n------------------------------------------------------------------------------------------------------------")
    print("The list of parcel(s) is as follows:\n")                                                                                                 # Εμφανίζουμε την λίστα με τα πακέτα που έχει εισάγει ο χρήστης (δηλαδή με τα χαρακτηριστικά τους)
    print("Item No.        Length          Width           Height          Weight          Price")
    for item_no, parcel in enumerate(paketa, start=1):
        print(f"{item_no}\t\t{parcel['Lenght']}\t\t{parcel['Width']}\t\t{parcel['Height']}\t\t{parcel['Weight']}\t\t{parcel['Price']}")

    best_solution, best_truck_loads = optimize(paketa, fortigo_info)                                                                                # Τρέχουμε την συνάρτηση optimize με παράμετρο τα πακέτα και τις πληροφορίες του φορτηγού
    sinoliki_timi = sum(parcel['Price'] for i, parcel in enumerate(paketa) if best_solution[i] == 1)                                                # Βρίσκουμε την τελική τιμή των δεμάτων που μπορούνα να μπούν στο φορτηγό

    print("\n------------------------------------------------------------------------------------------------------------")
    print("The truck's info after the parcel(s) is the following:\n")                                                                               # Εμφανίζουμε τις πληροφορίες του/των φορτηγών μετά από τα δέματα που μπόρεσαν να εισέλθουν
    for truck in best_truck_loads:
        for key, value in truck.items():
            print(f"{key}: {value}")
        print()

    print("------------------------------------------------------------------------------------------------------------")
    print("Best solution found:\n")                                                                                                                 # Έπειτα εμφανίζουμε το best solution
    for i, paketa in enumerate(paketa):                                                                                                             # Δηλαδή τα πακέτα που μπορούν να χωρέσουν στα φορτηγά
        if best_solution[i] == 1:
            print(f"Parcel {i + 1}: {paketa}")
    print("\n------------------------------------------------------------------------------------------------------------")
    print("The total value of the items that can fit into the trucks is: ", sinoliki_timi, "\n")                                                    # Και τέλος εμφανίζουμε την συνολική τιμή από όλα τα πακέτα που μπόρεσαν να χωρέσουν στα φορτηγά 



if __name__ == "__main__":
    main()



"""
________________________________________________________________________________________________________________
Παράδειγμα εκτέλεσης αλγορίθμου με 5 πακέτα (τα δύο μπαίνουν στο ένα φορτηγό, τα άλλα δύο στο άλλο και ένα μένει εκτός)

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