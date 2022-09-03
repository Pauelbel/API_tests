class Cache:
    """ 
    Класс для передачи данных в кэш, для последущего переиспользования в сценариях тестирования
    Принимает 
    - request, key, value
    """

    def add_cache(request, key, value):
        var_name = [name for name in globals() if globals()[name] is key]
        return request.config.cache.set(f'{var_name}', value)
  
    def get (request, key):
        var_name = [name for name in globals() if globals()[f'{name}'] is key]
        data = request.config.cache.get(f'{var_name}', None)
        return data