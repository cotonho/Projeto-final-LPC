import re

class E():
    
    def __init__(self):
        self.I = None
        self.O = None
        self.E = None
    def imprimir(self):
        
        if isinstance(self.I, E) and self.E is None:
            return f"I: {self.I.imprimir()}, O: {self.O}, E: None"
        elif isinstance(self.I, E) and self.E is not None:
            return f"I: {self.I.imprimir()}, O: {self.O}, E: {self.E.imprimir()}"
        elif self.E is not None:
            return f"I: {self.I}, O: {self.O}, E: {self.E.imprimir()}"
        
        return f"I: {self.I}, O: {self.O}, E: {self.E}"

def monta_arvore(expressao ,  E_instance ):
    index = 0
    while index < len(expressao):
        elemento = expressao[index]

        #agora verifica se é número, inteiro ou decimal
        if re.fullmatch(r'\d+(\.\d+)?', elemento) and E_instance.I is None:
            E_instance.I = elemento

        elif elemento in "+-*/" and  E_instance.O is None:
            E_instance.O = elemento

        elif elemento == "(":
            expre_parents = ""
            index += 1  # Pular o '('
            parenteses_abertos = 1
            while index < len(expressao) and parenteses_abertos > 0:
                if expressao[index] == '(':
                    parenteses_abertos += 1
                elif expressao[index] == ')':
                    parenteses_abertos -= 1
                if parenteses_abertos > 0:
                    expre_parents += expressao[index]
                index += 1

            expre_parents = expre_parents.replace(" ", "")
            partes = re.findall(r'\d+\.\d+|\d+|[()+\-*/]', expre_parents)
            E_instance.I = E()
            monta_arvore(partes , E_instance.I)
            continue  # evitar index++ extra

        if E_instance.E is not None:
            E_profundo = verifica_E(E_instance)
            monta_arvore(expressao[index +1:] , E_profundo)
            return

        elif E_instance.E is None:
            E_instance.E  =  E()

        index += 1       

def verifica_E(objeto):
    if objeto.I is None and objeto.O is None:
        return objeto
    else:
        return verifica_E(objeto.E)       

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
expressao = expressao.replace(" ", "") 

operadores = "()+-*/"

#Separar números decimais 
partes = re.findall(r'\d+\.\d+|\d+|[()+\-*/]', expressao)

# remove espaços vazios de partes
partes = list(filter(None, partes))

try:  # esse código ainda passa as verificações em operações como 1++
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

except TypeError: 
    invalido = 1
    print(f"Valor inválido na posição")
except ValueError: 
    invalido = 1
    print(f"Valor inválido na posição")

IOEs, Is = Expressoes_Necessarias(Os_Necessarios, Es_Necessarios)

if invalido: 
    print("Portanto essa expressão não é válida.")
else:
    print('')

E_instance = E()
monta_arvore(partes, E_instance)

print(E_instance.imprimir())
