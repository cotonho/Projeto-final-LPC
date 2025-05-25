
import re
invalido = 0
contadorOperadores = 0
expressao = input("Digite uma expressão: ")
operadores = "+-*/"
partes = re.split(r'([+\-*/])', expressao)
contadorOperadores = sum(1 for e in partes if e in operadores) #verifica se existe mais de um operador
if contadorOperadores != 1: invalido = 1, print("Quantidade inválida de operadores.")
if len(partes) != 3: invalido = 1, print("Expressão invalida para a estrutura <numero> <op> <numero>. Número inesperado de operadores.")
#verifica se a expressão é do tamanho esperado
posicao = 0
try:
 
    int(partes[0])
    
    posicao = 2
    
    int(partes[2]) # verifica se os valores são válidos
except TypeError: invalido = 1, print(f"Valor inválido na posição {posicao}.")
except ValueError: invalido = 1, print(f"Valor inválido na posição {posicao}.")
if invalido: print("Portanto essa expressão não é válida.")
