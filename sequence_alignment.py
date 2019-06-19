import sys

MAX_INT = sys.maxsize

GAP = 2
MISMATCH = 3

GAP_CHARACTER = '_'

def build_solution(sequence_a, sequence_b):
    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1 # [0..4] se o tamanho da palavra for 4 [0..3]

    matrix = [[GAP * row] + ([0] * (columns - 1)) for row in range(rows)]
    matrix[0] = [GAP * column for column in range(columns)]

    for row in range(1, rows):
        for column in range(1, columns):
            # Verificação se é match ou mismatch
            if sequence_b[column - 1] == sequence_a[row - 1]:
                mismatch = 0
            else:
                mismatch = MISMATCH
            
            # Verificar o menor dentre os adjacentes
            results = [matrix[row - 1][column - 1] + mismatch, matrix[row - 1][column] + GAP, matrix[row][column - 1] + GAP]

            matrix[row][column] = min(results)

    penalty = matrix[rows - 1][columns - 1]

    return matrix, penalty


def find_solution(matrix, sequence_a, sequence_b):
    # Initial position
    row = len(sequence_a)
    column = len(sequence_b)

    solution_a = ''
    solution_b = ''

    while column != 0 or row != 0:
        adj = []
        if column > 0 and row > 0:
            adj = [matrix[row - 1][column - 1], matrix[row - 1][column], matrix[row][column - 1]]
        else:
            adj.append(MAX_INT)
            if row == 0:
                adj.append(MAX_INT)
            else:
                adj.append(matrix[row - 1][column])
            if column == 0:
                adj.append(MAX_INT)
            else:
                adj.append(matrix[row][column - 1])

        index = adj.index(min(adj))
        if index == 0:
            solution_a += sequence_a[row - 1]
            solution_b += sequence_b[column - 1]
            row -= 1
            column -= 1
        elif index == 1:
            solution_a += sequence_a[row - 1]
            solution_b += GAP_CHARACTER
            row -= 1
        elif index == 2:
            solution_a += GAP_CHARACTER
            solution_b += sequence_b[column - 1]
            column -= 1
    return solution_a[::-1], solution_b[::-1]


def print_solution(matrix, sequence_a, sequence_b):

    print("  " + GAP_CHARACTER, end=' ')
    result = '  ' + GAP_CHARACTER + ' '

    for i in range(len(sequence_b)):
        print(sequence_b[i], end=' ')
        result += str(sequence_b[i]) + ' '

    print()
    result += "\n"

    for i in range(0, len(matrix)):
        if i == 0:
            print(GAP_CHARACTER, end=' ')
            result += GAP_CHARACTER + ' '
        else:
            print(sequence_a[i - 1], end=' ')
            result += str(sequence_a[i - 1]) + ' '
        for j in range(0, len(matrix[0])):
                print(matrix[i][j], end=' ')
                result += str(matrix[i][j]) + ' '
        print()
        result += "\n"

    return result

if __name__ == '__main__':
    line_sequence = str(input("Line Sequence: "))
    column_sequence = str(input("Column Sequence: "))

    print(line_sequence)
    print(len(line_sequence))
    print(column_sequence)
    print(len(column_sequence))

    matrix, penalty = build_solution(line_sequence, column_sequence)

    print_solution(matrix, line_sequence, column_sequence)

    for row in matrix:
        print(row)

    solution_a, solution_b = find_solution(matrix, line_sequence, column_sequence)

    print(penalty)
    print(solution_a)
    print(solution_b)
