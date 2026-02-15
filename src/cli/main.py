# Copyright (C) 2026 Luis Fernando (luisfbl) https://github.com/luisfbl
# Copytight (c) 2026 sergioDm (sergioDm) https://github.com/sergiDM-0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from src.data.encode import encode_expression
from src.cli.truth_table import generate_truth_table


def print_main_header():
    header = r"""
       _____                                 _ _   _                   _ _             _      
    |  __ \                               (_) | (_)                 | | |           (_)     
    | |__) | __ ___  _ __   ___  ___ _ _ _ _| |_ _  ___  _ __   __ _| | | ___   __ _ _  ___ 
    |  ___/ '__/ _ \| '_ \ / _ \/ __| | | | | __| |/ _ \| '_ \ / _` | | |/ _ \ / _` | |/ __|
    | |   | | | (_) | |_) | (_) \__ \ |_| | | |_| | (_) | | | | (_| | | | (_) | (_| | | (__ 
    |_|   |_|  \___/| .__/ \___/|___/\__,_|_|\__|_|\___/|_| |_|\__,_|_|_|\___/ \__, |_|\___|
                    | |                                                         __/ |       
                    |_|                                                        |___/
    """

    print(header)
    print("  Operadores disponíveis:")
    print("    Conjunção (E):      ^, &, ∧")
    print("    Disjunção (OU):     v, |, ∨")
    print("    Condicional:        ->, →")
    print("    Bicondicional:      <->, ↔")
    print("    Negação:            ~, ¬")
    print("    XOR (OU exclusivo): xor, ⊕, ⊻")
    print("    NAND:               nand, ↑")
    print("    NOR:                nor, ↓")


def get_menu_choice():
    print("\nMenu Principal:")
    print("1 - Tabela Verdade")
    print("0 - Sair\n")

    try:
        return int(input("Escolha uma opção: "))
    except ValueError:
        print("Erro: Por favor, digite um número válido.")
        return get_menu_choice()


def parse_input(item, prepositions, expressions):
    try:
        wrapped = encode_expression(item)
    except ValueError as e:
        print(f"Erro ao processar a expressão: {e}")
        return False

    if wrapped is None:
        print(f"Erro: Expressão \"{item}\" é inválida ou está vazia.")
        return False

    if wrapped not in expressions:
        expressions.append(wrapped)

    # Palabras reservadas para operadores (no son preposiciones)
    operator_keywords = {'v', 'xor', 'nand', 'nor'}
    
    # Eliminar las palabras clave de operadores del item antes de buscar preposiciones
    clean_item = item.lower()
    for keyword in operator_keywords:
        clean_item = clean_item.replace(keyword, ' ')
    
    for char in clean_item:
        if char.isalpha() and char.upper() not in prepositions:
            prepositions.append(char.upper())
    
    return True


def get_input_list(prompt, repeat=True):
    prepositions, expressions = [], []

    while True:
        item = input(prompt).replace(" ", "")

        if item == "0":
            break

        success = parse_input(item, prepositions, expressions)
        
        if not success:
            # Si hay error pero repeat=True, permitir reintentar
            if repeat:
                continue
            else:
                break

        if not repeat:
            break

    prepositions.sort()

    return prepositions, expressions


def main():
    print_main_header()

    while True:
        menu = get_menu_choice()

        if menu == 0:
            return

        (prepositions, premises) = get_input_list("Digite uma premissa (ou 0 para pular): ")
        (_, conclusion) = get_input_list("Digite a conclusão (ou 0 para pular): ", False)

        if menu == 1:
            generate_truth_table(prepositions, premises, conclusion)
        else:
            break


if __name__ == "__main__":
    main()
from src.data.encode import encode_expression
from src.cli.truth_table import generate_truth_table


def print_main_header():
    header = r"""
      _____              _ _                 _       
     |  __ \            | (_)               | |      
     | |__) | __ ___  __| |_ _ __ ___   __ _| |_ ___ 
     |  ___/ '__/ _ \/ _` | | '_ ` _ \ / _` | __/ _ \
     | |   | | |  __/ (_| | | | | | | | (_| | ||  __/
     |_|   |_|  \___|\__,_|_|_| |_| |_|\__,_|\__\___|
    """

    print(header)
    print("  Operadores disponíveis:")
    print("    Conjunção (E):      ^, &, ∧")
    print("    Disjunção (OU):     v, |, ∨")
    print("    Condicional:        ->, →")
    print("    Bicondicional:      <->, ↔")
    print("    Negação:            ~, ¬")
    print("    XOR (OU exclusivo): xor, ⊕, ⊻")
    print("    NAND:               nand, ↑")
    print("    NOR:                nor, ↓")


def get_menu_choice():
    print("\nMenu Principal:")
    print("1 - Tabela Verdade")
    print("0 - Sair\n")

    try:
        return int(input("Escolha uma opção: "))
    except ValueError:
        print("Erro: Por favor, digite um número válido.")
        return get_menu_choice()


def parse_input(item, prepositions, expressions):
    try:
        wrapped = encode_expression(item)
    except ValueError as e:
        print(f"Erro ao processar a expressão: {e}")
        return False

    if wrapped is None:
        print(f"Erro: Expressão \"{item}\" é inválida ou está vazia.")
        return False

    if wrapped not in expressions:
        expressions.append(wrapped)

    # Palabras reservadas para operadores (no son preposiciones)
    operator_keywords = {'v', 'xor', 'nand', 'nor'}
    
    # Eliminar las palabras clave de operadores del item antes de buscar preposiciones
    clean_item = item.lower()
    for keyword in operator_keywords:
        clean_item = clean_item.replace(keyword, ' ')
    
    for char in clean_item:
        if char.isalpha() and char.upper() not in prepositions:
            prepositions.append(char.upper())
    
    return True


def get_input_list(prompt, repeat=True):
    prepositions, expressions = [], []

    while True:
        item = input(prompt).replace(" ", "")

        if item == "0":
            break

        success = parse_input(item, prepositions, expressions)
        
        if not success:
            # Si hay error pero repeat=True, permitir reintentar
            if repeat:
                continue
            else:
                break

        if not repeat:
            break

    prepositions.sort()

    return prepositions, expressions


def main():
    print_main_header()

    while True:
        menu = get_menu_choice()

        if menu == 0:
            return

        (prepositions, premises) = get_input_list("Digite uma premissa (ou 0 para pular): ")
        (_, conclusion) = get_input_list("Digite a conclusão (ou 0 para pular): ", False)

        if menu == 1:
            generate_truth_table(prepositions, premises, conclusion)
        else:
            break


if __name__ == "__main__":
    main()
