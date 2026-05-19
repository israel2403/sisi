import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model import (
    PacientePediatrico,
    MedicionFrecuenciaCardiaca,
    MedicionTemperatura,
    MedicionPeso,
    MedicionTalla,
)

paciente = PacientePediatrico(nombre="Luis Perez", edad=8, tutor="Maria Perez")

paciente.agregar_medicion(MedicionFrecuenciaCardiaca(88))
paciente.agregar_medicion(MedicionTemperatura(37.2))
paciente.agregar_medicion(MedicionPeso(25.5))
paciente.agregar_medicion(MedicionTalla(124))

print(paciente)

for medicion in paciente.mediciones:
    print(medicion)
