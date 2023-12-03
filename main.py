import random

def createMatrix(k = 0, n = 0):
  matrix = []

  for _ in range(k):
    turn = []
    for j in range(n):
      # turn.append(chr(97 + j))
      turn.append(random.randint(0, 1))

    
    print(turn)
    matrix.append(turn)

  return matrix


# r1: É necessário haver no mínimo 1 enfermeiro e no máximo 3 enfermeiros em cada turno.
def r1(matrix, k, n, min, max):
  fault = 0
  for j in range(n):
    sum_ = 0
    for i in range(k):
      sum_ += matrix[i][j]
    
    fault += int(min > sum_ or sum_ > max)
    # print(sum_, fault)
    

  return -fault


# r2: Cada enfermeiro deve ser alocado em 5 turnos por semana.
def r2(matrix, k, num):
  fault = 0
  for i in range(k):
    fault += int(sum(matrix[i]) != num)
    # print(i + 1, sum(matrix[i]))

  return -fault


# r3: Nenhum enfermeiro pode trabalhar mais que 3 dias seguidos sem folga.
def r3(matrix, k, n, max, turnByDay):
  fault = 0
  for i in range(k):
    for j in range(0, n, turnByDay):
      sumDays = 0
      for k in range(min(max + 1, n)):
        # print(matrix[i][j + turnByDay * k:j + turnByDay * (k + 1)], end=" ")
        sumDays += int(sum(matrix[i][j + turnByDay * k:j + turnByDay * (k + 1)]) >= 1)
      
        if sumDays > max:
          fault += 1
          # print()
          break
      
      if sumDays > max:
          print(i, j, fault)    
          break

  return -fault

# r4: Enfermeiros preferem consistência em seus horários, ou seja, eles preferem trabalhar todos os dias da semana no mesmo turno (dia, noite, ou madrugada).
def r4(matrix, k, n, turnByDay):
  day = int(sum([matrix[0][i] for i in range(0, n, turnByDay)]) >= 1)
  night = int(sum([matrix[0][i + 1] for i in range(0, n, turnByDay)]) >= 1)
  dawn = int(sum([matrix[0][i + 2] for i in range(0, n, turnByDay)]) >= 1)

  fault = int((day + night + dawn) > 1)
  return -fault


if __name__ == "__main__":
  k = 2 # 10
  turnByDay = 3
  n = turnByDay * 7
  size_pop = 100
  max_gen = 100
  mutate_ratio = 0.1
  elitism_ratio = 0.1
  
  matrix = createMatrix(k, n)
  # print(r1(matrix, k, n, 1, 3))
  # print(r2(matrix, k, 5))
  # print(r3(matrix, k, n, 3, turnByDay))
  # print(r4(matrix, k, n, turnByDay))