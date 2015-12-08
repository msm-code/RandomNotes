# Coursera Machine Learning

## Lesson 6.1 - Classification

Klasyfikacja - dzielenie czegoś na klasy:
* email - spam / not spam
* online transactoins - fraud / not fraud
* tumor - malignant / benign

Na razie tylko dwie klasy, ale może też być multi class classification problem.

## Lesson 6.2 - Hypothesis Representation

Logistic Regression Model

Chcemy 0 <= h_o(x) <= 1

    h_o(x) = g(O^T * x)

    g(z) = 1/(1 + e^{-z})

Sigmoid function == Logistic function == g(x).

Przykład - Interpretation of Hypothesis Output

h_o(x) - estimated probability that y=1 on input x

Example: if x = [x0, x1] = [1, tumorsize]

jeśli h_o(x) = 0.7, tzn. pacjent ma 70% szans że jego rak jest malignant.

## Lesson 6.3 - Decision Boundary

    h_o(x) = g(O_0 + O_1 * x_1 + O_2 * x_2)

Powstaje linia, która jest nazywana Decision Boundary - poniżej niej jest y=0, a powyżej jest y=1.

W przypadku nieliniowych modeli, możemy zrobić coś w rodzaju dodania nieliniowych parametrów:

    h_o(x) = g(O_o + O_1*x_1 + O_2*x_2 + O_3 * x_1^2 + O_4 * x_2^2)

Cost function:

Logistic regression: J(O) = 1/n * Sum(1/2 h_o(x^i) - y^i)

Problem z non convex functions - takie funkcje które mają wiele globalnych minimum.

Logistic regression cost function: 

    Cost(h_o(x), y) = -log(h_o(x)) if y = 1
                    = -log(1 - h_o(x)) if y = 0

Taka funkcja kosztu ma kilka ciekawych własności:
* jeśli y=0, h_o(x) = 1 to koszt = 0
* ale kiedy h_o(x) -> 0, to koszt -> inf

## Lesson 6.4 - Simplified Cost Function and Gradient Descent

Bierzemy poprzednią definicję:

    Cost(h_o(x), y) = -log(h_o(x)) if y = 1
                    = -log(1 - h_o(x)) if y = 0

Można ją zapisać prościej jako:

Cost(h_o(x), y) = -y*log(h_o(x)) - (1 - y)*log(1 - h_o(x))

Wstawiając do wzoru

    J(O) = 1/m * sum(Cost(h_o(x^{(i)}), y^{(i)}))

    J(O) = -1/m * sum(y*log(h_o(x)) + (1 - y)*log(1 - h_o(x)))

Gradient descend

    repeat {
        O_j = O_j - a * sum(h_o(x^{(i)}) - y^{(i)}) * x_j^{(i)};
    }


## Lesson 6.5 - Advanced Optimization

Mamy funkcję J(O). Chcemy uzyskać min_o(J(O))

I teraz dane jakie mamy, to:
* kod potrafiący obliczyć J(O)
* kod potrafiący obliczyć d/dO_j * J(O) (pochodną J(O))

I robimy gradient descent:

    repeat {
        O_j = O_j - a*(d/dO_j)*J(O)
    }

Gradient descent to nie jedyny algorytm który potrafi obliczyć minimum mając te same dane!

Algorytmy służące do tego to:
* Gradient descent
  - to o nim jest ostatnie X lekcji
* Conjugare gradient
* BFGS
* L-BFGS

Cechy pozostałych trzech algorytmów:
* zaleta - nie trzeba ręcznie wybierać alpha
* zaleta - często szybszy niż gradient descent
* wada - bardziej skomplikowane

Przykład:

O = [O1, O2]
J(O) = (O1 - 5)^2 + (O2 - 5)^2
d/dO_1*J(O) + 2(O1 - 5)
d/dO_2*J(O) + 2(O2 - 5)

W kodzie:

```
function [jVal, gradient] = costFunction(theta)
    jVal = (theta(1)-5)^2 + (theta(2)-5)^2;
    gradient = zeros(2, 1);
    gradient(1) = 2*(theta(1)-5);
    gradient(2) = 2*(theta(2)-5);
endfunction

options = optimset('GradObj', 'on', 'MaxIter', '100');
initialTheta = zeros(2, 1);
[optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options);
```

gradient(1) - kod obliczający d/dO_0 * J(O)
gradient(2) - kod obliczający d/dO_1 * J(O)
                ...
gradient(n) - kod obliczający d/dO_n * J(O)

## Lesson 6.6 - Multiclass Classification - One-Vs-All

Mutliclass classification - klasyfikacja z wieloma klasami (huh)

Działa tak że klasyfikuje najpierw wszystko osobno dla każdej grupy (czyli dla trzech klas mamy trzy funkcje klasyfikacji binarnej)

Żeby klasyfikować, uruchamiamy wszystkie klasyfikatory, i wybieramy ten który maksymalizuje hipotezę.

