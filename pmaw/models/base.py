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

    @classmethod
    def from_data(cls, messari, data):
        return cls(messari, _data=data)


class MessariBase(PMAWBase):

    def __init__(self, messari, _data=None, _fetched=False, _str_field=True):
        super().__init__(messari, _data=_data)

        self._fetched = _fetched

        if _str_field and self.STR_FIELD not in self.__dict__:
            raise ValueError

    def _fetch(self):
        self._fetched = True

    def _reset_attributes(self, *attributes):
        for attribute in attributes:
            if attribute in self.__dict__:
                del self.__dict__[attribute]
        self._fetched = False

    def __eq__(self, other):
        if isinstance(other, str):
            return other.lower() == str(self).lower()
        return isinstance(other, self.__class__) and str(self.lower() == str(other).lower())

    def __ne__(self, other):
        return not self == other

    def __getattr__(self, attribute):
        if not attribute.startswith("_") and not self._fetched:
            self._fetch()
            return getattr(self, attribute)
        raise AttributeError

    def __hash__(self):
        return hash(self.__class__.__name__) ^ hash(str(self).lower())
