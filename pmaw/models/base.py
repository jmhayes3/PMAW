from copy import deepcopy


class PMAWBase:

    def __init__(self, messari, _data=None):
        self._messari = messari

        if _data:
            for attribute, value in _data.items():
                setattr(self, attribute, value)

    @staticmethod
    def _safely_add_arguments(argument_dict, key, **new_arguments):
        value = deepcopy(argument_dict[key]) if key in argument_dict else {}
        value.update(new_arguments)
        argument_dict[key] = value

    @staticmethod
    def _safely_add_argument(argument_dict, key, new_key, new_value):
        value = deepcopy(argument_dict[key]) if key in argument_dict else {}
        value.update({new_key: new_value})
        argument_dict[key] = value

    @classmethod
    def from_data(cls, messari, data):
        return cls(messari, _data=data)


class MessariBase(PMAWBase):

    def __init__(self, messari, _data=None, _fetched=False):
        super().__init__(messari, _data=_data)

        self._fetched = _fetched

    def __getattr__(self, attribute):
        if not attribute.startswith("_") and not self._fetched:
            self._fetch()
            return getattr(self, attribute)
        raise AttributeError

    def _fetch(self):
        self._fetched = True

    def _reset_attributes(self, *attributes):
        for attribute in attributes:
            if attribute in self.__dict__:
                del self.__dict__[attribute]
        self._fetched = False
