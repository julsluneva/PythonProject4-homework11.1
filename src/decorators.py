import datetime
from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем имя функции
            func_name = func.__name__

            # Получаем текущее время
            call_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Логируем в файл или консоль
            def write_log(message):
                if filename:
                    with open(filename, "a", encoding="UTF-8") as f:
                        f.write(message)
                else:
                    print(message, end="")

            try:
                # Вызываем функцию и получаем результат
                result = func(*args, **kwargs)
                # Составляем сообщение об успешном выполнении
                write_log(f"{call_time} - {func_name} ok\n")
                return result
            except Exception as e:
                write_log(f"{call_time} - {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n")
                raise
        return wrapper
    return decorator

@log()
def my_function(x,y):
    return x + y

my_function(1, 2)

if __name__ ="__main__":
    print(my_function(1, 2))
