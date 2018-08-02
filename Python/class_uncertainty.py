"""
Class structure for using values with uncertainties.
Class currently overloads: + - * / ** exp
"""
import math
import numpy as np
import tableprint as tp
from math import sqrt, log, sin, cos

# If the input doesn't have uncertainty, make it zero
def vu_cast(x):
    if type(x) is not val_uncert:
        x = val_uncert(x, 0.0)
    return x
   
# Calculate e^x and uncertainty   
def exp(x):
    x  = vu_cast(x)
    u  = math.exp(x.val)
    du = u*x.uncert
    return val_uncert(u, du)
            
class val_uncert(object):
    # Define the object's value and uncertainty on initialization
    def __init__(self, val, uncert):
        self.val    = val
        self.uncert = uncert   
        
    # Absolute uncertainty for addition and subtraction (dU)    
    def du_addsub(self, a, b): 
        da = a.uncert
        db = b.uncert
        return sqrt(da*da + db*db)
    
    # Relative uncertainty for multiplication and division (dU/U)  
    def rel_du_muldiv(self, a, b): 
        da_a = a.uncert / a.val
        db_b = b.uncert / b.val
        return sqrt(da_a*da_a + db_b*db_b)
        
    # Define basic math operations (returns class,  U and dU)
    def __add__(self, other):
        other = vu_cast(other)
        u = self.val + other.val
        return val_uncert(u, self.du_addsub(self, other))

    def __sub__(self, other):
        other = vu_cast(other)
        u = self.val - other.val
        return val_uncert(u, self.du_addsub(self, other))

    def __mul__(self, other):
        other = vu_cast(other)
        u = self.val * other.val
        return val_uncert(u, u * self.rel_du_muldiv(self, other))

    def __truediv__(self, other):
        other = vu_cast(other)
        u = self.val / other.val
        return val_uncert(u, u * self.rel_du_muldiv(self, other))
    
    def __pow__(self, other):
        other = vu_cast(other)
        a, da = (self.val,  self.uncert)
        b, db = (other.val, other.uncert)
        u  = self.val**other.val
        du = u * sqrt( (da*b/a)**2 + (db*log(a))**2 )
        return val_uncert(u, du)
        
    # Reverse operations to account for left incompatible   
    def __radd__(self, other):
        return vu_cast(other) + self
        
    def __rsub__(self, other):
        return vu_cast(other) - self
        
    def __rmul__(self, other):
        return vu_cast(other) * self
        
    def __rtruediv__(self, other):
        return vu_cast(other) / self
        
    def __rpow__(self, other):
        return vu_cast(other) ** self
        
    # String the value and uncertainty    
    def __str__(self):
        return "( " + str(self.val) + ", " + str(self.uncert) + ")"
    
# Check uncertainty class system using a few preselected values 
def demo_class():
    print("Below are tables validating operation,. Second table")
    print("involves an int or float, in both operation orders.")
    a = val_uncert(1, 0.5)
    b = val_uncert(3, 1.2)
    c = val_uncert(3, 2.0)
    tp.table(width=[8, 8, 12], 
        headers=[' ','Value','Uncertainty'], 
        data=[['      a',         a.val,         a.uncert],
              ['      b',         b.val,         b.uncert], 
              ['    a+b',     (a+b).val,     (a+b).uncert], 
              ['    a-b',     (a-b).val,     (a-b).uncert], 
              ['    a*b',     (a*b).val,     (a*b).uncert], 
              ['    a/b',     (a/b).val,     (a/b).uncert], 
              ['    b/a',     (b/a).val,     (b/a).uncert], 
              ['   a**b',    (a**b).val,    (a**b).uncert], 
              ['  exp(a)',  (exp(a)).val,  (exp(a)).uncert], 
              ['(a+b)-b', ((a+b)-b).val, ((a+b)-b).uncert], 
              ['(a*b)/b', ((a*b)/b).val, ((a*b)/b).uncert]])
    tp.table(width=[8, 8, 12], 
        headers=[' ','Value','Uncertainty'], 
        data=[['      c',         c.val,         c.uncert],
              ['    4+c',     (4+c).val,     (4+c).uncert], 
              ['    c+4',     (c+4).val,     (c+4).uncert],
              ['    4-c',     (4-c).val,     (4-c).uncert], 
              ['    c-4',     (c-4).val,     (c-4).uncert],
              ['    4*c',     (4*c).val,     (4*c).uncert], 
              ['    c*4',     (c*4).val,     (c*4).uncert],
              ['    4/c',     (4/c).val,     (4/c).uncert], 
              ['    c/4',     (c/4).val,     (c/4).uncert],
              ['   4**c',    (4**c).val,    (4**c).uncert], 
              ['   c**4',    (c**4).val,    (c**4).uncert]])
              
              
# ------------------------------------
#  Main Execution Space
# ------------------------------------

def main():
    demo_class()
    
if __name__== "__main__":
  main()

""" === Example ===
>>> demo_class()
Below are tables validating operation,. Second table
involves an int or float, in both operation orders.
╭──────────┬──────────┬──────────────╮
│          │  Value   │ Uncertainty  │
├──────────┼──────────┼──────────────┤
│        a │        1 │          0.5 │
│        b │        3 │          1.2 │
│      a+b │        4 │          1.3 │
│      a-b │       -2 │          1.3 │
│      a*b │        3 │       1.9209 │
│      a/b │  0.33333 │      0.21344 │
│      b/a │        3 │       1.9209 │
│     a**b │        1 │          1.5 │
│   exp(a) │   2.7183 │       1.3591 │
│  (a+b)-b │        1 │       1.7692 │
│  (a*b)/b │        1 │      0.75498 │
╰──────────┴──────────┴──────────────╯
╭──────────┬──────────┬──────────────╮
│          │  Value   │ Uncertainty  │
├──────────┼──────────┼──────────────┤
│        c │        3 │            2 │
│      4+c │        7 │            2 │
│      c+4 │        7 │            2 │
│      4-c │        1 │            2 │
│      c-4 │       -1 │            2 │
│      4*c │       12 │            8 │
│      c*4 │       12 │            8 │
│      4/c │   1.3333 │      0.88889 │
│      c/4 │     0.75 │          0.5 │
│     4**c │       64 │       177.45 │
│     c**4 │       81 │          216 │
╰──────────┴──────────┴──────────────╯
"""
