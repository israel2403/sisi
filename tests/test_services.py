"""
Pytest unit tests for services.py
"""

import pytest

from repository import PacienteRepository
from services import PacienteService

from model import (
    PacientePediatrico,
    MedicionTemperatura,
    MedicionFrecuenciaCardiaca,
    MedicionPeso,
    MedicionTalla,
)


@pytest.fixture
def service(tmp_path):
    """
    Create isolated repository and service.
    """
    test_file = tmp_path / "test_pacientes.pkl"

    repository = PacienteRepository(file_path=str(test_file))

    return PacienteService(repository)


@pytest.fixture
def paciente():
    paciente = PacientePediatrico(
        "Juan",
        10,
        tutor="Maria",
    )

    paciente.agregar_medicion(MedicionTemperatura(36.5))

    paciente.agregar_medicion(MedicionTemperatura(37.5))

    paciente.agregar_medicion(MedicionFrecuenciaCardiaca(90))

    paciente.agregar_medicion(MedicionPeso(30))

    paciente.agregar_medicion(MedicionTalla(140))

    return paciente


def test_obtene_pacientes_vacio(service):
    assert service.obtener_pacientes() == []


def test_registrar_paciente(service, paciente):
    service.registrar_paciente(paciente)

    pacientes = service.obtener_pacientes()

    assert len(pacientes) == 1


def test_contar_pacientes(service, paciente):
    service.registrar_paciente(paciente)

    assert service.contar_pacientes() == 1


def test_contar_mediciones_totales(service, paciente):
    service.registrar_paciente(paciente)

    assert service.contar_mediciones_totales() == 5


def test_obtener_todas_las_mediciones(service, paciente):
    service.registrar_paciente(paciente)

    mediciones = service.obtener_todas_las_mediciones()

    assert len(mediciones) == 5

def test_filtrar_mediciones_por_tipo(service, paciente):
    service.registrar_paciente(paciente)

    temperaturas = service.filtrar_mediciones_por_tipo(
        MedicionTemperatura
    )

    assert len(temperaturas) == 2

    assert all(
        isinstance(t, MedicionTemperatura)
        for t in temperaturas
    )

def test_calcular_promedio_por_tipo(service, paciente):
    service.registrar_paciente(paciente)

    promedio = service.calcular_promedio_por_tipo(
        MedicionTemperatura
    )

    assert promedio == pytest.approx(37.0)

def test_calcular_promedio_sin_mediciones(service):
    promedio = service.calcular_promedio_por_tipo(
        MedicionTemperatura
    )

    assert promedio is None 
def test_obtener_estadisticas_generales(
    service,
    paciente
):
    service.registrar_paciente(paciente)

    stats = service.obtener_estadisticas_generales()

    assert stats["total_pacientes"] == 1
    assert stats["total_mediciones"] == 5
    assert stats["promedio_temperatura"] == pytest.approx(
        37.0
    )

def test_limpiar_datos(service, paciente):
    service.registrar_paciente(paciente)

    service.limpiar_datos()

    assert service.contar_pacientes() == 0


def test_registrar_paciente_invalido(service):
    with pytest.raises(TypeError):
        service.registrar_paciente("not a patient")


def test_filtrar_mediciones_tipo_invalido(service):
    with pytest.raises(TypeError):
        service.filtrar_mediciones_por_tipo(
            "not a type"
        )
