"""
TREE-ish
    import_test/
    │   modA.py
    │       >> func()
    │       >> A(x).func()
    │
    └───deeper/
            modB.py
                >> Alphabet(x)
                >> Alphabet.sm()

>>> import import_test.modA
>>> import_test.modA.func()
'something'
>>> import_test.modA.A(5)
<import_test.modA.A object at 0x0000000001FFAEB8>
>>> import_test.modA.A(5).func()
5
>>> import import_test.deeper.modB
>>> import_test.deeper.modB.Alphabet.sm()
I am always here
'I am always here'
"""
