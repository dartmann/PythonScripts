'''
Created on 15.10.2014

@author: David Artmann
'''
import sys
sys.setrecursionlimit(10000)

def ack1(M, N):
    return (N + 1) if M == 0 else (
      ack1(M-1, 1) if N == 0 else ack1(M-1, ack1(M, N-1)))
   
print "Ackermann(3,7): " + str(ack1(3,7))
print "Ackermann(3,8): " + str(ack1(3,8))
print "Ackermann(3,9): " + str(ack1(3,9))
print "Ackermann(4,0): " + str(ack1(4,0))