import numpy as np
from math import sqrt


# ------------------------------------
#  Function Space
# ------------------------------------
    
# Check uncertainty class system using a few preselected values 
def check_class():
    a = val_uncert( 9, 3)
    b = val_uncert(16, 4)
    tp.table(width=[8, 8, 12], 
        headers=[' ','Value','Uncertainty'], 
        data=[['      a',         a.val,         a.uncert],
              ['      b',         b.val,         b.uncert], 
              ['    a+b',     (a+b).val,     (a+b).uncert], 
              ['    a-b',     (a-b).val,     (a-b).uncert], 
              ['    a*b',     (a*b).val,     (a*b).uncert], 
              ['    a/b',     (a/b).val,     (a/b).uncert], 
              ['    b/a',     (b/a).val,     (b/a).uncert], 
              ['(a+b)-b', ((a+b)-b).val, ((a+b)-b).uncert], 
              ['(a*b)/b', ((a*b)/b).val, ((a*b)/b).uncert]])
    

# ------------------------------------
#  Class Space
# ------------------------------------

class val_uncert(object):
    # Define the object's value and uncertainty on initialization
    def __init__(self, val, uncert):
        self.val    = val
        self.uncert = uncert   
        
    # Calculates the absolute uncertainty for addition and subtraction (dU)    
    def uncert_addsub(self, a, b): 
        da = a.uncert
        db = b.uncert
        return sqrt(da*da + db*db)
    
    # Calculates the relative uncertainty for multiplication and division (dU/U)  
    def uncert_muldiv(self, a, b): 
        da_a = a.uncert / a.val
        db_b = b.uncert / b.val
        return sqrt(da_a*da_a + db_b*db_b)
        
    # Define basic math operations (returns class,  U and dU)
    def __add__(self, other):
        sum = self.val + other.val
        return val_uncert(sum, self.uncert_addsub(self, other))

    def __sub__(self, other):
        dif = self.val - other.val
        return val_uncert(dif, self.uncert_addsub(self, other))

    def __mul__(self, other):
        mul = self.val * other.val
        return val_uncert(mul, mul*self.uncert_muldiv(self, other))

    def __truediv__(self, other):
        div = self.val / other.val
        return val_uncert(div, div*self.uncert_muldiv(self, other))
        
    # Returns a string array of a class with n decimal points (for things like print)
    def strE(self, nv, nu):
        s = "%." +str(nv)+ "E  %." +str(nu)+ "E"
        return s%(self.val, self.uncert)

        
# ------------------------------------
#  Main Execution Space
# ------------------------------------

def main():
    check_class()
    
    
  
if __name__== "__main__":
  main()
