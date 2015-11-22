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
