#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    constrains = []
    if not newVar:
        constrains = csp.get_all_cons()
    else:
        constrains = csp.get_cons_with_var(newVar)
    is_true = True      #output bool, default as True
    prune_list = []     #output prune_list
    
    for c in constrains:
        if c.get_n_unasgn() == 1:
            #unassigned constrain detected
            is_true = False     #This constrain may return False
            uv = c.get_unasgn_vars()[0]
            vals = []
            vars = c.get_scope()
            curr_index = 0;
            #construct the value list used to check constrain
            for var in vars:
                if var != uv:
                    vals.append(var.get_assigned_value())
                else:
                    vals.append(0)
                    uv_index = curr_index
                curr_index += 1
                
            #check all current values in the unassigned varible
            uvals = uv.cur_domain()
            for uval in uvals:
                vals[uv_index] = uval
                
                #if ckeck for this value is not passed:
                #prune it and add it to the prune list
                if not (c.check(vals)):
                    uv.prune_value(uval)
                    prune_list.append((uv, uval))
                    
                #if check for this value is passed:
                #change output bool to True so that the search would continue
                else:
                    is_true = True

                    
    return is_true, prune_list
        
        

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    prune_list = []
    if newVar == None:
        cq = csp.get_all_cons()
    else:
        cq = csp.get_cons_with_var(newVar)
    #start operating in constrain queue
    while cq != []:
        c = cq.pop(0)
        vars = c.get_scope()
        for var in vars:
            for d in var.cur_domain():
                prune_happened = False
                #prune not GAC values
                if not c.has_support(var, d):
                    var.prune_value(d)
                    prune_list.append((var, d))
                    prune_happened = True
                #If all values are pruned, return False
                if var.cur_domain() == []:
                    return False, prune_list
                #when prune_happened, all constrains related with this value should be checked
                #if any of this constrains not in queue, add it
                if prune_happened:
                    for another_c in csp.get_cons_with_var(var):
                        if not another_c in cq:
                            cq.append(another_c)
    return True, prune_list

