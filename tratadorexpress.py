import re

def Expressoes_Necessarias (Os_Necessarios, Es_Necessarios):
    IOEs = 0
    Is = 0

    while Os_Necessarios > 0 or Es_Necessarios > 0:
        if Os_Necessarios >= 1 and Es_Necessarios >= 1:
                    IOEs += 1
                    Os_Necessarios -= 1
                    Es_Necessarios -= 1

        elif Es_Necessarios == 1 and Os_Necessarios == 0:
            Is = 1
            Es_Necessarios -= 1

    return IOEs, Is

# Variáveis
invalido = 0
contadorOperadores = 0
Os_Necessarios = 0
Es_Necessarios = 0
parenteses = 0
expressao = input("Digite uma expressão: ")
operadores = "()+-*/"

# Caracteres que serão utilizados para separar a expressão
partes = re.split(r'([(+\-*/)])', expressao)


# remove espaçõs vazios de partes
partes = list(filter(None, partes))

print(partes)

try: # esse código ainda passa as verificações em operações como 1++
    for atual in partes:

        if atual in operadores:
            if atual == '(':
                parenteses += 1
            elif atual == ')':
                continue
            else:
                Os_Necessarios += 1

        elif (float(atual).is_integer()):
            Es_Necessarios += 1

            decimal = int(atual)
        else:
            decimal = float(atual)
            Es_Necessarios += 1    

    # verifica se os valores são válidos
except TypeError: invalido = 1, print(f"Valor inválido na posição")
except ValueError: invalido = 1, print(f"Valor inválido na posição")

print(f"O: {Os_Necessarios}, E: {Es_Necessarios}")

IOEs, Is = Expressoes_Necessarias(Os_Necessarios, Es_Necessarios)
print(f"IOEs: {IOEs}, Is: {Is}")

if invalido: print("Portanto essa expressão não é válida.")
else:print('passou')