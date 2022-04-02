from aiohttp.web import Response, Request


def query_requirements(*args):
    """
    Декоратор для Handler'ов.
    Требует, чтобы каждый элемент args присутствовал в request.query.

    :param args: перечисление требуемых параметров в виде набора строк.
    :return: Response(status=500) в случае отсутствия хотя бы одного из аргументов. Или результат исполнения
    Handler'а в случае их наличия.
    """

    def decorator(func):
        async def wrapper(self, request: Request):
            satisfactory_list = []
            query = request.query.keys()
            for arg in args:
                if arg not in query:
                    satisfactory_list.append(arg)
            if len(satisfactory_list):
                return Response(text=f'Not enough parameters in GET request query! Missing {str(satisfactory_list)}',
                                status=500)
            return await func(self, request)

        return wrapper

    return decorator


def json_requirements(*args):
    """
    Декоратор для Handler'ов post запросов. Требует, чтобы каждый элемент
    args присутствовал в request.json.

    :param args: перечисление требуемых параметров в виде набора строк.
    :return: Response(status=500) в случае отсутствия хотя бы одного из аргументов. Или результат исполнения
    Handler'а в случае их наличия.
    """

    def decorator(func):
        async def wrapper(self, request: Request):
            satisfactory_list = []
            query = await request.json()
            for arg in args:
                if arg not in query:
                    satisfactory_list.append(arg)
            if len(satisfactory_list):
                return Response(text=f'Not enough parameters in POST request JSON! Missing {str(satisfactory_list)}',
                                status=500)
            return await func(self, request)

        return wrapper

    return decorator
