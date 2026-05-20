"""
services.py

Business logic layer for the SISI project.

This module contains the PacienteService class, which:
- communicates with the repository layer
- performs statistics calculations
- applies business rules
- remains independent from GUI frameworks like tkinter

Author: Isra
"""

from typing import Optional

from repository import PacienteRepository
from model import (
    PacientePediatrico,
    MedicionTemperatura,
    MedicionFrecuenciaCardiaca,
    MedicionPeso,
    MedicionTalla,
)


class PacienteService:
    """
    Service layer for patient operations and statictics.

    This class acts as an intemediate layer between:
    - GUI (future tkinter layer)
    - repository persistence layer

    Similar to a Spring Service in Java.
    """

    def __init__(self, repository: Optional[PacienteRepository] = None):
        """
        Initialize the service.

        Args:
            repository:
                Optional repository dependency.
                If not provided, a default PacienteRepository is created.
        """
        self._repository = repository or PacienteRepository()

    def obtener_pacientes(self) -> list:
        """
        Return all stored patients.

        Returns:
            list: list of PacientePediatrico objects
        """
        return self._repository.load_all()

    def registrar_paciente(self, paciente: PacientePediatrico) -> None:
        """
        Register and persist a patient.

        Args:
            paciente:
                Patient instanced to save.

        Raises:
            TypeError:
                If paciente is not a PacientePediatrico instance.
        """
        if not isinstance(paciente, PacientePediatrico):
            raise TypeError("paciente must be an instance of PacientePediatrico")
        self._repository.add(paciente)

    def contar_pacientes(self) -> int:
        """
        Count total patients.

        Returns:
            int: total patients
        """
        return len(self.obtener_pacientes())

    def contar_mediciones_totales(self) -> int:
        """
        Count all measurements across all patients.

        Returns:
            int: total measurements
        """
        total = 0

        for paciente in self.obtener_pacientes():
            total += len(paciente.mediciones)

        return total

    def obtener_todas_las_mediciones(self) -> list:
        """
        Return all measurements from all patients in  a flat t.

        Returns:
            list: all measurement objects
        """
        mediciones = []

        for paciente in self.obtener_pacientes():
            mediciones.extend(paciente.mediciones)

        return mediciones

    def filtrar_mediciones_por_tipo(
        self,
        tipo_medicion: type,
    ) -> list:
        """
        Filter measurements by measurement class.

        Example:
            service.filtar_mediciones_por_tipo(
                MedicionTemperatura
            )

        Args:
            tipo_medicion:
                Measurement class type.

        Returns:
            list: filtered measurements

        Raises:
            TypeError:
                if tipo_medicion is not a class/type.
        """
        if not isinstance(tipo_medicion, type):
            raise TypeError("tipo_medicion must be a class/type")

        return [
            medicion
            for medicion in self.obtener_todas_las_mediciones()
            if isinstance(medicion, tipo_medicion)
        ]

    def calcular_promedio_por_tipo(
        self,
        tipo_medicion: type,
    ) -> float | None:
        """
        Calculate average value for a measurment type.

        Args:
            tipo_medicion:
                Measurement class type.

        Returns:
            float | None:
                Average value or None if no measurments exist.
        """
        mediciones = self.filtrar_mediciones_por_tipo(tipo_medicion)

        if not mediciones:
            return None

        suma = sum(medicion.valor for medicion in mediciones)

        return suma / len(mediciones)

    def obtener_estadisticas_generales(self) -> dict:
        """
        Build a statistics summary dictionary.

        Returns:
            dict: statistics dictionary
        """
        return {
            "total_pacientes": self.contar_pacientes(),
            "total_mediciones": self.contar_mediciones_totales(),
            "promedio_frecuencia_cardiaca": self.calcular_promedio_por_tipo(
                MedicionFrecuenciaCardiaca
            ),
            "promedio_temperatura": self.calcular_promedio_por_tipo(
                MedicionTemperatura
            ),
            "promedio_peso": self.calcular_promedio_por_tipo(MedicionPeso),
            "promedio_talla": self.calcular_promedio_por_tipo(MedicionTalla),
        }

    def limpiar_datos(self) -> None:
        """
        Remove all persisted data.
        """
        self._repository.clear()
