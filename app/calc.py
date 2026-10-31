import math

import app.util


class InvalidPermissions(Exception):
    pass


class Calculator:
    # Operacione con dos numeros 

    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def substract(self, x, y):
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y):
        if not app.util.validate_permissions(f"{x} * {y}", "user1"):
            raise InvalidPermissions('User has no permissions')

        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")

        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        # 0 elevado a un exponente negativo equivale a dividir entre  0
        if x == 0 and y < 0:
            raise TypeError("No se puede elevar 0 a un exponente negativo")
        # Una base negativa con exponente decimal da un numero complejo
        if x < 0 and not float(y).is_integer():
            raise TypeError("Una base negativa con exponente decimal no da un numero real")

        try:
            return x ** y
        except OverflowError:
            raise TypeError("El resultado es demasiado grande")

    # Operaciones con un numero

    def sqrt(self, x):
        self.check_type(x)
        if x < 0:
            raise TypeError("No se puede calcular la raiz cuadrada de un numero negativo")

        return math.sqrt(x)

    def log10(self, x):
        self.check_type(x)
        if x <= 0:
            raise TypeError("El logaritmo solo existe para numeros mayores que 0")

        return math.log10(x)

    # Validaciones

    @staticmethod
    def check_type(x):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("Parameters must be numbers")

    @staticmethod
    def check_types(x, y):
        Calculator.check_type(x)
        Calculator.check_type(y)


if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
