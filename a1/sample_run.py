from warehouse import *

if __name__ == '__main__':
    s = make_init_state([['prod1', (0,0)], ['prod2', (0,10)], ['prod3', (0, 20)]], 
                        [['pack1', (20,0)], ['pack2', (20,10)], ['pack3', (20,20)]],
                        0, 
                        [['prod1', 'pack1'], ['prod2', 'pack2'], ['prod3', 'pack3']], 
                        [['r1', 'on_delivery', (20,10), 14], 
                         ['r2', 'on_delivery', (20,20), 8], 
                         ['r3', 'on_delivery', (20,0), 8]])
    
    se = SearchEngine('astar', 'full')
    se.search(s, warehouse_goal_fn, heur_min_completion_time)
    se.set_strategy('breadth_first')
    se.search(s, warehouse_goal_fn)

'''
{
    (8,
        "[['r1', 'on_delivery', (20, 10), 14],
          ['r2', 'idle', (20, 20)],
          ['r3', 'idle', (20, 0)]]",
        "[['prod1', 'pack1'],
          ['prod2', 'pack2'],
          ['prod3', 'pack3']]",
        "[['prod1', (0, 0)],
          ['prod2', (0, 10)],
          ['prod3', (0, 20)]]",
        "[['pack1', (20, 0)],
          ['pack2', (20, 10)],
          ['pack3', (20, 20)]]"
    ): 8,
    
    (0,
        "[['r1', 'on_delivery', (20, 10), 14],
          ['r2', 'on_delivery', (20, 20), 8],
          ['r3', 'on_delivery', (20, 0), 8]]",
        "[['prod1', 'pack1'],
          ['prod2', 'pack2'],
          ['prod3', 'pack3']]",
        "[['prod1', (0, 0)],
          ['prod2', (0, 10)],
          ['prod3', (0, 20)]]",
        "[['pack1', (20, 0)],
          ['pack2', (20, 10)],
          ['pack3', (20, 20)]]"
    ): 0,

    (14,
        "[['r1', 'idle', (20, 10)],
          ['r2', 'on_delivery', (20, 20), 48, 38, 28],
          ['r3', 'on_delivery', (20, 0), 28, 38, 48]]",
        "[['prod2', 'pack2'],
          ['prod3', 'pack3']]",
        "[['prod1', (0, 0)],
          ['prod2', (0, 10)],
          ['prod3', (0, 20)]]",
        "[['pack1', (20, 0)],
          ['pack2', (20, 10)],
          ['pack3', (20, 20)]]"
    ): 14,

    (8,
        "[['r1', 'on_delivery', (20, 10), 14],
          ['r2', 'on_delivery', (20, 20), 48, 38, 28],
          ['r3', 'on_delivery', (20, 0), 28, 38, 48]]",
        "[['prod2', 'pack2'],
          ['prod3', 'pack3']]",
        "[['prod1', (0, 0)],
          ['prod2', (0, 10)],
          ['prod3', (0, 20)]]",
        "[['pack1', (20, 0)],
          ['pack2', (20, 10)],
          ['pack3', (20, 20)]]"
    ): 8, (8, "[['r1', 'on_delivery', (20, 10), 14], ['r2', 'on_delivery', (20, 20), 48, 38, 28], ['r3', 'on_delivery', (20, 0), 28, 38, 48]]", "[['prod1', 'pack1'], ['prod2', 'pack2']]", "[['prod1', (0, 0)], ['prod2', (0, 10)], ['prod3', (0, 20)]]", "[['pack1', (20, 0)], ['pack2', (20, 10)], ['pack3', (20, 20)]]"): 8, (8, "[['r1', 'on_delivery', (20, 10), 14], ['r2', 'on_delivery', (20, 20), 48, 38, 28], ['r3', 'on_delivery', (20, 0), 28, 38, 48]]", "[['prod1', 'pack1'], ['prod3', 'pack3']]", "[['prod1', (0, 0)], ['prod2', (0, 10)], ['prod3', (0, 20)]]", "[['pack1', (20, 0)], ['pack2', (20, 10)], ['pack3', (20, 20)]]"): 8}
'''
