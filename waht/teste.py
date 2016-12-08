aa = ['1', '2', '3','4','1','6','t','p','r']
bb = ['d','1', 'b', 'c', 'a','r']

print 'zip: ', zip(aa, bb)
print [a for a, b in zip(aa, bb) if a == b]
['b']

e = list(set(aa) & set(bb))
print 'e: ', e
if e == []:
    print 'e vazio'
else: print 'erro'