from src.entity.operators import *
from src.entity.quantifiers import *


def encode_expression(expr: str) -> Base:
    """
    Codifica una expresión lógica en texto a una estructura de objetos.
    
    Args:
        expr: Expresión lógica como string (ej: "P^Q", "P->Q", "~P")
    
    Returns:
        Objeto Base representando la expresión, o None si la expresión está vacía.
    
    Raises:
        ValueError: Si la expresión tiene formato inválido.
    """
    if not expr or not expr.strip():
        return None
    
    i = 0
    result = []

    while i < len(expr):
        if expr[i] == '(':
            # Ignore '('
            i += 1
            # Sum `i` to find the real position of parenthesis in current expr
            # Add 1 to the result to move to the character immediately after the closing parenthesis.
            j = find_parentheses_end(expr[i:]) + i + 1

            sub_expr = encode_expression(expr[i:j])
            if sub_expr is not None:
                result.append(sub_expr)
            # Move to the closing ')' - it will be skipped in the next iteration
            i = j
        elif expr[i] == ')':
            # Ignore ')'
            i += 1
        # The operator with the most characters is 'nand' (4), so check up to 4 chars
        elif operator := find_operator(expr[i:i + 4]):
            i += len(operator)

            # The behavior of negation is different from the other operators
            # While operators have a left and right side to the expression, negation has only one parameter
            if operator not in get_operators(Negation):
                right = encode_expression(expr[i:])
                if not result:
                    raise ValueError(f"Operador '{operator}' sin operando izquierdo en: {expr}")
                left = result.pop()
                
                if right is None:
                    raise ValueError(f"Operador '{operator}' sin operando derecho en: {expr}")

                return operators[operator](left, right)
            else:
                # After the negation there can be a parenthesis or a literal, as in ~(P^Q) or ~P
                if i >= len(expr):
                    raise ValueError(f"Negación sin expresión después en: {expr}")
                
                if expr[i] == '(':
                    i += 1
                    j = find_parentheses_end(expr[i:]) + i
                    sub_result = encode_expression(expr[i:j])
                    i = j  # The ')' will be skipped in the next iteration
                elif not expr[i].isalpha():
                    # Double negation or other operator after negation
                    i += 1
                    end_pos = find_end(expr[i:])
                    j = (end_pos if end_pos is not None else 0) + i + 1
                    sub_result = encode_expression(expr[i - 1:j])
                    i = j
                else:
                    end_pos = find_end(expr[i:])
                    j = (end_pos if end_pos is not None else 0) + i + 1
                    sub_result = encode_expression(expr[i:j])
                    i = j

                if sub_result is not None:
                    result.append(Negation(sub_result))
                else:
                    raise ValueError(f"Negación de expresión vacía en: {expr}")
        elif quantifier := find_quantifier(expr[i]):
            i += 2
            if i > len(expr):
                raise ValueError(f"Cuantificador sin variable en: {expr}")
            var = expr[i - 1]

            if i >= len(expr):
                raise ValueError(f"Cuantificador sin expresión en: {expr}")
            
            if expr[i] == '(':
                i += 1
                j = find_parentheses_end(expr[i:]) + i
                sub_result = encode_expression(expr[i:j])
                i = j  # The ')' will be skipped in the next iteration
            elif expr[i] in get_operators(Negation):
                i += 1
                end_pos = find_end(expr[i:])
                j = (end_pos if end_pos is not None else 0) + i + 1
                sub_result = Negation(Predicate(expr[i], [*expr[i + 1:j]]))
                i = j
            elif not expr[i].isalpha():
                sub_result = encode_expression(expr[i:])
                i = len(expr)
            else:
                i += 1
                end_pos = find_end(expr[i:])
                j = (end_pos if end_pos is not None else 0) + i + 1
                sub_result = encode_expression(expr[i - 1:j])
                i = j

            result.append(quantifiers[quantifier](var, sub_result))
        else:
            end_pos = find_end(expr[i:])
            j = (end_pos if end_pos is not None else 0) + i + 1

            if j - i >= 2:
                sub_result = Predicate(expr[i], [*expr[i + 1:j]])
            else:
                sub_result = Preposition(expr[i].upper())

            result.append(sub_result)
            i = j

    if len(result) == 1:
        return result[0]
    elif len(result) == 0:
        return None
    else:
        # Si hay múltiples elementos sin operador entre ellos, es un error
        raise ValueError(f"Expresión mal formada, múltiples elementos sin operador: {expr}")


def find_parentheses_end(expr: str) -> int:
    # In the expr the first parenthesis is ignored, so we start the count with 1
    count = 1

    for i, char in enumerate(expr):
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
            if count == 0:
                return i

    raise ValueError("Parênteses desequilibrados")


def find_operator(expr: str) -> str | None:
    """
    Busca un operador al inicio de la expresión.
    
    Prioriza operadores más largos para evitar falsos positivos
    (ej: "<->" debe encontrarse antes que "<" si existiera).
    
    Args:
        expr: Substring de la expresión a analizar
        
    Returns:
        El operador encontrado o None si no hay ninguno.
    """
    if not expr:
        return None
    
    # Ordenar por longitud descendente para matchear operadores más largos primero
    sorted_operators = sorted(operators.keys(), key=len, reverse=True)
    
    for operator in sorted_operators:
        # Use startswith to avoid false truths like in PvQ, making sure that the start is an operator
        if expr.startswith(operator):
            return operator

    return None


def find_quantifier(expr: str) -> str | None:
    for quantifier in quantifiers:
        if expr.startswith(quantifier):
            return quantifier

    return None


def find_end(expr):
    """
    Encuentra el final de un identificador (preposición o predicado).
    
    Se detiene cuando encuentra un carácter no alfabético o un operador
    (incluyendo operadores multi-carácter como 'xor', 'nand', 'nor').
    
    Args:
        expr: Substring de la expresión a analizar
        
    Returns:
        Índice del último carácter del identificador, o -1 si está vacío.
    """
    if not expr:
        return -1
    
    # Caracteres que terminan un identificador (operadores de un solo carácter)
    terminating_chars = {'v', '∨', '|', '&', '^', '∧', '~', '¬', '⊕', '⊻', '↑', '↓'}
    
    # Operadores multi-carácter que terminan un identificador
    multi_char_operators = ['xor', 'nand', 'nor']
    
    for i in range(len(expr)):
        char = expr[i]
        
        # Termina si no es alfabético
        if not char.isalpha():
            return i - 1
        
        # Termina si es un operador de un solo carácter
        if char in terminating_chars:
            return i - 1
        
        # Verifica si estamos al inicio de un operador multi-carácter
        remaining = expr[i:].lower()
        for op in multi_char_operators:
            if remaining.startswith(op):
                return i - 1
        
        # Si es el último carácter
        if i == len(expr) - 1:
            return i

    return -1


def get_operators(op):
    result = []

    for key, value in operators.items():
        if value == op:
            result.append(key)

    return result
