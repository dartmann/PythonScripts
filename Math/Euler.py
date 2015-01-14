'''
Created on 16.10.2014

@author: David Artmann
'''
import decimal
from decimal import Decimal

accuracy = 120
terms = 1000
print "Calculating Euler's number with accurary of "+str(accuracy)+" digits and "+str(terms)+" terms..."

def main(): 
    decimal.getcontext().prec = accuracy
    num = Decimal(1000)
    fact = Decimal(1.0) 
    term = Decimal(0.0)
    power = Decimal(0.0)
    
    for i in range(1, num+1): 
        fact = fact*i 
        for j in range(i): 
          term = term + (Decimal(1.0) / fact) 
          
    print term 
main()