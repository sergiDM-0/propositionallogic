from collections import OrderedDict
from itertools import product

from src.entity.operators import *


def generate_combinations(prepositions):
    return list(product([True, False], repeat=len(prepositions)))


def evaluate_expression(expr, result, row):
    value = None

    if expr is None:
        raise ValueError(
            "Nó da expressão é None. Verifique a fórmula e use ^, ∧ ou & para 'e'; v, ∨ ou | para 'ou'."
        )

    if expr in result and len(result[expr]) > row:
        return result[expr][row]

    if isinstance(expr, Operator):
        left_value = evaluate_expression(expr.left, result, row)
        right_value = evaluate_expression(expr.right, result, row)

        if isinstance(expr, Conjunction):
            value = left_value and right_value
        elif isinstance(expr, Disjunction):
            value = left_value or right_value
        elif isinstance(expr, Conditional):
            value = (not left_value) or right_value
        elif isinstance(expr, BiConditional):
            value = left_value == right_value
        elif isinstance(expr, ExclusiveOr):
            # XOR: verdadero si exactamente uno es verdadero
            value = left_value != right_value
        elif isinstance(expr, Nand):
            # NAND: negación de AND
            value = not (left_value and right_value)
        elif isinstance(expr, Nor):
            # NOR: negación de OR
            value = not (left_value or right_value)
    elif isinstance(expr, Negation):
        value = not evaluate_expression(expr.expr, result, row)
    else:
        return result[expr][row]

    result.setdefault(expr, []).append(value)

    return value


def evaluate_expressions(prepositions, expressions, combinations):
    prep_combinations = list(zip(*combinations))
    result = {Preposition(preposition): prep_combinations[i] for i, preposition in enumerate(prepositions)}

    for i in range(len(combinations)):
        for expr in expressions:
            evaluate_expression(expr, result, i)

    keys = list(result.keys())

    return OrderedDict(
        sorted(
            result.items(),
            key=lambda item: (
                not isinstance(item[0], Preposition),
                not (isinstance(item[0], Negation) and isinstance(item[0].expr, Preposition)),
                str(item[0].expr) if isinstance(item[0], Negation) and isinstance(item[0].expr, Preposition) else None,
                keys.index(item[0])
            )
        )
    )


def table_type(results):
    if all(result[-1] for result in results):
        return "Tautologia"
    elif all(not result[-1] for result in results):
        return "Contradição"
    else:
        return "Contingência"


def is_valid(results, premises, conclusion):
    """
    Verifica si un argumento lógico es válido.
    
    Un argumento es válido si y solo si: siempre que TODAS las premisas
    sean verdaderas, la conclusión también debe ser verdadera.
    
    Args:
        results: Diccionario con los valores de verdad de cada expresión
        premises: Lista de expresiones que son premisas
        conclusion: Expresión que es la conclusión
        
    Returns:
        True si el argumento es válido, False en caso contrario.
    """
    if not premises:
        # Sin premisas, verificamos si la conclusión es una tautología
        return all(results[conclusion])
    
    final_premises = [results[premise] for premise in premises]
    final_conclusion = results[conclusion]

    for row_premises, row_conclusion in zip(zip(*final_premises), final_conclusion):
        # Un argumento es inválido si existe una fila donde:
        # TODAS las premisas son verdaderas Y la conclusión es falsa
        if all(row_premises) and not row_conclusion:
            return False

    return True
