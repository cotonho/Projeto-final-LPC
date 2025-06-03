
import re
invalido = 0
contadorOperadores = 0
expressao = input("Digite uma expressão: ")
operadores = "()+-*/"


partes = re.split(r'([(+\-*/)])', expressao)


print(f"{partes}")

try: # esse código ainda passa as verificações em operações como 1++
    for atual, prox, prox_prox in zip(partes, partes[1:], partes[2:]):
        if atual in operadores:
            continue
        else:
            int(atual)

    # verifica se os valores são válidos
except TypeError: invalido = 1, print(f"Valor inválido na posição .")
except ValueError: invalido = 1, print(f"Valor inválido na posição .")

if invalido: print("Portanto essa expressão não é válida.")
else:print('passou')
# testes