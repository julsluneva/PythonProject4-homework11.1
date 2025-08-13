from datetime import datetime

import pytest

from src.decorators import log


# Очистка тестовых файлов
@pytest.fixture(autouse=True)
def cleanup(request, tmp_path):
    def remove_test_files():
        test_file = tmp_path / "test.log"
        if test_file.exists():
            test_file.unlink()

    request.addfinalizer(remove_test_files)


def test_log_decorator_console_output_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    # Проверка работы функции
    assert result == 5
    # Проверка вывода в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out
    # Проверка формата времени
    log_time_str = captured.out.split(" - ")[0]
    try:
        datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail("Неверный формат времени")


def test_log_decorator_concole_output_error(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


# Проверка с выводом в файл
def test_log_decorator_file_output_success(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)

    # Проверка работы функции
    assert result == 12

    # Проверка записи в файл
    with open(log_file, "r") as f:
        content = f.read()
        assert "multiply ok" in content


def test_log_decorator_file_output_error(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def fail_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail_function()

    # Проверяем запись в файл
    with open(log_file, "r") as f:
        content = f.read()
        assert "fail_function error: ValueError" in content


# Проверяем сохранение метаданных в функции
def test_log_decorator_preserves_metadata():
    @log()
    def sample_func(a: int, b: int) -> int:
        """Функция для тестирования"""
        return a + b

    assert sample_func.__name__ == "sample_func"
    assert sample_func.__doc__ == "Функция для тестирования"
    assert sample_func.__annotations__ == {"a": int, "b": int, "return": int}


# Проверяем логирование с аргументами-ключами
def test_decorator_log_with_kwargs(capsys):
    @log()
    def greet(name, title="Mr"):
        return f"Hello, {title} {name}"

    result = greet("Smith", title="Dr")

    # Проверяем работу функции
    assert result == "Hello, Dr Smith"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_decorator_log_with_kwargs_error(capsys):
    @log()
    def failing_kwargs_function(a, b=0):
        return a / b

    with pytest.raises(ZeroDivisionError):
        failing_kwargs_function(1, b=0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "failing_kwargs_function error: ZeroDivisionError" in captured.out
    assert "Inputs: (1,), {'b': 0}" in captured.out
