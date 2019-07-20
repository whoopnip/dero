

class EqOnAttrsMixin:
    equal_attrs = None

    def __eq__(self, other):
        if self.equal_attrs is None:
            return self == other

        for equal_attr in self.equal_attrs:
            if not hasattr(other, equal_attr): # other object doesn't have this property, must not be equal
                return False
            if getattr(self, equal_attr) != getattr(other, equal_attr):
                return False

        # passed all checks, must be equal
        return True


class EqOnAttrsWithConversionMixin(EqOnAttrsMixin):
    convert_type = str

    def __eq__(self, other):
        if self.equal_attrs is None:
            return self == other

        for equal_attr in self.equal_attrs:
            if not hasattr(other, equal_attr): # other object doesn't have this property, must not be equal
                return False
            if self.convert_type(getattr(self, equal_attr)) != self.convert_type(getattr(other, equal_attr)):
                return False

        # passed all checks, must be equal
        return True


class EqHashMixin:
    equal_attrs = None

    def __hash__(self):
        return hash(tuple([getattr(self, attr) for attr in self.equal_attrs]))