from math import cos, sin
from typing import SupportsFloat, SupportsIndex, TypeAlias

import attr

SupportsFloatOrIndex: TypeAlias = SupportsFloat | SupportsIndex


@attr.s(auto_attribs=True, frozen=True)
class Vector:
    x: float
    y: float

    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return NotImplemented

    def __mul__(self, other: "Vector | SupportsFloatOrIndex") -> "Vector":
        if isinstance(other, (SupportsFloat, SupportsIndex)):
            return Vector(self.x * float(other), self.y * float(other))

        return NotImplemented

    def rotate(self, theta: SupportsFloatOrIndex) -> "Vector":
        sin_theta = sin(theta)
        cos_theta = cos(theta)
        return Vector(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta,
        )
