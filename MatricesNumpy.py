from fractions import Fraction
import numpy as np


def initialize_matrix():   # initializes a new matrix
    print("Enter a new matrix:")
    new_matrix = []        # total matrix
    s = input()            # every it's row

    while s != "":         # going by rows
        new_matrix.append(s.split())  # add new row by splitting the input string
        s = input()

    new_matrix = np.matrix(new_matrix)
    new_matrix = new_matrix.astype('float')
    return new_matrix


def matrix_int(mat):  # Bring all values in matrix to integers by multiplication
    coefs = []  # Array for denominators which aren't 1
    # Check if there are any fractions and add to coefs denominators of Fractions
    for i in range(len(mat)):
        for j in range(len(mat[0])):
           if mat[i, j].denominator != 1:
               coefs.append(mat[i, j].denominator)
    # If all int - return matrix
    if not coefs:
        return mat.astype('int')
    # If not, use found denominators, find lcm and multiply all elements
    coefs = np.array(coefs)
    coefs = np.lcm.reduce(coefs)
    mat *= coefs
    # Since denominators are 1, make everything Integer
    mat = mat.astype('int')

    return mat


def extract_from_matrix(mat):  # Takes a matrix and creates equations based on it
    aug = input('Is matrix Augmented?\n')
    aug.lower()
    if aug in 'yes1':
        aug = 1
    else:
        aug = -1

    for i, v in enumerate(mat):
        temp = v  # shows if we found first non-zero element in the row
        temp = temp[temp != 0]

        numer = sum(temp[1:])
        if numer:
            numer = temp[0] / numer
        else:
            print('x{} = 0'.format(chr(ord('1') + i)))
            continue

        print(temp[0], 'x', chr(ord('1') + i),' = ', sep = '', end='')
        for j in range(1, len(temp)):
            if j == len(temp) -1:
                temp[j] *= (-1)
            print(temp[j] * (-1), ' + ' if j < len(temp) - 1 else '', sep='', end='') # print value and '+' if there are more

        print('  x = {:.3f}'.format(numer))

    print()


def rref(mat, form = 'raw'):  # get matrix to RERF from REF
    if form == 'raw':
        mat = ref(mat)

    # Subtract row underneath if it exists
    try:
        mat[0] -= mat[1] * mat[0, 1]
    except:
        return mat

    # Create matrix less and RREF it
    mat_1 = rref(mat[1:, 1:], '')
    # Stick RREF'd remainder to 0th row and 0th column
    mat = np.vstack([mat[0], np.hstack([mat[1:, :1], mat_1]) ])
    # Subtract all rows underneath 0th in new matrix
    for i in range(1, len(mat)):  # account for situations when pivot isn't on main diagonal
        non_zero_indx = i
        for non_zero_indx in range(i, len(mat[0])):  # find pivot by going from diagonal to the right
            if mat[i, non_zero_indx] != 0:
                break
        mat[0] -= mat[i] * mat[0, non_zero_indx]
    return mat


def ref(mat):  # get matrix to row-echelon form
    # If matrix has one row or column - it's already in form
    r, c = mat.shape
    if r == 0 or c == 0:
        return mat

    # Search for non-zero element in the first column
    for i in range(len(mat)):
        if mat[i, 0] != 0:
            break
    else:
        # If all elements in the first column are zeroes,
        # Perform Row-Echelon Reduction(REF) on other columns
        mat_1 = ref(mat[:, 1:])
        # Return first column plus reduced remaining matrix
        return np.hstack([mat[:, :1], mat_1])

    # If found non-zero not in the first row, we change rows
    if i > 0:
        temp = mat[i].copy()
        mat[i] = mat[0]
        mat[0] = temp

    # Divide 1st row by pivot of it
    mat[0] /= mat[0, 0]
    # Subtract all subsequent rows with first row (it has 1 now as first element)
    # multiplied by the corresponding element in the first column
    mat[1:] -= mat[0] * mat[1:, 0:1]

    # Perform REF on matrix from second row, from second column
    mat_1 = ref(mat[1:, 1:])

    # Add first row and first column, and return
    return np.vstack([mat[:1], np.hstack([mat[1:, :1], mat_1]) ])


choice = " "
while choice.lower() not in 'exit|stop'.lower():
    print("Choose Option:")
    print("1. Simplify Matrix(Row-Echelon)")
    print("2. Find Determinant of a Matrix")
    print("3. Find Inverse of a Matrix")
    print("4. Multiply 2 Matrices")
    print("Exit/Stop")
    choice = input()

    if choice == '1':
        M = initialize_matrix()  # Create matrix from keyboard
        M = M.astype('int')      # Make it all integers for purposes of fractions
        M = np.array(M) + Fraction()  # Turn np array into array of Fractions
        M = rref(M)  # RREF out of REF form
        M = matrix_int(M)  # Turn all into integers
        print('Ans:\n')
        print(np.matrix(M))
        extract_from_matrix(M)

    elif choice == '2':
        M = initialize_matrix()
        print('Ans:\n')
        print(np.linalg.det(M))

    elif choice == '3':
        M = initialize_matrix()
        print('Ans:\n')
        print('Determinant = ', np.linalg.det(M))
        try:
            print(np.linalg.inv(M))
        except:
            print('Presudo inverse:')
            print(np.linalg.pinv(M))

    elif choice == '4':
        x = initialize_matrix()
        y = initialize_matrix()
        print('Ans:\n')
        print(x * y)
