'''
Created on 16.10.2014

@author: David Artmann
'''
num = 10000000
print "Computing from first till "+str(num)+" prime..."
def prime(n):
    def z(x):
        if x :return True
        return False
    num1=range(0,n+1); num2=int(n**0.5) +1
    for k in range(2,num2):
        num0=range(k,n+1,k);del num0[0]     
        for i in num0:
            num1[i]=0
    return filter(z, num1)

print prime(num)[-1]