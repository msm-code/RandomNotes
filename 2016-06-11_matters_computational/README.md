# MATTERS COMPUTATIONAL

## 1. Low Level Algorithms

## 2. Combinatorial Generation

## 3. Fast Transforms

## 4. Fast Arithmetic

## 5. Algorithms For Finite Fields

### 5.1. Modular Arithmetics And Some Number Theory

**Implementation of arithmetic operations**
 - Dodawanie/odejmowanie w pierścieniu modulo m -> trywialne
 - Mnożenie jest trywialne, ale ciekawa rzecz zachodzi jeśli się chcey przejmować czymś takim jak wielkośc słowa
      maszynowego - przy naiwnym (a*b)%m ograniczamy się do połowy wielkości słowa, a można to zrobić inaczej:    
      ```c
      uint64_t mod_mul(uint64_t a, uint64_t b, uint64_t m) {
        uint64_t y = (uint64_t)((double)a*(double)b/m + 1.0/2.0);  // floor(a*b/m)
        y *= m;
        uint64_t x = a * b;
        uint64_t r = x - y;
        if ((int64_t)r < 0) {
          r += m;
          y -= 1;
        } 
        return r;
      ```
        
      Ten algorytm korzysta z tego że `a*b` na intach wylicza najniższe bity wyniku, a `a*b` na floatach - najwyższe
  - Potęgowanie - algorytm szybkiego potęgowania, dość proste. Ale w razie potrzeby:
      ```c
      uint64_t mod_pow(uint64_t a, uint64_t e, uint64_t m) {
        uint64_t z = a;
        uint64_t y = 1;
        while (e != 0) {
          if (e & 1) {
            y = (y * z) % m;
          }
          e >>= 1;
          z = (z * z) % m;
        }
        return y;
      }
      ```
  - Division and modular inversion - dzielenie trywialne mając odwrotność, a odwracanie proste, ale mozna zapisać.
      Napisałem małą ale śmieszną implementację używając struktur jak krotek (niezbyt wydajna pewnie):
      ```c
      struct egcd_result { uint64_t g, y, x; };
      struct egcd_result egcd(uint64_t a, uint64_t b) {
        if (a == 0) {
          struct egcd_result result = { b, 0, 1 };
          return result;
        } else {
          struct egcd_result r = egcd(b % a, a);
          struct egcd_result result = { r.g, r.x - (b / a) * r.y, r.y };
          return result;
        }
      }
      ``` 
      Mając egcd napisanie modinva jest trywialne - modinv n to po prostu x % m z egcd(n, m);
  - Redukcja jest szczególnie prosta przy mersenne primes (`M = 2^k - 1`). Wtedy jeśli `u*v = 2^k*r + s`
      to można zredukować `u*v === r+s (mod M)`.
  - Algorytm redukcji używający jedynie przesunięć bitowych, dodawań i odejmowań istnieje dla dowolnych structured
      primes, zwanych również generalised mersenne primes - jeśli M jest postaci `M = Sum[i=0..n](m_i * x^i)`
      gdzie `x = 2^k`, `m_n = 1`, `m_i = +-1` i `m_(n-1) = -1`.
   - Sito Eratostenesa - algorytm na tyle nudny że mi sie go nie chce implementować. Fun pomysł - algorytm ten można
      dowolnie optymalizować, przez hardkodowanie pętli na małe liczby pierwsze na początku (albo jeszcze lepiej - nie
      umieszczenie ich w docelowej tablicy). Klasyczne jest robienie tego dla liczby 2. Ciekawe byłoby uogólnienie
      tego i napisanie wersji z "hardkodowanymi" pierwszymi N liczbami pierwszymi.
   - Chineese Remainder Theorem (CRT) - mamy m1, m2 ... mn które są względnie pierwsze. I teraz jeśli `x === xi mod mi`
      to x istnieje i jest unikalne w przedziale `0 <= x < m1*m2*...*mn`.
      Pozwala to na liczenie rzeczy modulo M przez podzielenie liczby na kilka kawałków i połączenie ich używając CRT.
      Dla dwóch wartości łatwo to wyliczyć:
      ```python
      def crt2(x1, m1, x2, m2):
        s = ((x2 - x1)*invmod(m1, m2)) % m2
        return x1 + s * m1
      ```
      Dla wielu wartości można użyć pewnego mądrego algorytmu który kiedyś widziałem, ale można po prostu powtarzać
      ten sam algorytm wielokrotnie:
      ```python
      def crt(pairs):
        x, m = pairs[0]
        for x1, m1 in pairs[1:]:
          x, m = crt2(x, m, x1, m1), m*m1
        return x, m
      ```
  - Rząd elementu (multiplicative order) zapisywany jako ord(a) to najmniejsza liczba r że zachodzi `a^r = 1`. Dla
      elementów bez odwrotności (gcd(a, m) != 1) ord jest niezdefiniowany. Element a taki że `a^r == 1` jest nazywany
      r-tym pierwiastkiej jedności. Maksymalny rząd R(m) to największy z rzędów dla wszystkich elementów dla
      ustalonego m. Jeśli p jest liczbą pierwszą, R(p) = p-1. Jeśli element nie ma maksymalnego rzędu r, czasami nazywa
      się współczynnik którego mu brakuje jako index - tzn. `i*r = R`.
      Koncept rzędu pochodzi z teorii grup. Odwracalne elementy modulo m z mnożeniem tworzą grupę (multiplicative
      group). Z dodawaniem też, tam większość rzeczy jest prostsza.
      
     
 