import re

class D():
    def __init__(self):
        self.value = None

class N():
    def __init__(self):
        self.D = D()

class I():

    def __init__(self):
        self.N = N()

class E():

    def __init__(self):
        self.I = I()
        self.O = None
        self.E = None

    def remover_nulos(self):
        # Remove atributos nulos diretamente no objeto
        if self.I is None:
            del self.I
        if self.O is None:
            del self.O
        if self.E is None:
            del self.E
        else:
            self.E.remover_nulos()

    def imprimir(self):

        partes = ["E:"]
        if hasattr(self, 'I'):
            if isinstance(self.I, E):
                partes.append(f"I: N: D: {self.I.N.D.value.imprimir()}")
            else:
                partes.append(f"I: N: D: {self.I.N.D.value}")
        if hasattr(self, 'O'):
            partes.append(f"O: {self.O}")
        if hasattr(self, 'E'):
            if isinstance(self.E, E):
                partes.append(f"E: {self.E.imprimir()}")
            else:
                partes.append(f"E: {self.E}")
        return ', '.join(partes)


def monta_arvore(expressao, E_instance):
    index = 0

    while index < len(expressao):
        print(index)
        elemento = expressao[index]
        if elemento.isdigit() and len(elemento) == 1 and isinstance(E_instance.I, I):
            E_instance.I.N.D.value = elemento






        elif elemento in "+-*/" and E_instance.O is None:
            E_instance.O = elemento


        elif elemento == "(":
            expre_parents = ""

            while index < len(expressao) and expressao[index] != ")":
                expre_parents += expressao[index]
                index += 1

            expre_parents = expre_parents.replace(" ", "")
            partes = expre_parents[1:]
            partes = list(filter(None, partes))

            E_instance.I = E()
            ref = E_instance.I
            monta_arvore(partes, ref)
            ref.remover_nulos()

        if E_instance.E is not None:
            E_profundo = verifica_E(E_instance)
            monta_arvore(expressao[index + 1:], E_profundo)
            return
            E_instance.E.I = elemento

        elif index + 1 < len(expressao):
            E_instance.E = E()

        index += 1

def verifica_E(objeto):
    try:
        if isinstance(objeto.I, I):
            if objeto.I.N.D.value is None and objeto.O is None:
                return objeto
        elif objeto.I is None and objeto.O is None:
            return objeto
    except AttributeError:
        return objeto  # Caso a estrutura esteja incompleta

    return verifica_E(objeto.E)


def Expressoes_Necessarias(Os_Necessarios, Es_Necessarios):
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

# Caracteres que serão utilizados para separar a expressão
partes = re.split(r'([(+\-*/)])', expressao)

# remove espaçõs vazios de partes
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

        elif float(atual).is_integer():
            Es_Necessarios += 1

            decimal = int(atual)
        else:
            decimal = float(atual)
            Es_Necessarios += 1

    # verifica se os valores são válidos
except TypeError:
    invalido = 1, print(f"Valor inválido na posição")
except ValueError:
    invalido = 1, print(f"Valor inválido na posição")

# print(f"O: {Os_Necessarios}, E: {Es_Necessarios}")

# IOEs, Is = Expressoes_Necessarias(Os_Necessarios, Es_Necessarios)
# print(f"IOEs: {IOEs}, Is: {Is}")

if invalido:
    print("Portanto essa expressão não é válida.")
else:
    print('')

E_instance = E()
monta_arvore(partes, E_instance)

E_instance.remover_nulos()

print(E_instance.imprimir())