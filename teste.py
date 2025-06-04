
import re
invalido = 0
contadorOperadores = 0
Os_Necessarios = 0
Es_Necessarios = 0
expressao = input("Digite uma expressão: ")
operadores = "()+-*/"


partes = re.split(r'([(+\-*/)])', expressao)


print(partes)

partes = list(filter(None, partes))

try: # esse código ainda passa as verificações em operações como 1++
    for atual in partes:

        if atual in operadores:
            if atual == '(':
                Es_Necessarios += 1
            elif atual == ')':
                continue
            else: 
                Os_Necessarios += 1
            
        else:
            Es_Necessarios += 1
            int(atual)

    # verifica se os valores são válidos
except TypeError: invalido = 1, print(f"Valor inválido na posição .")
except ValueError: invalido = 1, print(f"Valor inválido na posição .")

print(Os_Necessarios, Es_Necessarios)

if invalido: print("Portanto essa expressão não é válida.")
else:print('passou')
# testes