import pandas as pd

if True:
    data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
            'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions',
                     'Lions', 'Lions'],
            'wins': [11, 8, 10, 15, 11, 6, 10, 4],
            'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
    football = pd.DataFrame(data)
    #print football['year']
   # print ''
    #print football[['year','wins','losses']]
    '''
    Row selection can be done through multiple ways.

    Some of the basic and common methods are:
       1) Slicing
       2) An individual index (through the functions iloc or loc)
       3) Boolean indexing

    You can also combine multiple selection requirements through boolean
    operators like & (and) or | (or)
    '''
   # print football.iloc[[0]]
    print ''
    print football.loc[[0]]
   # print football[3:5]
   # print football[:]
    print football[(football.wins>10) &(football.team == 'Packers')]