#!/usr/bin/python
import numpy as np
from collections import defaultdict

#back_tracking_count = 0


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



def show_domain(domain_dict):
    for i in range(9):
        if i%3==0:
            print '--------------------------------------------------------------------------------------------------------------------\n',
        for j in range(9):
            if j%3==0:
                print '|',
            if (i,j) in domain_dict:
                a=''.join(map(str,domain_dict[i,j]))
                print a + ' '*(9-len(a)),
            else:
                print 'f'+' '*8,
        print

    print '--------------------------------------------------------------------------------------------------------------------\n'




def finding_coordinates(set_values,k):
    final_dict_values = defaultdict(list)
    for key in sorted(set_values.items(), key=lambda t: -len(t[0])):
        if len(key[0]) == k:
            final_dict_values[key[0]] += set_values[key[0]]
        else:
            for key1 in final_dict_values:
                if key[0].issubset(key1):
                    final_dict_values[key1] += set_values[key[0]]

    return final_dict_values




def remove_domains(indicator,i,j,key,coordinates,domain_dict):
    check_list=[]
    if indicator=='r':
        check_list = [key2 for key2 in domain_dict if i==key2[0]]
    if indicator=='c':
        check_list = [key2 for key2 in domain_dict if j==key2[1]]
    if indicator=='b':
        for i1 in range(i,i+3):
            for j1 in range(j,j+3):
                for key2 in domain_dict:
                    if key2==(i1,j1):
                        check_list+=[key2]
    #print check_list
    for cor in check_list:
        if list(cor) not in coordinates:
            domain_dict[cor]=list(frozenset(domain_dict[cor]).difference(key))
            print "coordinates here", cor













def naked_triples_row(domain_dict,list_sud,k):

    #row unit

    if domain_dict=={}:
        domain_dict = update_domain(domain_dict,list_sud)

    #show_domain(domain_dict)
    for i in range(9):
        set_values = defaultdict(list)
        for j in range(9):
            if (i,j) in domain_dict:
                if len(domain_dict[i,j])<=k:
                    set_values[frozenset(domain_dict[i, j])] += [[i, j]]

        final_dict_values = finding_coordinates(set_values,k)

        for key in final_dict_values:
            if len(final_dict_values[key])==k:
                print "Naked triple found in row ", i, " : ", final_dict_values[key]

                print_sudoku(list_sud)
                show_domain(domain_dict)
                print_sudoku(list_sud)
                show_domain(domain_dict)
                remove_domains('r',i,j, key, final_dict_values[key], domain_dict)
                return True
    return False


def naked_triples_column(domain_dict,list_sud,k):

    #column unit
    for j in range(9):
        set_values = defaultdict(list)


        for i in range(9):
            if (i,j) in domain_dict:
                if len(domain_dict[i,j])<=k:
                    set_values[frozenset(domain_dict[i, j])] += [[i, j]]

        final_dict_values = finding_coordinates(set_values,k)
        for key in final_dict_values:
            if len(final_dict_values[key]) == k:
                print "Naked triple found in col ", j
                remove_domains('c', i, j, key, final_dict_values[key], domain_dict)
                return True

    return False

def naked_triples_box(domain_dict, list_sud, k):

    #box unit
    for i in [0,3,6]:
        for j in [0,3,6]:
            set_values = defaultdict(list)
            for i1 in range(i,i+3):
                for j1 in range(j,j+3):
                    if (i1, j1) in domain_dict:
                        if len(domain_dict[i1, j1]) <= k:
                            set_values[frozenset(domain_dict[i1, j1])] += [[i1, j1]]

            final_dict_values=finding_coordinates(set_values,k)
            for key in final_dict_values:
                if len(final_dict_values[key]) == k:
                    print "Naked triple found in box ", i, " ", j
                    #print key,final_dict_values[key]
                    #print i,j
                    remove_domains('b', i, j, key, final_dict_values[key], domain_dict)
                    return True

    return False









# This function updates domain.
def update_domain(domain_dict,list_sud):

    for (i,j) in domain_dict.keys():
        domain_dict[i, j] = find_domain([i, j], list_sud,domain_dict[i,j])
    return domain_dict


def create_domain(domain_dict,list_sud):

    for i in range(9):
        for j in range(9):
            if list_sud[i, j] == 0:
                domain_dict[i,j]=range(10)

    return domain_dict




def rule3_row(domain_dict,list_stud):
    if domain_dict=={}:
        domain_dict = update_domain(domain_dict,list_sud)


    for i in range(9):

        val_count=defaultdict(int)
        dict_indices = defaultdict(list)
        deleted_list=[]
        for j in range(9):
            if (i,j) in domain_dict:

                for val in domain_dict[i,j]:
                    val_count[val]+=1
                    dict_indices[val]+=[(i,j)]

        for key,item in val_count.items():
            if item==1 and (dict_indices[key][0] not in deleted_list):
                deleted_list+=[dict_indices[key][0]]
                del domain_dict[dict_indices[key][0]]

                #update_domain(domain_dict, list_sud)

                #print dict_indices[key][0], key
                #print dict_indices[key][0]
                #print val_count
                #print dict_indices
                list_sud[dict_indices[key][0]]=key
                print 'In row ', i, " only position ", dict_indices[key][0], " has value ", key, " in its domain"
                print_sudoku(list_sud)
                show_domain(domain_dict)





def rule3_column(domain_dict, list_stud):
    if domain_dict == {}:
        domain_dict = update_domain(domain_dict, list_sud)

    for j in range(9):

        val_count = defaultdict(int)
        dict_indices = defaultdict(list)
        deleted_list=[]
        for i in range(9):
            if (i, j) in domain_dict:

                for val in domain_dict[i, j]:
                    val_count[val] += 1
                    dict_indices[val] += [(i, j)]



        for key, item in val_count.items():

            if (item == 1) and (dict_indices[key][0] not in deleted_list):
                if (j == 0):
                    print "I PREDICT THINGS ARE ABOUT TO BREAK"
                    print_sudoku(list_sud)
                    show_domain(domain_dict)
                deleted_list += [dict_indices[key][0]]
                del domain_dict[dict_indices[key][0]]
                #print dict_indices[key][0]
                list_sud[dict_indices[key][0]]=key
                print 'In col ', j, " only position ", dict_indices[key][0], " has value ", key, " in its domain", val_count
                print_sudoku(list_sud)
                show_domain(domain_dict)
                return



def rule3_box(domain_dict, list_stud):
    if domain_dict == {}:
        domain_dict = update_domain(domain_dict, list_sud)
    for i in [0,3,6]:
        for j in [0,3,6]:
            set_values = defaultdict(list)
            val_count = defaultdict(int)
            dict_indices = defaultdict(list)
            deleted_list =[]
            for i1 in range(i,i+3):
                for j1 in range(j,j+3):
                    if (i1, j1) in domain_dict:
                        for val in domain_dict[i1, j1]:
                            #print val
                            val_count[val] += 1
                            dict_indices[val] += [(i1, j1)]
            #print val_count
            #print dict_indices
            for key, item in val_count.items():
                if item == 1 and ( dict_indices[key][0] not in deleted_list):
                    deleted_list+=[dict_indices[key][0]]
                    del domain_dict[dict_indices[key][0]]
                    #print dict_indices[key][0]
                    list_sud[dict_indices[key][0]] = key
                    print 'In box ', i, " ", j, " only position ", dict_indices[key][0], " has value ", key, " in its domain"
                    print_sudoku(list_sud)
                    show_domain(domain_dict)
                    return

            #if i==3 and j==3:
                #print val_count
                #print dict_indices

































def constraint_propogation(domain_dict,list_sud,k):
    domain_dict = create_domain(domain_dict, list_sud)
    while 1:

        check =True
        #Applying Rule 1
        domain_dict = update_domain(domain_dict,list_sud)
        print 'Rule 1 domain dictionary has ', len(domain_dict)
        print_sudoku(list_sud)
        show_domain(domain_dict)

        #Applying Rule 2
        for key,value in domain_dict.items():
            if len(value)==1:
                check = False
                list_sud[key[0],key[1]]= value[0]
                print "At position ", key[0], ", ", key[1], " its domain only contains ", value[0]
                print 'After Rule 2 domain dictionary has ', len(domain_dict)
                print_sudoku(list_sud)
                show_domain(domain_dict)
                del domain_dict[key]
                domain_dict = update_domain(domain_dict, list_sud)
                break


        # #Applying Rule 3
        if(rule3_row(domain_dict,list_sud)): continue
        domain_dict = update_domain(domain_dict, list_sud)
        rule3_column(domain_dict,list_sud)
        domain_dict = update_domain(domain_dict, list_sud)
        rule3_box(domain_dict,list_sud)
        domain_dict = update_domain(domain_dict, list_sud)
        print 'After Rule 3 domain dictionary has ', len(domain_dict)

        #Applying Rule 4
        naked_triples_row(domain_dict,list_sud,k)
        domain_dict = update_domain(domain_dict, list_sud)
        naked_triples_column(domain_dict,list_sud,k)
        domain_dict = update_domain(domain_dict, list_sud)
        naked_triples_box(domain_dict, list_sud, k)
        domain_dict = update_domain(domain_dict, list_sud)
        print 'After Naked Triples domain dictionary has ', len(domain_dict)
        print_sudoku(list_sud)
        show_domain(domain_dict)


        #domain_dict=update_domain(domain_dict,list_sud)

        if check:
            if domain_dict=={}:
                return True

            else:
                show_domain(domain_dict)
                return solve_sudoku_search(list(list_sud),domain_dict)








def find_domain(l,list_sud,vals):

    x = l[0]; y = l[1]

    if x/3==0:
        x1=0 ; x2 = 3
    if x/3 == 1 :
        x1 = 3 ; x2 = 6
    if x/3 ==2 :
        x1 = 6 ; x2 =9
    if y/3==0:
        y1=0 ; y2 = 3
    if y/3 == 1 :
        y1 = 3 ; y2 = 6
    if y/3 ==2 :
        y1 = 6 ; y2 =9

    temp = set(vals).difference(set(list_sud[:,y]) | set(list_sud[x,:]) | set(np.unique(list_sud[x1:x2,y1:y2])  ) )
    return list(temp)










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
    return not used_in_row(list_sud, row, num) and not used_in_col(list_sud, col, num) and not used_in_box(list_sud, row - row % 3,
                                                                                                 col - col % 3, num)


def solve_sudoku_search(list_sud,domain_dict):
    # 'l' is a list variable that keeps the record of row and col in find_empty_location Function
    l = [0, 0]
    global back_tracking_count



    # If there is no unassigned location, we are done
    if (not find_empty_location(list_sud, l)):
        return True

    # Assigning list values to row and col that we got from the above Function
    row = l[0]
    col = l[1]
    #print l
    # consider digits 1 to 9
    #print domain_dict[(row,col)]
    for num in domain_dict[(row,col)]:

        if (check_location_is_safe(list_sud, row, col, num)):


            list_sud[row][col] = num


            if (solve_sudoku_search(list_sud,domain_dict)):
                return True

            list_sud[row][col] = 0

            back_tracking_count+=1


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

    #print data_dict
    for key in [27]:

        domain_dict={}

        print key

        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        list_sud =data_dict[key]
        print_sudoku(list_sud)
        back_tracking_count = 0
        k=3
        print key, constraint_propogation(domain_dict, list_sud,k), back_tracking_count
        print_sudoku(list_sud)
        print domain_dict
        # #naked_triples(domain_dict,list_sud,3)
        # #show_domain(domain_dict)
        # print 'None applied '
        # print_sudoku(list_sud)
        # #rule3_row(domain_dict,list_sud)
        # #print 'row'
        # #print_sudoku(list_sud)
        #
        # #rule3_column(domain_dict,list_sud)
        # #print 'column'
        # #print_sudoku(list_sud)
        # print 'box'
        # rule3_box(domain_dict,list_sud)
        # print_sudoku(list_sud)
        # #update_domain(domain_dict,list_sud)
        # #solve_sudoku_search(list_sud,domain_dict)
        # ##print key,constraint_propogation(domain_dict,list_sud), back_tracking_count
