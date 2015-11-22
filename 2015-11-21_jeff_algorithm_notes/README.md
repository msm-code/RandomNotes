# Jeff Algorithm Notes

## Introduction

### Algorytm mnożenia xxx chłopów

```python
def PeasantMultiply(x, y):
    product = 0
    while x > 0:
        if x % 2 == 1:
            product += y
        x = x // 2
        y *= 2
    return product
```

## Recursion

### Magiczne piątki
```python
def MedianSelect(array, k): # magiczne piątki
    if len(array) <=  25: # jakaś stała
        return sorted(array)[k] # bruteforce
    else:
        m = (n+4)/n # zaokrąglone w górę n/5
        medarray = [0] * m
        for i in range(m):
            medarray = MedianSelect(array[5*i:5*i+5], 3)
        mom = MedianSelect(medarray, m/2)
        r = Partition(array, mom)
        if k < r:
            return MedianSelect(array[:r], k)
        else if k > r:
            return MedianSelect(array[r+1:], k-r)
        else:
            return mom
```

Może niezbyt praktyczny, ale ciekawy algorytm, wyszukiwanie mediany w tablicy w czasie O(n)

Można zauważyć że czas algorytmu spełnia równanie:
T(n) <= O(n) + T(n/5) + T(7n/10)

A z tego wynika T(n) = O(n)

### Karatsuba multiply

Trzeba zauważyć własność że możemy podzielić liczby a i b jako

    a = ah * 10^n + al
    b = bh * 10^n + bl

    a*b = (ah * bh)*10^{2n} + (ah*bl + al*bh)*10^n + al*bl  

I teraz sztuczka - można to wyżej zapisać inaczej zauważając że:

    ac + bd - (a - b)(c - d) = bc + ad

Czyli ostateczna forma wzoru to:

    a*b = (ah * bh)*10^{2n} + (al*bl + ah*bh - (al - ah)(bl - bh))*10^m + al*bl

To mnożenie ma już czas O(n^log(3)). 

Możemy podzielić liczbę na więcej fragmentów i będzie szybciej. Rozwinięcie tego pomysłu to fast fourier transform, bardziej skomplikowany algorytm który pozwala pomnożyć dwie liczby w czasie n log n.

### Ciekawe ćwiczenia:

 - algorytm rekonstruujący drzewo binarne mając jego preorder i postorder
