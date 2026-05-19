"""
Repository module for the SISI project.

This module is responsible only for persistence.
It saves and loads PacientePediatico objects using pickle.

It should not contain GUI code, validation logic, or business rules.
"""

import pickle
from pathlib import Path

from config import DATA_FILE
from model import PacientePediatrico


class PacienteRepository:
    """
    Repository responsible for saving and loading pediatric patients.

    This classworks like a DAO / Repository in Java:
    it hides the persistence details from the rest of the application.
    """

    def __init__(self, file_path: Path | str | None = None) -> None:
        """
        Creates a repository.

        Args:
            file_path: Optional custom pickle file path.
                       Useful for tests.
        """
        self.file_path = Path(file_path) if file_path is not None else DATA_FILE

    def load_all(self) -> list[PacientePediatrico]:
        """
        Load all patients fro pickle file.

        Returns:
            A list of PacientePediatrico objects.
            If the file does not exist or is empty, returns an empty list.
        """
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "rb") as file:
                pacientes = pickle.load(file)

                if not isinstance(pacientes, list):
                    return []

                return pacientes
        except EOFError:
            return []

    def save_all(self, pacientes: list[PacientePediatrico]) -> None:
        """
        Save the full list of patients into the pickle file.

        Args:
            pacientes: List of PacientePediatrico objects.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "wb") as file:
            pickle.dump(pacientes, file)

    def add(self, paciente: PacientePediatrico) -> None:
        """
        Add a new patient and ave the updated list.

        Args:
            paciente: PacientePediatrico object to save.

        Raises:
            TypeError: If paciente is not a PacientePediatrico.
        """
        if not isinstance(paciente, PacientePediatrico):
            raise TypeError("paciente must be an instance of PacientePediatrico")

        pacientes = self.load_all()
        pacientes.append(paciente)
        self.save_all(pacientes)

    def clear(self) -> None:
        """
        Clear all saved patients.
        """
        self.save_all([])
