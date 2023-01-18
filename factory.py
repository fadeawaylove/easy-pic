from typing import Dict, Callable


class CommonFactory(object):

    def __init__(self, callable_type=None) -> None:
        """
        callable_type: 可调用对象的类型（自定义类，方法）
        """
        self._callable_type = callable_type
        self._factory: Dict[str, callable_type or Callable] = {}

    def _check_stuff(self, callable_obj):
        if not callable(callable_obj):
            raise Exception("传入对象不可调用")
        # 子类或者类的实例
        if self._callable_type and (not isinstance(callable_obj, self._callable_type) and
                                    not issubclass(callable_obj, self._callable_type)):
            raise Exception("传入对象类型不匹配")

    def register(self, key, callable_obj):
        self._check_stuff(callable_obj)
        self._factory[key] = callable_obj

    def deco_register(self, key):

        def _wrapped(cls_or_method):
            self.register(key, cls_or_method)
            return cls_or_method

        return _wrapped

    def deco_register_many(self, key_list):

        def _wrapped(cls_or_method):
            for key in key_list:
                self.register(key, cls_or_method)
            return cls_or_method

        return _wrapped

    def factory_data_copy(self) -> dict:
        return self._factory

    def merge(self, factory_obj):
        self._factory.update(factory_obj.factory_data_copy())

    def unregister(self, key):
        self._factory.pop(key, None)

    def get_stuff(self, key):
        return self._factory.get(key)
