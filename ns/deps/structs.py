from ns.deps.errors import DependencyError, ErrorCodes


class Register:
    def __init__(self, not_rewrite: bool = True):
        self.data = {}
        self.not_rewrite = not_rewrite

    def get(self, item):
        if item not in self.data:
            raise DependencyError(ErrorCodes.ITEM_NOT_FOUND, item=item)
        return self.data[item]

    def set(self, item, value):
        if self.not_rewrite and item in self.data:
            raise DependencyError(ErrorCodes.ITEM_REGISTERED_YET, item=item)
        self.data[item] = value

    def update(self, d: dict):
        self.data.update(d)

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()
