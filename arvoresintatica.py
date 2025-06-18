import re


# Separa os elementos da expressão e classifica cada um
def gerar_tabela_tokens(expressao):
    padrao = r'\d+\.\d+|\d+|[()+\-*/]'  # Padrão para separar os tokens
    tokens = re.findall(padrao, expressao)
    tabela = []

    for t in tokens:
        if re.fullmatch(r'\d+\.\d+', t):
            tipo = "D.D"
        elif re.fullmatch(r'\d+', t):
            tipo = "Digito"
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

    def derivar_E(tok_list, nivel=0, contador=0):

        indent = "  " * nivel  # Faz a indentação da derivação

        if tok_list[0] == '(' and ')' in tok_list:
            listaparenteses = []
            while tok_list[0] != ')':
                listaparenteses.append(tok_list[0])
                tok_list.pop(0)
            tok_list.pop(0)  # Remove o ')'
            if len(tok_list) == 0: contador = 1
            derivar_E(listaparenteses, nivel, contador)
            nivel+=1
            if len(tok_list) == 0: return

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

        elif tok_list[0] in "+-*/":
            indent = "  " * nivel
            print(f"{indent}O → {tok_list[0]}")
            derivar_E(tok_list[1:], nivel)

        elif len(tok_list) >= 3:
            if '(' == tok_list[0]:
                boleano = False
                # Conta quantos parênteses estão abertos
                for e in tok_list:
                    if e == ')':
                        boleano = True
                    if e == '(':
                        boleano = False
                    if boleano:
                        contador += 1
            if contador > 3 or contador == 0:
                print(f"{indent}E → I O E")
                nivel += 1
                indent = "  " * nivel
            else:
                print(f"{indent}E → I")
            print(f"{indent}I → N")

            if '(' == tok_list[0]:
                print(f"{indent}N → ( E )")

                nivel += 1
                indent = "  " * nivel
                print(f"{indent}E → I O E")

                print(f"{indent}I → N")
                tok_list.pop(0)  # Remove o '('

            if '.' in tok_list[0]:
                print(f"{indent}N → D.D")
                d1, d2 = tok_list[0].split('.')
                print(f"{indent}D → {d1}")
                print(f"{indent}D → {d2}")

            else:
                print(f"{indent}N → D")
                print(f"{indent}D → {tok_list[0]}")
            print(f"{indent}O → {tok_list[1]}")
            derivar_E(tok_list[2:], nivel)

        else:
            print(f"{indent}Expressão inválida ou incompleta.")

    derivar_E(tokens)


expressao = input("Digite uma expressão: ")
expressao = expressao.replace(" ", "")  # Remove espaços em branco

tokens, tabela = gerar_tabela_tokens(expressao)
imprimir_tabela(tabela)
print("\nDerivação:")
imprimir_derivacao(tokens)
