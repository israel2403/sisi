"""
Domain model classes for the SISI project.

This module defines the main objects of the application:

- Persona: abstract base class.
- PacientePediatrico: concrete patient class.
- Medicion: abstract base class for mesurements.
- MedicionFrecuenciaCardiaca
- MedicionPeso
- MedicionTalla
"""

from abc import ABC, abstractmethod
from datetime import datetime

from validators import (
    validate_age,
    validate_non_negative_number,
    validate_not_empty,
    validate_positive_number,
)


class Persona(ABC):
    """
    Abstract base class that represents a generic person.

    In java terms, this is similar to an abstract class.
    It cannot be instantiated directly.
    """

    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad

    @property
    def nombre(self) -> str:
        """Return th person's name."""
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        """Set and validate the person's name."""
        self._nombre = validate_not_empty(value, "Name")

    @property
    def edad(self) -> int:
        """Return the person's age."""
        return self._edad

    @edad.setter
    def edad(self, value: int) -> None:
        """Set and validate the person's age."""
        self._edad = validate_age(value)

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Return a text su7mmary of tnhe person."""
        pass


class PacientePediatrico(Persona):
    """
    Represents a pediatric patient.

    This class inherits from Persona and adds patient-specific information.
    """

    def __init__(self, nombre: str, edad: int, tutor: str):
        super().__init__(nombre, edad)
        self.tutor = tutor
        self.mediciones = []

    @property
    def tutor(self) -> str:
        """Return the patient's tutor name."""
        return self._tutor

    @tutor.setter
    def tutor(self, value: str) -> None:
        """Set and validate the patient's tutor name."""
        self._tutor = validate_not_empty(value, "Tutor")

    def agregar_medicion(self, medicion: "Medicion") -> None:
        """Add a mesurement to the patient."""
        if not isinstance(medicion, Medicion):
            raise TypeError("Only fmedicion objects can be added.")
        self.mediciones.append(medicion)

    def obtener_resumen(self) -> str:
        """Return a summary of the pediatric patient."""
        return (
            f"Patient: {self.nombre}, "
            f"Age: {self.edad}, "
            f"Tutor: {self.tutor}, "
            f"Measurements: {len(self.mediciones)}"
        )

    def __repr__(self) -> str:
        return (
            f"PacientePediatrico("
            f"nombre={self.nombre!r}, "
            f"edad={self.edad!r}, "
            f"tutor={self.tutor!r})"
        )


class Medicion(ABC):
    """
    Abstract base class for all measurements.

    Every measurement has:
    - value
    - unit
    - date/time
    Concrete child classes must implement interpretar().
    """

    def __init__(self, valor: float, unidad: str, fecha: datetime | None = None):
        self.valor = valor
        self.unidad = unidad
        self.fecha = fecha if fecha is not None else datetime.now()

    @property
    def valor(self) -> float:
        """Return the measurement value."""
        return self._valor

    @valor.setter
    def valor(self, value: float) -> None:
        """Set and validate the measurement value."""
        self._valor = validate_non_negative_number(value, "Measurement value")

    @property
    def unidad(self) -> str:
        """Return the measurement unit."""
        return self._unidad

    @unidad.setter
    def unidad(self, value: str) -> None:
        """Set and validate the measurement unit."""
        self._unidad = validate_not_empty(value, "Unit")

    @property
    def fecha(self) -> datetime:
        """Return the measurment date."""
        return self._fecha

    @fecha.setter
    def fecha(self, value: datetime) -> None:
        """Set and validate the measurment date."""
        if not isinstance(value, datetime):
            raise ValueError("Date must be  datetime object.")
        self._fecha = value

    @abstractmethod
    def interpretar(self) -> str:
        """Return a simple interpretation of the measurement."""
        pass

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"valor={self.valor!r}, "
            f"unidad={self.unidad!r}, "
            f"fecha={self.fecha!r})"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}: "
            f"{self.valor} {self.unidad} - "
            f"{self.interpretar()}"
        )


class MedicionFrecuenciaCardiaca(Medicion):
    """Represents a heart rate measurement."""

    def __init__(self, valor: float, fecha: datetime | None = None):
        super().__init__(valor, "bpm", fecha)

    def interpretar(self) -> str:
        if self.valor < 60:
            return "Low heart rate"
        if self.valor <= 100:
            return "Normal heart rate"
        return "High heart rate"


class MedicionTemperatura(Medicion):
    """Represetns a body temperature measurement."""

    def __init__(self, valor: float, fecha: datetime | None = None):
        super().__init__(valor, "°C", fecha)

    @Medicion.valor.setter
    def valor(self, value: float) -> None:
        self._valor = validate_positive_number(value, "Temperature")

    def interpretar(self) -> str:
        if self.valor < 36.0:
            return "Low temperature"
        if self.valor <= 37.5:
            return "Normal temperature"
        return "Possible fever"


class MedicionPeso(Medicion):
    """Represents a body weight measurement."""

    def __init__(self, valor: float, fecha: datetime | None = None):
        super().__init__(valor, "kg", fecha)

    @Medicion.valor.setter
    def valor(self, value: float) -> None:
        self._valor = validate_positive_number(value, "Weight")

    def interpretar(self) -> str:
        if self.valor < 10:
            return "Low weight range"
        if self.valor <= 40:
            return "Expected pediatric weight range"
        return "High weight range"


class MedicionTalla(Medicion):
    """Represents a height measurement."""

    def __init__(self, valor: float, fecha: datetime | None = None):
        super().__init__(valor, "cm", fecha)

    @Medicion.valor.setter
    def valor(self, value: float) -> None:
        self._valor = validate_positive_number(value, "Height")

    def interpretar(self) -> str:
        if self.valor < 80:
            return "Low height range"
        if self.valor <= 170:
            return "Expected pediatric height range"
        return "High Height range"
