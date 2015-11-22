# Jeff Algorithm Notes

## 0. Introduction

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

## 1. Recursion

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

 * algorytm rekonstruujący drzewo binarne mając jego preorder i postorder (proste rekurencyjnie)
 * mamy kratkę o wielkości 2^n x 2^n z usuniętym jednym kwadracikiem (w dowolnym miejscu, udowodnić że każda taka kratka może zostać wypełniona puzzlami w kształcie 'L'
 * algorytm do liczenia inwersji w tablicy w czasie O(n log n) (modyfikacja mergesortu)

## 2. Fast Fourier Transforms

Reprezentacje wielomianów vs złożoność operacji:
| representation  |  evaluate  | add        | multiply   |
| coefficients    | O(n)       | O(n)       | O(n^2)     |
| roots + scale   | O(n)       | impossible | O(n)       |
| samples         | O(n^2)     | O(n)       | O(n)       |

Chcemy szybkich algorytmów konwesji z coefficients do samples i z powrotem.

Trywialnie można konwertować coefficients->samples za pomocą obliczenia wielomianu (koszt O(n^2)), a z powrotem za pomocą formuły lagrange'a (koszt O(n^3) używając naiwnych algorytmów mnożenia/dodawania)
Ale jeśli zahardcodujemy pozycje sampli w algorytm, możemy wykonać konwersję samples->coefficients w czasie O(n^2)

## Szybkie mnożenie wielomianów

Każdy wielomian stopnia n-1 można zapisać jako kombinację dwóch wielomianów stopni (n/2)-1:

P(x) = P_even(x^2) + x * P_odd(x^2)

Definiujemy zbiór X jako collapsible, jeśli zachodzi jedna z dwóch własności:
* X ma jeden element
* Zbiór X^2 = {x^2 for x in X} ma dokładnie n/2 elementy i jest collapsing

Widać że mając dowolny zbiór collapsible możemy obliczyć {p(x) for x in X}:
* rekurencyjnie oblicz P_even(x^2)
* rekurencyjnie oblicz P_odd(x^2)
* dla każdego x oblicz P(x) = P_even(x^2) + x * P_odd(x^2)

Widać że czas wykonywania tego algorytmu to O(n log n)

Pomysł żeby wykorzystać pierwiastki jedności (Cooley, Tukeys), zakłada że n jest potęgą dwójki:

def fft(array):
    n = len(array)
    if n == 1:
        return array
    even, odd = [0] * (n/2), [0] * (n/2)
    for j in range(n/2):
        even[j], odd[j] = array[2*j], array[2*j + 1]
    even1, odd1 = fft(even), fft(odd)
    w, w_step = 1, cos(2pi/n) + i*sin(2pi/n)
    result = [0] * n
    for j in range(n/2):
        result[j] = even[j] + w * odd[j]
        result[j + n/2] = even[j] - w * odd[j]
        w = w * w_step
    return result

Algorytm do inverse FFT jest bardzo, bardzo podobny - jedyne co, to w_step trzeba zmienić na cos - sin (zamiast cos + sin)
