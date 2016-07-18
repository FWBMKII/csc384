#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def sudoku_csp_model_1(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''    
#IMPLEMENT
    i = 0
    dom = [1,2,3,4,5,6,7,8,9]
    #construct variables
    vars = []
    #get fixed points => these variables' domain have only one value
    i_index = 0
    
    fix_points = []
    for i in initial_sudoku_board:
        j_index = 0
        for j in i:
            if j != 0:
                fix_points.append((i_index, j_index, j))
            j_index += 1
        i_index += 1
    
    #construct all variables, set each variables' domain based on fixed points
    i_index = 0
    for i in initial_sudoku_board:
        j_index = 0
        #ban list of values in every variable in this row
        r_baned = [el[2] for el in fix_points if (el[0] == i_index)]
        for j in i:
            #ban list of values in every variable in this column
            c_baned = [el[2] for el in fix_points if (el[1] == j_index)]
            if j == 0:
                vars.append(Variable("({}, {})".format(i_index, j_index), dom))
                for val_index in range(9):
                    if (dom[val_index] in r_baned) or (dom[val_index] in c_baned):
                        vars[-1].curdom[val_index] = False
            else:
                vars.append(Variable("({}, {})".format(i_index, j_index), [j]))
            j_index += 1
        i_index += 1
    #ban fixed values in each small square
    for i in range(9):
        scope = get_square(vars, i)
        buf = []
        for var in scope:
            if len(var.domain()) == 1:
                buf.append(var.domain()[0])
        for var in scope:
            if len(var.domain()) != 1:
                cur_dom = var.cur_domain()
                for baned_val in buf:
                    if baned_val in cur_dom:
                        var.curdom[var.domain().index(baned_val)] = False
    
    #constructing constrains
    cons = []
    for i in range(9):
        #get the variable list representing ith row / column / square
        vars_row = vars[(i * 9) : ((i+1) * 9)]
        vars_col = []
        for j in range(9):
            vars_col.append(vars[i + (j * 9)])
        vars_sqr = []
        for j in range(3):
            vars_sqr.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 0])
            vars_sqr.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 1])
            vars_sqr.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 2])

        #construct constrains by each two variables in the same row
        for var_pair in itertools.combinations(vars_row, 2):
            con = Constraint("C-{}|{})".format(var_pair[0].name, var_pair[1].name), [var_pair[0], var_pair[1]])
            sat_tuples = []
            for t in itertools.product(var_pair[0].cur_domain(), var_pair[1].cur_domain()):
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        #construct constrains by each two variables in the same column
        for var_pair in itertools.combinations(vars_col, 2):
            con = Constraint("C-{}, {})".format(var_pair[0].name, var_pair[1].name), [var_pair[0], var_pair[1]])
            sat_tuples = []
            for t in itertools.product(var_pair[0].cur_domain(), var_pair[1].cur_domain()):
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        #construct constrains by each two variables in the same square
        for var_pair in itertools.combinations(vars_sqr, 2):
            con = Constraint("C-{}, {})".format(var_pair[0].name, var_pair[1].name), [var_pair[0], var_pair[1]])
            sat_tuples = []
            for t in itertools.product(var_pair[0].cur_domain(), var_pair[1].cur_domain()):
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
    
    #construct CSP      
    sudoku_csp = CSP("sudoku_mod1", vars)
    for c in cons:
        sudoku_csp.add_constraint(c)
    variable_array = []
    for i in range(9):
        variable_array.append(vars[(i * 9) : ((i+1) * 9)])
    wcnmb = BT(sudoku_csp)
    wcnmb.restore_all_variable_domains()
    return sudoku_csp, variable_array



##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''

#IMPLEMENT
    i = 0
    dom = [1,2,3,4,5,6,7,8,9]
    #construct variables
    vars = []
    #get fixed points => these variables' domain have only one value
    i_index = 0
    
    fix_points = []
    for i in initial_sudoku_board:
        j_index = 0
        for j in i:
            if j != 0:
                fix_points.append((i_index, j_index, j))
            j_index += 1
        i_index += 1
    
    print("ban var finished...")
    #construct all variables, set each variables' domain based on fixed points
    i_index = 0
    for i in initial_sudoku_board:
        j_index = 0
        #ban list of values in every variable in this row
        r_baned = [el[2] for el in fix_points if (el[0] == i_index)]
        for j in i:
            #ban list of values in every variable in this column
            c_baned = [el[2] for el in fix_points if (el[1] == j_index)]
            if j == 0:
                vars.append(Variable("({}, {})".format(i_index, j_index), dom))
                for val_index in range(9):
                    if (dom[val_index] in r_baned) or (dom[val_index] in c_baned):
                        vars[-1].curdom[val_index] = False
            else:
                vars.append(Variable("({}, {})".format(i_index, j_index), [j]))
            j_index += 1
        i_index += 1
    #ban fixed values in each small square
    for i in range(9):
        scope = get_square(vars, i)
        buf = []
        for var in scope:
            if len(var.domain()) == 1:
                buf.append(var.domain()[0])
        for var in scope:
            if len(var.domain()) != 1:
                cur_dom = var.cur_domain()
                for baned_val in buf:
                    if baned_val in cur_dom:
                        var.curdom[var.domain().index(baned_val)] = False
                    
                    
            
    print("cosntruct var finished...")
    #construct constrains
    cons = []
    #construct constrains representing each row
    for i in range(9):
        con = Constraint("C Row{}".format(i), vars[(i * 9) : ((i+1) * 9)])
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        if i == 0:
            print(nmb[0])
            print(nmb[1])
            print(nmb[2])
            print(nmb[3])
            print(nmb[4])
            print(nmb[5])
            print(nmb[6])
            print(nmb[7])
            print(nmb[8])
            print("Constrain", i, " --- ",sat_tuples)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("row finished...")
    #construct constrains representing each row
    for i in range(9):
        scope = []
        for j in range(9):
            scope.append(vars[i + (j * 9)])
        con = Constraint("C Col{}".format(i), scope)
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        print("Constrain", i, " --- ",len(sat_tuples))
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("col finished...")  
    #construct constrains representing each row
    for i in range(9):
        scope = get_square(vars, i)
        '''
        for j in range(3):
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 0])
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 1])
            scope.append(vars[(9 * 3 * int(i / 3)) + (3 * (i % 3)) + (9 * j) + 2])
        '''
        con = Constraint("C sqr{}".format(i), scope)
        sat_tuples = []
        nmb = []
        for var in con.scope:
            nmb.append(var.cur_domain())
        for t in itertools.product(nmb[0], nmb[1], nmb[2], nmb[3], nmb[4], nmb[5], nmb[6], nmb[7], nmb[8]):
            if len(set(t)) == 9:
                sat_tuples.append(t)
        print("Constrain", i, " --- ",len(sat_tuples))
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    print("sqr finished...")   
    #construct CSP  
    sudoku_csp = CSP("sudoku_mod2", vars)
    for c in cons:
        sudoku_csp.add_constraint(c)
    variable_array = []
    for i in range(9):
        variable_array.append(vars[(i * 9) : ((i+1) * 9)])
    wcnmb = BT(sudoku_csp)
    wcnmb.restore_all_variable_domains()
    print("all done...")
    return sudoku_csp, variable_array

def get_square(vars, n):
    if n == 0:
        s = 0
    if n == 1:
        s = 3
    if n == 2:
        s = 6
    if n == 3:
        s = 27
    if n == 4:
        s = 30
    if n == 5:
        s = 33
    if n == 6:
        s = 54
    if n == 7:
        s = 57
    if n == 8:
        s = 60
        
    ss = s + 9
    sss = ss + 9
    return [vars[s], vars[s + 1], vars[s + 2],
            vars[ss], vars[ss + 1], vars[ss + 2],
            vars[sss], vars[sss + 1], vars[sss + 2]]

'''
def cnmb(vars):
    cnmb_helper(output, vars, 0)
    return output

def cnmb_helper(output, vars, index):
    if index == 8:
        return
    else:
'''
