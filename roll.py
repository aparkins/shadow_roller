# Simple collection of functions intended for rolling dice per rules of Shadowrun RPG

import random

def roll():
    return random.randint(1, 6)

def multiRoll(n):
    return [ roll() for i in range(n) ]

def explodeRoll(prev=None):
    if prev is None:
        prev = []
    
    r = roll()
    if r < 6:
        return prev + [r]
   
    return explodeRoll(prev + [r])

def multiExplodeRoll(n):
    return [ subroll for i in range(n) for subroll in explodeRoll() ]

def initiative(b, n):
    return b + sum(multiRoll(n))

def shadowRoll(n, l=None):
    rolls = multiRoll(n)
    successes = len([ r for r in rolls if r >= 5 ])
    ones = len([ r for r in rolls if r == 1 ])
    if l is not None:
        successes = min(successes, l)
    return (successes, ones >= (len(rolls) / 2))

def pushTheLimit(n):
    rolls = multiExplodeRoll(n)
    successes = len([ r for r in rolls if r >= 5 ])
    glitch = False # cannot glitch an edge roll
    return (successes, glitch)

def multiShadowRolls(k, n, l=None):
    return [ shadowRoll(n, l) for i in range(k) ]

def multiPushedRolls(k, n):
    return [ pushTheLimit(n) for i in range(k) ]

def genRolls(c, k, n, l=None):
    results = [ sorted(multiShadowRolls(k, n, l), key=rollKey) for i in range(c) ]
    return [ [ printRoll(r) for r in rs ] for rs in results ]

def genPushedRolls(c, k, n):
    results = [ sorted(multiPushedRolls(k, n), key=rollKey) for i in range(c) ]
    return [ [ printRoll(r) for r in rs ] for rs in results ]

def rollKey(r):
    k = r[0]
    if r[1]:
        k -= 0.5
    return k

def printRoll(r):
    res = '{}'.format(r[0])
    if r[1]:
        res += '!'
    return res
