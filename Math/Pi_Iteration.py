'''
Created on 15.10.2014

@author: David Artmann
'''
import decimal
from decimal import Decimal

accuracy = 120

def plouffBig(n): #http://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
    
    decimal.getcontext().prec = accuracy
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(1)/(16**k))*((Decimal(4)/(8*k+1))-(Decimal(2)/(8*k+4))-(Decimal(1)/(8*k+5))-(Decimal(1)/(8*k+6)))
        k += 1
    return pi

for i in xrange(1,201):
    print "Iteration number ",i, " ", plouffBig(i)
print "========================================="
print "Calculated Pi with an accuracy of "+str(accuracy)+" digits after the decimal point and "+str(i)+" iterations"