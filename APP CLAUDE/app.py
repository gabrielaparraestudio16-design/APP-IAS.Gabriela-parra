"""
app.py — Punto de entrada principal de la aplicación.
Inicializa la ventana raíz de Tkinter y lanza el controlador principal.

NOTA DE COMPATIBILIDAD:
    TF_USE_LEGACY_KERAS=1 debe establecerse ANTES de importar tensorflow o
    deepface. Fuerza a TensorFlow >= 2.16 a usar tf-keras (Keras 2 legacy)
    en lugar de Keras 3, que es incompatible con DeepFace.
    Referencia: https://github.com/serengil/deepface/issues/1121
"""

import os

# CRITICO: debe ir antes de cualquier import de TF/DeepFace
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Crea la ventana raíz y arranca el bucle principal de eventos."""
    root = tk.Tk()
    root.title("EmotiScan · Detección de Emociones")
    root.resizable(False, False)

    # Colores base definidos en la raíz para que los widgets los hereden
    root.configure(bg="#0D0D0F")

    app = MainWindow(root)
    app.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
