"""
Manual test for Phase 2: repository.py and pickle persistence.

Run from the project root with:

    python tests/manual_test_phase2_repository.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tempfile

from repository import PacienteRepository
from model import (
    PacientePediatrico,
    MedicionFrecuenciaCardiaca,
    MedicionTemperatura,
    MedicionPeso,
    MedicionTalla,
)


def main() -> None:
    tmp = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False)
    tmp.close()
    repository = PacienteRepository(file_path=tmp.name)

    print("Clearing previous data...")
    repository.clear()

    print("Creating patient...")

    paciente = PacientePediatrico(
        nombre="Juan Perez",
        edad=8,
        tutor="Maria Perez",
    )

    print("Adding measurements...")

    paciente.agregar_medicion(MedicionFrecuenciaCardiaca(95))
    paciente.agregar_medicion(MedicionTemperatura(36.8))
    paciente.agregar_medicion(MedicionPeso(28.5))
    paciente.agregar_medicion(MedicionTalla(125))

    print("Saving patient with repository.add(...)...")
    repository.add(paciente)

    print("Loading patients from pickle file...")
    pacientes = repository.load_all()

    print("\nLoaded patients:")
    for loaded_paciente in pacientes:
        print(loaded_paciente)

        print("Measurements:")
        for medicion in loaded_paciente.mediciones:
            print(f" - {medicion}")

    print("\nCleaning up temp file...")
    Path(tmp.name).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
