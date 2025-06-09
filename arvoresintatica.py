import re

class D():
    def __init__(self):
        self.value = []

    def imprimir(self, espacos=1):
        indent = "  " * espacos
        return ' '.join(self.value)

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
        # Limpa elementos que não foram preenchidos na árvore
        if self.I is None:
            del self.I
        if self.O is None:
            del self.O
        if self.E is None:
            del self.E
        else:
            self.E.remover_nulos()


    def imprimir(self, espacos=1):
        indent = "  " * espacos
        partes = [f"{'  ' * espacos}E\n{indent}|"]

        # Processa o nó I
        if hasattr(self, 'I'):
            if isinstance(self.I, E):
                partes.append(f"I {self.I.imprimir(espacos)}")
            elif isinstance(self.I, I):
                partes.append(
                    f"I\n{indent}  | N\n"
                    f"{indent}    | D\n"
                    f"{indent}      | {self.I.N.D.imprimir(espacos)}\n"
                )

        # Processa o nó O
        if hasattr(self, 'O'):
            partes.append(f"{indent} O\n{indent}  | {self.O}\n")

        # Processa o nó E
        if hasattr(self, 'E'):
            if isinstance(self.E, E):
                partes.append(self.E.imprimir(espacos + 1))
            else:
                partes.append(f"{indent}E\n{indent}  {self.E}")

        return ' '.join(partes)

# Separa os elementos da expressão e classifica cada um
def gerar_tabela_tokens(expressao):
    padrao = r'\d+\.\d+|\d+|[()+\-*/]'  # Padrão para separar os tokens
    tokens = re.findall(padrao, expressao)
    tabela = []

    for t in tokens:
        if re.fullmatch(r'\d+\.\d+', t):
            tipo = "D.D"
        elif re.fullmatch(r'\d+', t):
            tipo = "D" if len(t) == 1 else "DD/DDD"
        elif t in '+-*/':
            tipo = "Operador"
        elif t == '(':
            tipo = "AbreParêntese"
        elif t == ')':
            tipo = "FechaParêntese"
        else:
            tipo = "Desconhecido"
        tabela.append((t, tipo))

    return tokens, tabela

# Exibe os tokens que foram identificados
def imprimir_tabela(tabela):
    print("\nTokens identificados:")
    for token, tipo in tabela:
        print(f"{token} → {tipo}")

# Imprime a derivação da expressão seguindo a gramática 
def imprimir_derivacao(tokens):
    def is_num(tok):
        return re.fullmatch(r'\d+\.\d+|\d+', tok)

    def derivar_E(tok_list, nivel=0):
        indent = "  " * nivel  # Faz a indentação da derivação

        if len(tok_list) == 1 and is_num(tok_list[0]):
            print(f"{indent}E → I")
            print(f"{indent}I → N")
            if '.' in tok_list[0]:
                print(f"{indent}N → D.D")
                d1, d2 = tok_list[0].split('.')
                print(f"{indent}D → {d1}")
                print(f"{indent}D → {d2}")
            else:
                print(f"{indent}N → D")
                print(f"{indent}D → {tok_list[0]}")
        elif len(tok_list) >= 3:
            print(f"{indent}E → I O E")
            print(f"{indent}I → N")
            if '.' in tok_list[0]:
                print(f"{indent}N → D.D")
                d1, d2 = tok_list[0].split('.')
                print(f"{indent}D → {d1}")
                print(f"{indent}D → {d2}")
            else:
                print(f"{indent}N → D")
                print(f"{indent}D → {tok_list[0]}")
            print(f"{indent}O → {tok_list[1]}")
            derivar_E(tok_list[2:], nivel + 1)
        else:
            print(f"{indent}Expressão inválida ou incompleta.")

# Monta a árvore sintática a partir dos tokens
def monta_arvore(expressao, E_instance):
    index = 0

    while index < len(expressao):
        elemento = expressao[index]

        if re.fullmatch(r'\d+(\.\d+)?', elemento) and isinstance(E_instance.I, I):
            for char in elemento:
                E_instance.I.N.D.value.append(char)

        elif elemento in "+-*/" and E_instance.O is None:
            E_instance.O = elemento

        elif elemento == "(":
            expre_parents = ""
            index += 1
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
            ref = E_instance.I
            monta_arvore(partes, ref)
            ref.remover_nulos()
            continue

        if E_instance.E is not None:
            E_profundo = verifica_E(E_instance)
            monta_arvore(expressao[index + 1:], E_profundo)
            return
        elif index + 1 < len(expressao):
            E_instance.E = E()

        index += 1

# Busca o próximo E disponível na árvore
def verifica_E(objeto):
    try:
        if isinstance(objeto.I, I):
            if objeto.I.N.D.value == [] and objeto.O is None:
                return objeto
        elif objeto.I is None and objeto.O is None:
            return objeto
    except AttributeError:
        return objeto
    return verifica_E(objeto.E)

expressao = input("Digite uma expressão: ")
expressao = expressao.replace(" ", "")  # Remove espaços em branco

tokens, tabela = gerar_tabela_tokens(expressao)
imprimir_tabela(tabela)
print("\nDerivação:")
imprimir_derivacao(tokens) 

print("\nÁrvore Sintática:")
E_instance = E()
monta_arvore(tokens, E_instance)
E_instance.remover_nulos()
print(E_instance.imprimir())
