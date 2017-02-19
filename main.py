#!/usr/bin/python
import numpy as np


def print_sudoku(list_sud):
    for i in range(9):
        if i%3==0:
            print '-----------------------\n',
        for j in range(9):
            if j%3==0:
                print '|',
            print list_sud[i][j],
        print

    print '-----------------------\n'






def find_domain(l,list_sud):

    x = l[0]; y = l[1]

    if x/3==1:
        x1=0 ; x2 = 3
    if x/3 == 2 :
        x1 = 3 ; x2 = 6
    if x/3 ==3 :
        x1 = 6 ; x2 =9
    if y/3==1:
        y1=0 ; y2 = 3
    if y/3 == 2 :
        y1 = 3 ; y2 = 6
    if y/3 ==3 :
        y1 = 6 ; y2 =9

        return list(set(list_sud[:,y]) & set(list_sud[x,:]) & set(np.unique(list_sud[x1:x2,y1:y2])) )





def find_empty_location(list_sud, l):
    for row in range(9):
        for col in range(9):
            if (list_sud[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


# Returns a boolean which indicates whether any assigned entry
# in the specified row matches the given number.
def used_in_row(list_sud, row, num):
    for i in range(9):
        if (list_sud[row][i] == num):
            return True
    return False


# Returns a boolean which indicates whether any assigned entry
# in the specified column matches the given number.
def used_in_col(list_sud, col, num):
    for i in range(9):
        if (list_sud[i][col] == num):
            return True
    return False


# Returns a boolean which indicates whether any assigned entry
# within the specified 3x3 box matches the given number
def used_in_box(list_sud, row, col, num):
    for i in range(3):
        for j in range(3):
            if (list_sud[i + row][j + col] == num):
                return True
    return False


# Checks whether it will be legal to assign num to the given row,col
# Returns a boolean which indicates whether it will be legal to assign
# num to the given row,col location.
def check_location_is_safe(list_sud, row, col, num):
    # Check if 'num' is not already placed in current row,
    # current column and current 3x3 box
    return not used_in_row(list_sud, row, num) \
        and not used_in_col(list_sud, col, num)\
	and not used_in_box(list_sud, row - row % 3, col - col % 3, num)


def solve_sudoku(list_sud):
    # 'l' is a list variable that keeps the record of row and col in find_empty_location Function
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location(list_sud, l)):
        return True

    # Assigning list values to row and col that we got from the above Function
    row = l[0]
    col = l[1]

    # consider digits 1 to 9
    for num in range(1, 10):

        # if looks promising
        if (check_location_is_safe(list_sud, row, col, num)):

            # make tentative assignment
            list_sud[row][col] = num

            # return, if sucess, ya!
            if (solve_sudoku(list_sud)):
                return True

            # failure, unmake & try again
            list_sud[row][col] = 0

    # this triggers backtracking
    return False


# Driver main function to test above functions
if __name__ == "__main__":


    with open('evenMoreConsistent.txt','rb') as fp:
        lines=fp.readlines()
        data_dict = {}
        count=0
        temp_data = []
        for line in lines:
            if 'easy' in line or 'medium' in line or 'hard' in line  or 'evil' in line:
                data_dict[count]=np.array(temp_data)
                count+=1
                temp_data=[]
                continue
            else:
                if line!='\n':
                    temp_data += [map(int,list(line[:-1]))]




    del data_dict[0]

    for key in [1]:
        domain_dict={}
        sud_array =data_dict[key]

        for i in range(9):
            for j in range(9):
                if sud_array[i,j]==0:
                    domain_dict[i,j] = find_domain([i,j],sud_array)
                else:
                    domain_dict[i,j] = [sud_array[i,j]]

        print domain_dict
        print key,solve_sudoku(data_dict[key])
        print_sudoku(data_dict[key])
