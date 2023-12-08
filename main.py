import os
from random import choices, randint, randrange, random

# r1: É necessário haver no mínimo 1 enfermeiro e no máximo 3 enfermeiros em cada turno.
def r1(genome, min, max):
  fault = 0
  for j in range(len(genome[0])):
    sum_ = 0
    for i in range(len(genome)):
      sum_ += genome[i][j]
    
    fault += int(min > sum_ or sum_ > max)
    
  return -fault


# r2: Cada enfermeiro deve ser alocado em 5 turnos por semana.
def r2(genome, numTurn):
  fault = 0
  for i in range(len(genome)):
    fault += int(sum(genome[i]) != numTurn)

  return -fault


# r3: Nenhum enfermeiro pode trabalhar mais que 3 dias seguidos sem folga.
def r3(genome, r3MaxConsecWorkDays):
  turnByDay = int(len(genome[0]) / 7)
  fault = 0
  for i in range(len(genome)):
    for j in range(0, len(genome[0]), turnByDay):
      sumDays = 0
      for r in range(min(r3MaxConsecWorkDays + 1, len(genome[0]))):
        sumDays += int(sum(genome[i][j + turnByDay * r:j + turnByDay * (r + 1)]) >= 1)
      
        if sumDays > r3MaxConsecWorkDays:
          fault += 1
          break
      
      if sumDays > r3MaxConsecWorkDays: 
          break

  return -fault


# r4: Enfermeiros preferem consistência em seus horários, ou seja, eles preferem trabalhar todos os dias da semana no mesmo turno (dia, noite, ou madrugada).
def r4(genome):
  turnByDay = int(len(genome[0]) / 7)
  fault = 0
  for j in range(len(genome)):
    # 0, 3, 6, 9, 12, 15, 18
    # 1, 4, 7, 10, 13, 16, 19
    # 2, 5, 8, 11, 14, 17, 20
    day = int(sum([genome[j][i] for i in range(0, len(genome[0]), turnByDay)]) >= 1)
    night = int(sum([genome[j][i] for i in range(1, len(genome[0]), turnByDay)]) >= 1)
    dawn = int(sum([genome[j][i] for i in range(2, len(genome[0]), turnByDay)]) >= 1)

    fault += int((day + night + dawn) > 1)

  return -fault


# Algoritmo Genético -----------------------------------------------

def generate_genome(numEnf, n):
    genome = []

    for _ in range(numEnf):
       genome.append(choices([0, 1], k=n))

    return genome


def generate_population(k, n, popSize):
    return [generate_genome(k, n) for _ in range(popSize)]


def convertMatrixToSingleLine(genome):
    strComb = ""
    
    for g in genome:
      strComb += "".join([str(v) for v in g])

    return strComb

def convertSingleLineToMatrix(lineGenome, n):
    genome = []
    indexToSee = [i for i in range(0, len(lineGenome), n)]

    for i in range(len(indexToSee)):
      aux = []
      i1 = indexToSee[i]

      if i + 1 < len(indexToSee):
        aux = lineGenome[i1:indexToSee[i + 1]]
      else:
        aux = lineGenome[i1:]
       
      genome.append([int(i) for i in aux])

    return genome


def crossover(genomeA, genomeB):
    if len(genomeA) != len(genomeB):
        raise ValueError("Os genomas A e B precisam ser do mesmo tamanho!")

    length = len(genomeA)
    if length < 2:
        return genomeA, genomeB

    genA = convertMatrixToSingleLine(genomeA)
    genB = convertMatrixToSingleLine(genomeB)
    
    p = randint(1, length - 1)
    newGenA = genA[0:p] + genB[p:]
    newGenB = genB[0:p] + genA[p:]

    return convertSingleLineToMatrix(newGenA, len(genomeA[0])), convertSingleLineToMatrix(newGenB, len(genomeB[0]))


def mutation(genome, mutationRatio):
    genomeL = list(convertMatrixToSingleLine(genome))
    index = randrange(len(genomeL))
    genomeL[index] = genomeL[index] if random() > mutationRatio else abs(int(genomeL[index]) - 1)

    return convertSingleLineToMatrix(genomeL, len(genome[0]))


def fitness(genome, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays):
    r1C = r1(genome, r1Min, r1Max)
    r2C = r2(genome, r2NumTurn)
    r3C = r3(genome, r3MaxConsecWorkDays)
    r4C = r4(genome)

    return r1C + r2C + r3C + r4C


# tournament selection
def tournament_selection(population, scores, k = 15):
  selection_ix = randint(0, len(scores) - 1)

  indexes = [randint(0, len(scores) - 1) for _ in range(k - 1)]
  for ix in indexes:
    if scores[ix] > scores[selection_ix]:
      selection_ix = ix

  return population[selection_ix]


def population_fitness(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays):
    return sum([fitness(genome, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays) for genome in population])


def sort_population(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays):
    return sorted(population, key=lambda genome: fitness(genome, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays), reverse=True)


def genome_to_string(genome):
    strComb = ""
    for g in genome:
       strComb += "\n" + str(g)
    strComb += "\n"
    return strComb

def print_stats(population, generation_id, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays):
    print("GERAÇÃO %02d" % generation_id)
    print("=============")
    print("Média de Fitness: %f" % (population_fitness(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays) / len(population)))

    sorted_population = sort_population(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)

    print("Melhor: %s" % genome_to_string(sorted_population[0]))
    print("R1: %d" % r1(sorted_population[0], r1Min, r1Max))
    print("R2: %d" % r2(sorted_population[0], r2NumTurn))
    print("R3: %d" % r3(sorted_population[0], r3MaxConsecWorkDays))
    print("R4: %d" % r4(sorted_population[0]))
    print("Fitness total: %d" % fitness(sorted_population[0], r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays))

    return sorted_population[0]


def run_evolution(k, n, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, popSize, maxInter, elitism_ratio, mutation_ratio):
    population = generate_population(k, n, popSize)

    bestFitness = float("-inf")
    bestPopulation = population.copy()
    bestGeneration = 0

    for i in range(maxInter):
        scores = [fitness(p, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays) for p in population]
        selected = [tournament_selection(population, scores) for _ in range(popSize)]

        next_generation = []

        canSubtract = False
        if random() < elitism_ratio:
          canSubtract = True
          next_generation = sort_population(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)[0:2]

        populationLen = len(population)
        for j in range(2 if canSubtract else 0, populationLen if populationLen % 2 == 0 else (populationLen - 1), 2):
            parentA, parentB = selected[j], selected[j + 1]

            offspring_a, offspring_b = crossover(parentA, parentB)
            offspring_a = mutation(offspring_a, mutation_ratio)
            offspring_b = mutation(offspring_b, mutation_ratio)
            next_generation += [offspring_a, offspring_b]

        next_generation = sort_population(next_generation, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)
        bestFitnessNextGen = fitness(next_generation[0], r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)

        if(bestFitnessNextGen > bestFitness):
           bestFitness = bestFitnessNextGen
           bestPopulation = next_generation
           bestGeneration = i + 1

        population = next_generation
        print(f"N° {i + 1} de {maxInter} e fitness: {bestFitness}")

    return bestPopulation, bestGeneration


# Métodos para experimentos -----------------------------------------------
def clear_log(folderName):
  folderPath = os.path.join("resultadoExperimentacao", folderName)
  logFilePath = os.path.join(folderPath, "log.txt")

  with open(logFilePath, "w") as logFile:
    logFile.write("")
    logFile.close()

def log_execution_final(population, generation_id, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, folderName, nExecucao):
  print_stats(population, generation_id, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)
  folderPath = os.path.join("resultadoExperimentacao", folderName)

  if not os.path.exists(folderPath):
    os.makedirs(folderPath)
  
  logFilePath = os.path.join(folderPath, "log.txt")

  with open(logFilePath, "a") as logFile:
    logFile.write(f"EXECUCAO {nExecucao}\n")
    logFile.write(f"GERACAO {generation_id}\n")
    logFile.write("=============\n")
    logFile.write("Media de Fitness: %f\n" % (population_fitness(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays) / len(population)))
    
    sorted_population = sort_population(population, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)
    
    logFile.write("Melhor: %s\n" % genome_to_string(sorted_population[0]))
    logFile.write("R1: %d\n" % r1(sorted_population[0], r1Min, r1Max))
    logFile.write("R2: %d\n" % r2(sorted_population[0], r2NumTurn))
    logFile.write("R3: %d\n" % r3(sorted_population[0], r3MaxConsecWorkDays))
    logFile.write("R4: %d\n" % r4(sorted_population[0]))
    logFile.write("Fitness total: %d\n" % fitness(sorted_population[0], r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays))
    logFile.write("\n\n")
    logFile.close()

# Experimentação -----------------------------------------------
def experimentation_01():
  k = 10
  n = 21

  # Parâmetros referentes somente aos requisitos
  r1Min = 1
  r1Max = 3
  r2NumTurn = 5
  r3MaxConsecWorkDays = 3

  # Demais parâmetros
  popSize = 100
  maxInter = 1000
  mutation_ratio = 0.1

  elitism_list = [0, 0.1, 0.25, 0.5, 0.75]

  clear_log("bloco01")
  for nExecucao in range(1, 11):
    for elitism_ratio in elitism_list:
      population, i = run_evolution(k, n, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, popSize, maxInter, elitism_ratio, mutation_ratio)
      log_execution_final(population, i, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, "bloco01", nExecucao)
  
def experimentation_02():
  k = 10
  n = 21

  # Parâmetros referentes somente aos requisitos
  r1Min = 1
  r1Max = 3
  r2NumTurn = 5
  r3MaxConsecWorkDays = 3

  # Demais parâmetros
  maxInter = 1000
  mutation_ratio = 0.1
  elitism_ratio = 0.1

  popSizeList = [10, 25, 50, 100, 500, 1000]

  clear_log("bloco02")
  for nExecucao in range(1, 11):
    for popSize in popSizeList:
      population, i = run_evolution(k, n, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, popSize, maxInter, elitism_ratio, mutation_ratio)
      log_execution_final(population, i, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, "bloco02", nExecucao)


if __name__ == "__main__":
  print("AT3: Algoritmos Genéticos\n")

  # Execução 
  executar_testes = input("Tecle '1' para executar as simulações de teste ou '2' para a execução padrão do programa: ").lower() == '1'

  if not executar_testes:  
    # k enfermeiros e n turnos
    k = 10
    n = 21

    # Solicitar valores ao usuário para os parâmetros desejados
    popSize = int(input("Digite o tamanho da população: "))
    maxInter = int(input("Digite o número de gerações (interações): "))
    elitism_ratio = float(input("Digite a taxa de elitismo: "))
    mutation_ratio = float(input("Digite a taxa de mutação: "))
    
    # Parâmetros referentes somente aos requisitos
    r1Min = 1
    r1Max = 3
    r2NumTurn = 5
    r3MaxConsecWorkDays = 3

    # Função de resolução
    population, i = run_evolution(k, n, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays, popSize, maxInter, elitism_ratio, mutation_ratio)

    print("###### Melhor população ######")
    print_stats(population, i, r1Min, r1Max, r2NumTurn, r3MaxConsecWorkDays)
  else:
    # Experimentação
    teste = input("Tecle '1' para executar a experimentação 01 ou '2' para executar a experimentação 02: ")
    if teste.lower() == '1':
      experimentation_01()
    elif teste.lower() == '2':
      experimentation_02()