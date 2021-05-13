from math import factorial

# сочетания
def combinations(n, k):
    result = factorial(n)/(factorial(k)*factorial(n-k))
    return result

# сочетания с повторениями
def repeat_combinations(n, k):
    result = factorial(n+k-1)/(factorial(k)*factorial(n-1))
    return result

# размещения
def permutations(n, k):
    result = factorial(n)/factorial(n-k)
    return result

# размещения с повторениями
def repeat_permutations(n, k):
    result = n**k
    return result

# перестановки
def replacements(n):
    result = factorial(n)
    return result

# перестановки с повторениями
def repeat_replacements(n, k):
    tmp = factorial(n)
    for i in k:
        tmp = tmp/factorial(i)
    return tmp
