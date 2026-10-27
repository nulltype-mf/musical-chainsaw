import ast
import operator

import sympy as sp


__all__ = ["parse_function"]

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS = {
    "abs": sp.Abs,
    "Abs": sp.Abs,
    "acos": sp.acos,
    "acosh": sp.acosh,
    "asin": sp.asin,
    "asinh": sp.asinh,
    "acot": sp.acot,
    "acoth": sp.acoth,
    "acsc": sp.acsc,
    "asec": sp.asec,
    "atan": sp.atan,
    "atanh": sp.atanh,
    "atan2": sp.atan2,
    "ceil": sp.ceiling,
    "ceiling": sp.ceiling,
    "cos": sp.cos,
    "cosh": sp.cosh,
    "cot": sp.cot,
    "coth": sp.coth,
    "csc": sp.csc,
    "csch": sp.csch,
    "exp": sp.exp,
    "floor": sp.floor,
    "erf": sp.erf,
    "erfc": sp.erfc,
    "gamma": sp.gamma,
    "ln": sp.log,
    "log": sp.log,
    "Max": sp.Max,
    "Min": sp.Min,
    "sec": sp.sec,
    "sech": sp.sech,
    "sin": sp.sin,
    "sinh": sp.sinh,
    "sinc": sp.sinc,
    "sqrt": sp.sqrt,
    "tan": sp.tan,
    "tanh": sp.tanh,
}

_CONSTANTS = {
    "E": sp.E,
    "pi": sp.pi,
}


def _parse_node(node, symbols):
    if isinstance(node, ast.Expression):
        return _parse_node(node.body, symbols)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return sp.sympify(node.value)
        raise ValueError("Only integer and decimal numbers are supported.")

    if isinstance(node, ast.Name):
        if node.id in symbols:
            return symbols[node.id]
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"Unknown name '{node.id}'. Use only t, y, pi, and E.")

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Use only +, -, *, /, and ** operators.")
        return operation(
            _parse_node(node.left, symbols),
            _parse_node(node.right, symbols),
        )

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Use only unary + and - operators.")
        return operation(_parse_node(node.operand, symbols))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ValueError("Call only supported math functions by name.")
        if node.keywords:
            raise ValueError("Math functions accept positional arguments only.")
        function = _FUNCTIONS[node.func.id]
        return function(*(_parse_node(argument, symbols) for argument in node.args))

    raise ValueError(
        "Use a mathematical expression made from numbers, t, y, "
        "arithmetic operators, and supported math functions."
    )


def parse_function(expression=None):
    """Parse a dy/dt expression and return a callable f(t, y).
    """
    if expression is None:
        print("    Differential Equation Parser >.< ")
        print("Instructions OwO :")
        print("  - Use ** for powers (e.g., t**2)")
        print("  - Use * for multiplication (e.g., 2*y)")
        print("  - Example: t - y, t**2 + 2*y, or sin(t) + y")
        print("  - Supported functions include sin, cos, tan, exp, log, sqrt, abs")
        print("-" * 40)
        expression = input("Enter your differential equation dy/dt = ")

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError(
            "The differential equation expression must be a non-empty string."
        )

    try:
        syntax_tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression {expression!r}: {exc.msg}.") from exc

    t, y = sp.symbols("t y")
    try:
        parsed_expression = _parse_node(syntax_tree, {"t": t, "y": y})
        return sp.lambdify((t, y), parsed_expression, modules="numpy")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid expression {expression!r}: {exc}") from exc


if __name__ == "__main__":
    parse_function()
