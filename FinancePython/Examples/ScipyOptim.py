
from scipy.optimize import minimize

def f(x):
    
    return x[0]**2+x[1]**2 + 4

res = minimize(f, x0 =[2,1], tol =0.00001)

print res

par = res.x
print par