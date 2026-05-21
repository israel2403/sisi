"""
Manual integration test for Phase 3 services.
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from repository import PacienteRepository
from services import PacienteService

from model import (
    PacientePediatrico,
    MedicionTemperatura,
    MedicionFrecuenciaCardiaca,
    MedicionPeso,
    MedicionTalla,
)


def main():
    tmp = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False)
    tmp.close()
    repository = PacienteRepository(file_path=tmp.name)

    service = PacienteService(repository)

    # Clear old data
    service.limpiar_datos()

    paciente1 = PacientePediatrico(
        "Juan",
        10,
        tutor="Carlos",
    )

    paciente1.agregar_medicion(MedicionTemperatura(36.5))

    paciente1.agregar_medicion(MedicionFrecuenciaCardiaca(88))

    paciente1.agregar_medicion(MedicionPeso(30))

    paciente1.agregar_medicion(MedicionTalla(140))

    paciente2 = PacientePediatrico(
        "Maria",
        8,
        tutor="Ana",
    )

    paciente2.agregar_medicion(MedicionTemperatura(37.2))

    paciente2.agregar_medicion(MedicionFrecuenciaCardiaca(92))

    paciente2.agregar_medicion(MedicionPeso(28))

    paciente2.agregar_medicion(MedicionTalla(132))

    service.registrar_paciente(paciente1)
    service.registrar_paciente(paciente2)

    print("\nPACIENTES:")
    print(service.obtener_pacientes())

    print("\nTOTAL PACIENTES:")
    print(service.contar_pacientes())

    print("\nTOTAL MEDICIONES:")
    print(service.contar_mediciones_totales())

    print("\nPROMEDIO TEMPERATURA:")
    print(service.calcular_promedio_por_tipo(MedicionTemperatura))

    print("\nPROMEDIO PESO:")
    print(service.calcular_promedio_por_tipo(MedicionPeso))

    print("\nESTADISTICAS GENERALES:")
    print(service.obtener_estadisticas_generales())

    print("\nCleaning up temp file...")
    Path(tmp.name).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
