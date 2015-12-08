# Coursera cryptography

Symmetric Ciphers:
A i B znają (ten sam) klucz k. A szyfruje wiadomość za pomocą k, D deszyfruje za pomocą tego samego keya k

Discrete probability:
U - finite set (np. {0, 1}^n)
Probability distribution - funkcja `P: U -> [0, 1]`
Wymagania: sum[x \in U] P(x) = 1. (prawdopodobieństwa sumuję sie do 1)

Przykłady:
Uniform distribution (dla każdego x, `P(x) = 1/|U|`)
Point distribution `P(x0) = 1, P(x != x0) = 0`

Events:
dla zbioru `A \in U Pr(A) = Sum[x \in A](P(X))`

## Lesson 1.5
Union bound:
Pr(A | B) <= Pr(A) + Pr(B)
Pr(A | B) = Pr(A) + Pr(B) - Pr(A & B)

Random variable X -> funkcja X: U -> V.
Random variable induces distribution.

Uniform random variable r -> dla każdego a \in U, Pr[r = a] = 1 / |U|. Formalnie r = r(x) = x.

Randomized algorithms:
y <- A(m; r) (gdzie r <- {0, 1}^1, m = input). y to random variable.

Independent events: Pr[A and B] = Pr[A] * Pr[B]
     Independent variables: forall a, b: Pr[X=a and Y=b] = Pr[X=a] * Pr[Y=b]

Czyli dwa zdarzenia są niezależne, jeśli znajomość jednej zmiennej mówi nic o wartości drugiej zmiennej.

Twierdzenie (trywialne): a jest random variable na jakiejkolwiek dystrybucji, a b jest uniform variable, to a^b jest uniform variable

Ciphertext powinien nie powinien mówić żadnej informacji o plaintexcie.

Birthday paradox: jeśli mamy r zmiennych losowych, to kiedy n ~=sqrt(U), Pr[exists i != j: Ri = Rj] >= 1/2

# Lesson 2.1 - information theoretic security

One Time Pad == M xor C

Information Theoretic Security: szyfr jest information theoretic secure, jeśli ciphertext nie wyjawia kompletnie żadnych informacji o plaintexcie.

Cipher E, D na (K, M, C) ma perfect secrecy, if
dla każdego m0, m1 (len(m0, m1)), `forall c \in C: Pr[E(k, m0) = c] = Pr[E(k, m1) = c] (k - uniform w K).`

(czyli każdy ciphertext ma dokładnie taką samą szansę na bycie stworzonym z każdej wiadomośći)

# Lession 2.2 - stream ciphers 

PRG - bierze seed i generuje (pseudo)losowe wartości. Nie jest information theoretic secure (oczywiście).

RPG musi być unpredictable - tzn. jeśli z G(k) możemy poznać G(G(k)) to jest predictiable, i to bardzo źle dla security.

Mówimy że PRG jest predictiable iff istnieje efektywny algorytm taki że:

    Pr[A(G(k)[:i])] = G(k)[i+1] >= 1/2 + epsilon

Często używane PRG:
 - LCG (linear congruential generator)

Stream ciphers - bierze seed i zmienia w duuuużo większy klucz (a później można z tego zrobić OTP).

Algorytym jest predictible, jeśli mając ciphertext i znając pierwsze n bitów plaintexta, możemy zgadnąć resztę plaintextu.

Definicja `negligible` (formalna, praktyczna to 'e <= 1/2^30):

e to funkcja z Z -> R. Jest non-neglibible iff istnieje takie d, że e(lambda) >= 1/lambda^d (nieskończoną ilość razy).

# Lesson 3.3 - Attacks on stream ciphers and OTP

Ofc nie używać nigdy OTP więcej niż raz

Przykład słabego protokołu: MS-PPTP

Ofc każdy blok jest szyfrowany w ten sam sposób, więc problem jest taki że C(x) = C(y) <=> x = y

# Lesson 3.4 - Real world stream ciphers

Real world stream ciphers

1. RC4 (1987)
Przyjmuje seed (różnej wielkości).
Jest rozszerzany do 2048bitowego klucza, używanego jako stan wewnętrzny.

Słabości:
Pr[2nd byte = 0] = 2/256
Pr[ (0, 0) ] = 1/256^2 + 1/256^3
Related key attacks

2. CSS
Linear feedback shift register (LFSR) - rejestr przesuwający wartości.
 - CSS używa 2 LFSR
 - GSM używa 3 LFSR
 - Bluetooth używa 4 LFSR
 - wszystkie są złamane

Content Scrambling System - algorytm szyfrujący filmy na DVD

Nowoczesne stream ciphery przyjmują seed i nonce (czyli IV chyba)

Salsa bierze seed 128 bitowy (albo 256 bitowy), i nonce 64bitowe.
Zaleta salsy jest taka, że jest prosta do zrobienia w hardware, i szybka w software.
Salsa20(k; r) = H(k, (r, 0)) || H(k, (r, 1)) || H(k, (r, 2)) ...

Robimy jakiś wektor A = [Const T0]:4 [key]:16 [Const T1]:4 [nonce]:8 [index]:8 [Const T2]:4 [key]:16 [Const T3]:6
Później wykonujemy funkcje h: h(A). Funkcja h jest kompletnie odwracalna, i designowana żeby być szybka na SSE2.
I robimy to znowu i znowu, 10 razy B = h(h(h(h(h(h(h(h(h(h(A)))))))))))
I pod koniec robimy wykon = B ^ A. (xorujemy wszystko).

## Lesson 2.5 - PRG Security Definitions

Statistical test: algorytm który przyjmuje n-bitowy string, i zwraca 0 albo 1. 0 znaczy że algorytm nie wygląda na losowy, a 1 że wygląda na losowy.

Statistical tests:
1) Pr[bit = 0] ~~ Pr[bit = 1]
2) Pr[2 bity = 00] ~~ 1/4
3) Pr[max run of bits] <= log2(n)

Czyli nie można rozróżnić outputu od statystycznie uniform outputu.

Definnicja PRG - co to znaczy żę jest nierozróżnialny od random
G: K -> {0, 1}^n
[k <- K, output G(k)]
jest nierozróżnialne od
[r <- {0, 1}^n, output r}

Advantage: G to PRG a A to test statystyczny
i definiujemy
ADV_{PRG}[A, G] = |Pr[A(G(K)) = 1] - PR[A(r) = 1]| - czyli różnica między wynikami prawdziwego RNG i PRG

Czyli bierzemy generator PRG i test statystyczny A. I teraz jaka jest "przewaga", czyli jak bardzo różni się rozkład wyników A(PRG(x)) jeśli PRG zamienimy prawdziwym generatorem liczb losowych.

Mówimy że PRG jest secure, jeśli dla każdego "efektywnego" statystycznego testu Adv_{PRG}[A, G] jest negligible

Czy można udowodnić że PRG jest secure? Nie wiadomo - P vs NP.
Jeśli PRG jest predictible, to jest insecure.

Fakt: Secure PRG jest unpredictiable.
Przez kontrapozycjeL RPG predictiable => PRG jest insecure.
RNG mamy, który mając pierwsze N bitów, potrafi wygenerować N+1 bit z prawdopodobieństwem 1/2 + epsilon, epsilon>0 (non-negligible).

Odwrotność: unprefictiable PRG jest secure

## Lesson 2.6 - Semantic Security

Semantic security - definiujemy przez definiowanie "eksperymentów".
Mamy adwersarza A który chce złamać system, i "challenge".
1. Challenge bierze losowy klucz
2. Adwersarz wysyła dwie wiadomości, m0 i m1.
3. Challenge wysyła szyfrowanie m0 albo m1, losowo
4. Adwersarz próbuje zgadnąć czy dostał zaszyfrowane m0 czy m1

Wn = zdarzenie że Exp(n) = 1
Adv_ss[A, E] = |Pr[W0] - Pr[w1]| - czyli jak bardzo jest w stanie rozróżniać pomiędzy wiadomościami.
Jeśli adv jest blisko zera, to dobrze.

E jest semantic secure <=> dla wszystkich A Adv[A, E] jest negligible

Stream cipher jest secure RNG => stream cipher E z jest semantically secure
dla każdego semantic secure adversary A, istnieje PRG adversary B

## Lesson 2.7 - Stream Ciphers Are Semantically Secure

Twierdzenie: jeśli G jest secure PRG, to stream cipher E derived z G jest semtanically secure.

## Lesson 3.1 - Block Ciphers

Przykłady:
 - 3DES (n = 64bit, k = 168bit)
 - AES (n = 128bit, k = 128bit ... 256bit)

Build by iteration:

key k, robimy key expansion k1, k2, k3...

i robimy coś w rodzaju

m0 = plaintext
m1 = R(k1, m0)
m2 = R(k2, m1)
m3 = R(k3, m2)
...
ciphertext = R(kn, mn)

Pseudo Random Function (PRF) to funkcja zdefiniowana na (K, X, Y)

F: K * X -> Y

Pseudo Random Permutation (PRP) to funkcja:

F: K * X -> X

P4*20RF jest secure jeśli random function w Funs[X, Y] jest indistinguishable od random function w S_F

Proste zastosowanie - z PRF f można zrobić PRG za pomocą f(k, 0) | f(k, 1) ..

## Lesson 3.2 Data Encryption Standard

Feistel network:

L1 = R0
R1 = f(R0) ^ L0

L2 = R1
R2 = f(R1) ^ L1

...

Ln = R(n-1)
Rm = f(L(n-1)) ^ L(n-1)

Ciekawa rzecz - dla każdych funckji f1, ... fd, feistel network jest invertible.

DES - 16 round feistel network

## Lesson 3.3 - Exhaustive Search Attacks

Luby-Rackoff theorem - mówi że jeśli round function jest secure pseudorandom function (PRF), to
3 roundy wystarczą żeby zrobić pseudorandom permutation (PRP).
Czyli zrobienie PRP z PRF

    Luby-Rackoff theorem discussed in Lecture 3.2 states that applying a three round Feistel network to a secure PRF gives a secure block cipher

Mając (m1, m2, m3) oraz (c1, c2, c3) chcemy poznać klucz.

Triple DES - trzy klucze, a 3E((k1, k2, k3), msg) = E(k1, D(k2, E(k3, msg)))
Key size ma 168 bitów, ale jest banalny atak w czasie 2^118

Dlaczego 3DES a nie 2DES?

Bo zakładając 2E((k1, k2), m) = E(k1, E(k2, m))
Rozwiązujemy równanie E(k2, m) = D(k1, c)
MITM attack (robimy tabele k -> E(k, M) oraz k -> D(k, M)

DESX:
* E((k1, k2, k3), m) = k1 ^ E(k2, k3 ^ m)
* Wielkość klucza = 64 + 56 + 64.
* Ale  jest atak o złożoności 2^120 (homework?)
* Jeśli będzie tylko jeden xor, to desx robi nic (homework?)

## Lesson 3.4 - More Attacks On Block Ciphers

* Side channel attacks

* Linear and differential attacks

Linear cryptanalysis: c = DES(k, m)

Dla losowej funkcji:
Pr[podzboir_bitow_m ^ podzbior_bitow_c = podzbior_bitow_k] = 1/2 + e

Ale dla DES takie coś istnieje z e = 0.0000000477.

Theorem: mając 1/e^2 losowocyh (m, c=DES(k, m)) par, to:
podzbior_bitow_k = MAJ[podzbior_bitow_m ^ podzbior_bitow_c]
(z prawdopodobieństwem 97.7%)

* Quantum attacks

Bruteforce normalnie bierze O(|X|)

Grover algorithm bierze O(sqrt(|X|))

## Lesson 3.5 - The AES Block Cipher

AES to substitution permutation network (nie feistel)

Działa tak że robi dużo substytucji, i po każdym kroku xoruje z fragmentem klucza.
* ByteSub
* ShiftRows
* MixColumn

Ataki na AES:
* Key Recovery - najlepszy atak 4x szybszy niż exhaustive search
* Related Key Attack - mając 2^99 input/output keys z 4 related keys, atak w czasie 2^99

## Lesson 3.6 - Block ciphers from PRGs

GGM PRF:
Rozszerzanie PRG (PRNG) na block cipher/PRF - mamy klucz k0=k, k1, k2, k3..., i dla inputu x0, x1, x2, x3
Robimy:
k1 = G(k0)[x0]
k2 = G(k2)[x1]
k3 = G(k3)[x2]
...
kn = wynik
Czyli PRF z PRNG

## Lesson 4.1 - PRPs and PRFs

Funs[X, Y] -> zbiór wszystkich funkcji z X na Y
S_F = { F(k, *) dla k \in K } (podzbiór Funs[X, Y]).

PRF jest secure jeśli jest indistinguishable z funkcji z Funs[X, Y]

PRF Switching Lemma - secure PRP jest też secure PRF, jeśli |X| jest wystarczająco duże

## Lesson 4.2 - Modes of operation - one time key

Duży błąd przy szyfrowaniu - ECB mode.
ECB nie jest semantically secure.

## Lesson 4.3 - Security for many time key

Atak na key used more than once.
Chosen plaintext attack (CPA) (całkiem życiowe)

Znane sposoby nie są semantically secure, bo zawsze jeden pt szyfreuje sie do jednego ct
Sposoby na walczenie z tym:
* randomized encryption (wiele ct dla jednego pt)
* nonce

nonce - wartość zmieniająca sie z wiadomości na wiadomość.
Para (k, n) nigdy nie jest używana więcej niż raz.

## Lesson 4.4 - Modes of operation - many time key (CBC)

(ja wiem jak działa cbc)
c0 = e(k, iv ^ p0)
c1 = e(k, c0 ^ p1)
c2 = e(k, c1 ^ p2)
...
cn = e(k, c(n-1) ^ pn)

IV w CBC musi być nieprzewidywalny, inaczej jest silny atak.

Bug w TLS 1.1 - IV dla rekordu #i = ostatni CT rekordu #(i-1)

Prosty padding - n byte pad w postaci [n, n, n, ...] - dekryptor czyta ostatni bajt i usuwa ostatnie n bajtów.

## Lesson 4.5 - Modes of operation - many time key (CTR)


c0 = p0 ^ e(k, iv + 0)
c1 = p1 ^ e(k, iv + 1)
c2 = p2 ^ e(k, iv + 2)
...
cn = pn ^ e(k, iv + n)

Porównanie CTR i CBC

Counter mode theorem: dla każdego L > 0
jeśli F jest secure PRF na (K, X, X) to
E_CTR jest semantically secure pod CPA over (K, X^L, X^{L+1})

W szczególności dla q-query adversary A atakującego E_CTR istnieje PRF adversary taki że

Adv_CPA[A, E_CTR] <= 2 * Adv_PRF[B, F] + 2 * q^2 *L / |X|

Czyli ctr jest secure tak długo jak q^2 * L << |X|

|                       | CBC               | CTR
| uses                  | PRG               | PRF
| parallel              | no                | yes
| security of rand. enc | q^2 * L^2 << |X|  | q^2 * L << |X|
| dummy padding block   | yes               | no
| 1 byte messages       | 16x expansion     | no expansion

## Lesson 5.1 - Message Authentication Codes

Przykłady:
- protecting public binaries on disk
- protecting banner ads on website

alice wysyła wiadomość m do bob
alice liczy tag = S(k, m)
a bob weryfikuje V(k, m, tag)

Integrity naprawdę wymaga shared key - bez tego nie ma integrity.

Wymagania do secure mac:
Możliwości atakującego:
 - chosen message attack (dostaje tagi dla wybranych wiadomości)
Cel atakującego:
 - stworzenie nowej pary (wiadomośc, tag)

## Lesson 5.2 - MACs based on PRFs

Definiujemy l_F (S, V) jako S(k, m) = F(k, m)
V(k, m, t) jest ok, jesli t = F(k, m)

(PRF to taki hash)

Jeśli F : K * K -> Y jest secure PRF i 1/|Y| jest negligible, to l_f jest secure MAC.

Co zrobić jeśli mamy PRF dla małych wiadomości i chcemy PRF dla długich wiadomości?

Dwa rozwiązania:
- CBC-Mac (banking - ANSI X9.9, X9.19, FIPS 186.3)
- HMAC (protokoły internetowe - SSL, IPsec, SSH)

## Lesson 5.3 - CBC-MAC i NMAC

CBC mac działa tak:

    c0 = f(k, m0) ^ iv
    c1 = f(k, m1) ^ c0
    c2 = f(k, m2) ^ c1
    ...
    cn = f(k, mn) ^ c(n-1)
    cf = f(k1, cn)

Wynikiem CBC-MAC jest cf.

Bez ostatniego kroku ta funkcja nazywa się Raw CBC, i nie jest bezpieczna kryptograficznie

NMAC (nested mac)

c0 = f(k, m0)
c1 = f(c0, m1)
c2 = f(c1, m2)
...
cn = f(c(n-1), mn)
cf = f(k1, cn || fixed_padding)

Wynikiem NMAC jest cf.

ECBC jest często używany z AES.
NMAC rzadko - trzeba zmienić AES na każdym bloku. Ale jest podstawą HMAC.

## Lesson 5.4 - MAC padding

ISO padding - padowanie za pomocą 10000.0000, ostatnia jedynka oznacza początek paddingu.

CMAC - wariant CBC-MAC gdzie mamy klucz = (k, k1, k2)

Nie ma final encryption step
Nie ma dummy blocku

Jeśli wiadomośc nie jest wielokrotnością block length, to dodajemy padding i xorujemy z k1.
Ale jeśli wiadomośc jest wielokrotnością key length, to nie paddujemy niczego, ale xorujemy z k2

## Lesson 5.5 - PMAC and the Carter Webman MAC

c0 = f(k1, m0 ^ P(k, 0))
c1 = f(k1, m1 ^ P(k, 1))
c2 = f(k1, m2 ^ P(k, 2))
...
cn = f(k1, mn ^ P(k, n))
cf = f(k1, c0 ^ c1 ^ c2 ^ ... ^ cn)

Funkcja P jest bardzo prostą funkcją (mnożenie)

Padding podobny do CMAC.

Ciekawa własnośc PMAC - jest inkrementalny jeśli funkcja jest PRP. Jeśli zmieni się jeden blok, możemy łatwo obliczyć nowy tag dla wiadomości (za pomocą dwóch xorów).

One time MAC - MAC używany tylko raz z jednym kluczem.
One time MAC może być secure do wszystkich adversaries.

Przykład one time mac:
- q jest dużą liczbą pierwszą
- klucz jest parą liczb pierwszych
- wiadomość to m1 .. ml
MAC to S(key, msg) = P_{msg}(k) + a (mod q)
gdzie P_{msg}(x) = mn*x^n + ... + m1*x^1

Jest kompletnie bezpieczny przeciwko atakom.

Cartem Wegman MAC - sposób na zmianę one time MAC na many time MAC:

F - secure PRF
(S, V) - secure one time MAC 
CW((k1, k2), m) = (r, F(k1, r) % S(k2, m))
dla losowego r <= {0, 1}^n

Wtedy CW jest bezpiecznym MAC (outputujący tagi w {0, 1}^{2n}

## Lesson 6.1 - Introduction (to hashes)

Recap - message integrity - konstrukcje MACów:
- ECBC-MAC, CMAC - często używane z AES (np. 802.11i)
- NMAC - baza dla HMAC
- PMAC - parallel mac
- Cartel-Webman MAC - build from a fast one time MAC

Collision Resistance - H : M -> T to funkcja hashująca (|M| >> |T|)

Funkcja h jest collision resistant jeśli dla wszystkich efektywnych algorytmó A

Adv_{CR}[A, H] = Pr[A outputs collision for H] jest negligible
Przykładowa funkcja - SHA256.

Jeśli mamy public read only space, to nie potrzeba klucza do weryfikacji.

## Lesson 6.2 - Generic birthday attack

- Wybieramy 2^{n/2} losowych wiadomości w M.
- obliczamy dla każdej ti = J(mi)
- szukamy kolizji ti = tj

## Lesson 6.3 - Merkle-Damgard Paradigm

Merkle-Damgard iterated construction:

h0 = h(m0, iv)
h1 = h(m1, h0)
...
hm = h(mn, h(n-1))

W ten sposób z funkcji hashującej krótkie wiadomości otrzymujemy funkcje hashującą długie wiadomości.

Compression function - funkcja transformująca dwie wiadomości (o fixed length) w jeden (fixed length) output.
Ta transformacja koniecznie musi być one way, tzn. że mając output bardzo ciężko znaleźć wejścia które
kompresując se do takiego outputu.

## Lesson 6.4 - Construction compression functions

Goal: construct compression function h : T * X -> T

Zrobienie compression function z block cipher:
Davies Meyer compression function: h(H, m) + E(m, H) ^ H

Są też inne konstrukcje, np. Miyaguchi-Preneel:
h(H, m) = E(m, H) ^ H ^ m (Whirpool)


Ale inne warianty naturalne nie są bezpieczne.

SHA256 :
korzysta z merkle-damgard function
korzysta z davis meyer compression function
block cipher używany to shacal-2

Provable compression functions:
wybierz losową 2000bitową liczbę pierwszą i losowe 1 <= u, v <= p

Dla m, h <= p-1 zdefiniuj h(H, m) = u^H * v^m (mod p)

Znalezienie kolizji jest tak trudne jak rozwiązanie dyskretnego logarytmu modulo p.

## Lesson 6.5 - HMAC

Prosta, niebezpieczna metoda na zrobienie MAC:

S(k, m) = H(k || m)

Niestety, jest to kompletnie insecure (a wiele osób uzywa takiej konstrukcji).

ALe jest standardowa metoda na konwersję hash function na MAC, i nazywa sie HMAC.

HMAC:

S(k, m) = H(k ^ opad, H(k ^ ipad || m))

## Lesson 6.6 - Timing attacks on MAC verification:

    def Verify(key, msg, sig_bytes):
        return HMACH(key, msg) == sig_bytes

Problem w tym że porównanie == jest wykonywane bajt po bajcie.

Prosty timing attack.
