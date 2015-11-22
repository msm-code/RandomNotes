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

```python
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
```

Algorytm do inverse FFT jest bardzo, bardzo podobny - jedyne co, to w_step trzeba zmienić na cos - sin (zamiast cos + sin)

## 3. Backtracking
## 4. Efficient exponential-time algorithms

Fun fact o maximum independent set size - computer generated algorithm wykonujący sie w czasie O(2^n/4) == O(1.1889^n) - sam opis algorytmu wymaga 15 stron.

## 5. Dynamic programming

### Memoizacja, etc

### Fibonacci
Bardzo fajny (chociaż dość trywialny) fakt:
    [0 1][x] = [x]
    [1 1][y] = [x+y]

Więc mnożąc przez M^n otrzymujemy ten sam efekt co iterując pętlą n razy.
A jesteśmy w stanie szybko (log n) podnieść macierz do potęgi M^n dzięki fast exp.

Swoją drogą ten algorytm (obliczanie fibonacciego macierzą) ma interesujące rozszerzenia jeśli zwiększymy macierz - pozwala obliczać inne podobnie iterowane funkcje zawierające w sobie np. sumę poprzednich elementów etc.

### Longest increasing subsequence

Algorytm ten sam co dla wykładniczego rozwiązania, ale tym razem z memoizacją czas wykonania spada do kwadratowego.
Można go zaimplementować ze złożonością przestrzenną O(n) trzymając tylko dwa najnowse wiersze macierzy

### Advanced Dynamic Programming Tricks

* Saving space - Hirschberg's divide and conquer trick

Prosty sposób to sliding window (używany np. przy LIS)
Niestety, w ten sposób traci się możliwość rekonstrukcji samego LIS, a poznaje sie tylko długośc.
Ale da się to zrobic w space O(m+n) i czasie O(mn), trzymając nie tylko edit distance dla każdej pary prefixów, ale też pozycję w optimal edting sequence dla tego prefiksu.

Konkretnie każda optymalna editing sequence zmieniająca A[1..m] w B[1..n] może zostać podzielona na dwa mniejsze editing sequences, jedną tranformującą `A[1...m/2]` w `B[1..h]` (dla jakieoś h), oraz drugą transformującą A[m/2 + 1..m] w B[h + 1..n].
Żeby obliczyć ten punkt h, definiujemy drugą funkcję Half(i, j) taką że pewna optymalna edit sekwencja z A[1..i] do B[1..j] zawiera optymalną edit sequence z A[1..m/2] do B[1..Half(i, j)].

Można zdefiniować half(i, j) rekurencyjnie:

```python
def half(i, j):
    if i < m/2:
        return infinity
    elif i == m/2:
        return j
    elif i > m/2 and edit(i, j) == edit(i - 1, j) + 1:
        return half(i - 1, j)
    elif i > m/2 and edit(i, j) == edit(i, j - 1) + 1
        return half(i, j - 1)
    else:
        return half(i - 1, j - 1)
```

(Może być więcej niż jedno optymalne rozwiążanie, więc to nie jedyna poprawna definicja).

Ta sztuczka może zostać zastosowana do (prawie) każdego problemu gdzie użyte jest dynamic programming.
(TODO napisać troche więcej/zaimplementować etc)

* Saving space - sparseness 

Można obliczyć LCS za pomocą listy match pointów, i w zasadzie wychodzi nawet szybciej niż pełnym dynamikiem O(m log m + n log n + K) (gdzie K to ilość match pointów)

* Saving time - monotonicity

Przykład - optimal binary tree. Prosty dynamiczny algorytm rozwiązuje ten problem w czasie O(n^3).

Tak jak w przypadku common subsequence problem, ten algorytm może zostać poprawiony przez wykorzystanie struktury w tabeli memoizacji:

    OptRoot[i, j-1] <= OptRoot[i, j] <= OptRoot[i+1, j]

## 7. Greedy Algorithms

### Storing files on tape

Mamy n plików każdy o wielkości l[i], chcemy je zapisać na taśmie. Dostęp do cpliku j jest równy sum(l[i] for i in range(j)) (sumie długości plików wcześniej). Jak to zrobić żeby zminimalizować koszt odczytów? Można zachłannie:

* jeśli każdy plik ma taką samą szansę być czytanym, posortować pliki po l[i]
* jeśli każdy plik ma taką samą długośc, ale różną częstotliwość czytania (w tablicy freq[i] ilość spodziewanych odczytań pliku i), posortować po freq
* jeśli oba sie różnią, posortować po freq/length

### Scheduling Classes

Posortować po czasie zakończenia i zachłannie.

### Huffman Codes

## 8. Matroids

Matroid M to skończona kolekcja skończonych zbiorów spełniających trzy aksjomaty:
* Non-emptiness: (Pusty zbiór jest w M)
* Heredity: jeśli X jest elementem M, to każdy podzbiór X jest w M
* Exchange: jeśli X i Y są dwoma zbiorami w M i |X| > |Y| to istnieje element x \in (X - Y) taki że Y + {x} jest w M.

Zbiory w M są nazywane zazwyczaj jako independent sets. Unia wszystkich zbiorów jest nazywana ground set. Independent set jest bazą jeśli nie jest podzbiorem żadnego innego independent set. Z exchange property wynika że wszystkie bazy mają taka samą licznośc. Rank podzbioru X to wielkość największego niezależnego podzbioru X.

Większość terminologii wynika stąd że oryginalny przykład to był linear matroid - macierz n x m. Inne przykłady to:
* uniform matroid
* graphic/cycle matroid
* cographic/cocycle matroid
* matching matroid
* disjoint path matroid

Matroid optimization problem:

```python
def greedy_basis(matroid, weights):
    ground_set = union(matroid)
    ground_set = sorted(ground_set, key=lambda x: weight[x])
    result = set([])
    for i in range(len(ground_set)):
        if matroid.contains(ground_set.union(set([ground_set[i]]))):
            result.insert(ground_set[i])
    return result
```
