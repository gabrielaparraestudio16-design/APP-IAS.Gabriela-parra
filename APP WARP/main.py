"""
╔══════════════════════════════════════════════════════╗
║          FaceEmotion Analyzer - v1.0                ║
║   Detección de emociones faciales con DeepFace      ║
╚══════════════════════════════════════════════════════╝

Punto de entrada de la aplicación.
Arquitectura: separación de responsabilidades en módulos cohesionados.
  - ImageLoader   : carga y redimensionado de imágenes.
  - EmotionEngine : análisis de emociones con DeepFace.
  - FaceDrawer    : dibuja bounding-boxes sobre el frame OpenCV.
  - AppUI         : construye y gestiona la interfaz gráfica Tkinter.
"""

import tkinter as tk
from app.ui import AppUI


def main() -> None:
    """Inicializa la ventana raíz y arranca el bucle principal."""
    root = tk.Tk()
    root.resizable(True, True)
    AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
