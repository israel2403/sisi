"""
SISI - Sistema Infantil de Seguimiento Integral

Phase 4: Tkinter GUI

This file is the presentation layer of the application.
It uses PacienteService for business logic and persistence.
"""

from os import stat
import tkinter as tk
from tkinter import ttk, messagebox

from model import(
    PacientePediatrico,
    MedicionFrecuenciaCardiaca,
    MedicionTemperatura,
    MedicionPeso,
    MedicionTalla,
) 
from repository import PacienteRepository
from services import PacienteService

class SisiApp(tk.Tk):
    """Main Tkinter window for the SISI desktop application."""
    def __init__(self):
        super().__init__()

        self.title("SISI - Pediatric Monitoring System")
        self.geometry("1000x650")

        # The GUI depends on the service, not directly on pickle persistence.
        self.repository = PacienteRepository()
        self.service = PacienteService(self.repository)

        self._create_widgets()
        self.refresh_all()

    def _create_widgets(self):
        """Create and organize all GUI widgets."""

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(main_frame, text="Registrar Paciente", padding=10)
        form_frame.pack(side="left", fill="y", padx=(0, 10))

        list_frame = ttk.LabelFrame(main_frame, text="Pacientes Guardados", padding=10)
        list_frame.pack(side="right", fill="both", expand=True)

        stats_frame = ttk.LabelFrame(self, text="Estadisticas", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))

        self._create_form(form_frame)
        self._create_patient_table(list_frame)
        self._create_statistics(stats_frame)

    def _create_form(self, parent):
        """Create the patient registration form."""

        ttk.Label(parent, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(parent, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(parent, text="Edad:").grid(row=1, column=0, sticky="w")
        self.age_entry = ttk.Entry(parent, width=30)
        self.age_entry.grid(row=1, column=1, pady=5)

        ttk.Label(parent, text="Tutor:").grid(row=2, column=0, sticky="2")
        self.tutor_entry = ttk.Entry(parent, width=30)
        self.tutor_entry.grid(row=2, column=1, pady=5)

        ttk.Separator(parent).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(parent, text="Mediciones opcionales").grid(
            row=4, column=0, columnspan=2, sticky="w"
        )

        ttk.Label(parent, text="Heart rate:").grid(row=5, column=0, sticky="w")
        self.heart_rate_entry = ttk.Entry(parent, width=30)
        self.heart_rate_entry.grid(row=5, column=1, pady=5)

        ttk.Label(parent, text="Temperatura:").grid(row=6, column=0, sticky="w")
        self.temperature_entry = ttk.Entry(parent, width=30)
        self.temperature_entry.grid(row=6, column=1, pady=5)

        ttk.Label(parent, text="Peso").grid(row=7, column=0, sticky="w")
        self.weight_entry = ttk.Entry(parent, width=30)
        self.weight_entry.grid(row=8, column=1, pady=5)

        ttk.Label(parent,text="Altura:").grid(row=7, column=0, sticky="w")
        self.height_entry = ttk.Entry(parent, width=30)
        self.height_entry.grid(row=8, column=1, pady=5)

        ttk.Button(parent, text="Clear Form", command=self.clear_form).grid(
            row=11, column=0, columnspan=2, sticky="ew", pady=(25, 5)
        )

    def _create_patient_table(self, parent):
        """Create the table that displays saved patients."""

        columns = ("name", "age", "tutor", "measurements")

        self.patient_table = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=18
        )

        self.patient_table.heading("name", text="Nombre")
        self.patient_table .heading("age", text="Edad")
        self.patient_table.heading("tutor", text="Tutor")
        self.patient_table.heading("measurements", text="Medidas")

        self.patient_table.column("name", width=180)
        self.patient_table.column("age", width=80)
        self.patient_table.column("measurements", width=180)
        self.patient_table.column("measurements", width=120)

        self.patient_table.pack(fill="both", expand=True)

        self.summary_text = tk.Text(parent, height=8, wrap="word")
        self.summary_text.pack(fill="x", pady=(10, 0))

        self.patient_table.bind("<<TreeviewSelect>>", self.show_selected_patient_summary)
