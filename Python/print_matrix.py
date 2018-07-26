"""
Neatly prints a 2D array. Can specify the format such
as 'e' and  'f'. Can also specify tailing digits as one 
would normally, e.g. '.3f'. If no (right aligned) width
is provided, the max string length amongst all elements 
is used. If this maximum is greater than the provided 
width, terms up till this length are 'sandwiched.'
"""
import numpy as np

def print_matrix(mtx, fmt='g', spc=None):
    # Slick string formatting
    xstr = lambda x, f: ('{:'+f+'}').format(x)
    
    # If width not given, set width to max char len
    if spc is None:
        xstr_len = lambda x, f: len(xstr(x, f))
        m_xstr_len = np.vectorize(xstr_len)
        spc = np.amax(m_xstr_len(mtx, fmt))
    
    # Print out matrix by rows with width and format
    for row in mtx:
        print(*[xstr(x, str(spc)+fmt) for x in row])

""" === Examples === 
>>> a = np.array([[   0,     1,    2],
                  [   1, 0.002,    3],
                  [   2,     3, 0.04],
                  [3e-1,     4, 5000]])
                  
>>> print_matrix(a)
    0     1     2
    1 0.002     3
    2     3  0.04
  0.3     4  5000
  
>>> print_matrix(a, 'e')
0.000000e+00 1.000000e+00 2.000000e+00
1.000000e+00 2.000000e-03 3.000000e+00
2.000000e+00 3.000000e+00 4.000000e-02
3.000000e-01 4.000000e+00 5.000000e+03

>>> print_matrix(a, 'f', 12)
    0.000000     1.000000     2.000000
    1.000000     0.002000     3.000000
    2.000000     3.000000     0.040000
    0.300000     4.000000  5000.000000
    
>>> print_matrix(a, '.2f', 0)
0.00 1.00 2.00
1.00 0.00 3.00
2.00 3.00 0.04
0.30 4.00 5000.00

"""
