class Materials:
    def __init__(self, metal, crystal, deuterium):
        if metal < 0 or crystal < 0 or deuterium < 0:
            raise ValueError('Metal, crystal and deuterium must be positive')

        self.metal = metal
        self.crystal = crystal
        self.deuterium = deuterium

    def __mul__(self, other):
        if type(other) in (int, float):
            return Materials(self.metal * other, self.crystal * other, self.deuterium * other)
        else:
            class_name = type(self).__name__
            raise TypeError(f'Cannot multiply {class_name} with {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        if type(other) == __class__:
            return Materials(self.metal - other.metal, self.crystal - other.crystal, self.deuterium - other.deuterium)
        else:
            class_name = type(self).__name__
            raise TypeError(f'Cannot subtract {class_name} with {type(other)}')

    def __add__(self, other):
        if type(other) == __class__:
            return Materials(self.metal + other.metal, self.crystal + other.crystal, self.deuterium + other.deuterium)
        else:
            raise TypeError(f'Cannot subtract {__class__.__name__} with {type(other)}')

    def __str__(self):
        return f"Materials: (M: {self.metal}, C: {self.crystal}, D: {self.deuterium})"

    def all_less_or_equal(self, other):
        return self.metal <= other.metal and self.crystal <= other.crystal and self.deuterium <= other.deuterium

