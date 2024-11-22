def strict(func):
    """
    Декоратор, который проверяет соответствие типов аргументов функции их аннотациям, указанным в прототипе функции.

    Если тип аргумента не соответствует ожидаемому типу, выбрасывается исключение TypeError.
    :param func: Декорируемая функция
    :return: обернутая функция с проверкой типов
    """

    def wrapper(*args):
        """
        Обертка для декорируемой функции, выполняющая проверку типов аргументов.

        :param args: Позиционные аргументы, переданные в функцию.
        :return: Результат вызова декорируемой функции (при успешной проверки типов).
        :raises TypeError: Если тип переданного аргумента не соответствует указанному в аннотации.
        """
        for arg_name, arg_value in zip(func.__annotations__, args):
            expected_type = func.__annotations__[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Argument {arg_name} must be of type {expected_type.__name__}, "
                    f"but got {type(arg_value).__name__}"
                )
        return func(*args)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
