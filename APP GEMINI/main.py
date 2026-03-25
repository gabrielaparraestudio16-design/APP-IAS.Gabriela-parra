import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from deepface import DeepFace

# Configuraci??n de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EmotionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Emotion Detector - DeepFace")
        self.geometry("1000x700")

        # Diccionario de traducci??n
        self.emociones_es = {
            "angry": "Enojado",
            "disgust": "Disgustado",
            "fear": "Miedo",
            "happy": "Feliz",
            "sad": "Triste",
            "surprise": "Sorprendido",
            "neutral": "Neutral"
        }

        self.path_imagen = None
        self.setup_ui()

    def setup_ui(self):
        """Configura el layout de la interfaz"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Panel Lateral) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="EMO-SCAN v1.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=30)

        self.btn_cargar = ctk.CTkButton(self.sidebar, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_cargar.pack(pady=15, padx=20)

        self.btn_analizar = ctk.CTkButton(self.sidebar, text="Analizar Emociones", 
                                          fg_color="#2ecc71", hover_color="#27ae60",
                                          command=self.analizar_emocion)
        self.btn_analizar.pack(pady=15, padx=20)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Resultados:", font=ctk.CTkFont(size=14, weight="bold"))
        self.info_label.pack(pady=(30, 10))

        self.txt_resultados = ctk.CTkTextbox(self.sidebar, width=200, height=250)
        self.txt_resultados.pack(pady=10, padx=20)

        # --- ??rea Principal (Imagen) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.image_label = ctk.CTkLabel(self.main_frame, text="No se ha cargado ninguna imagen", 
                                        fg_color="#2b2b2b", corner_radius=10)
        self.image_label.pack(expand=True, fill="both")

    def cargar_imagen(self):
        """Abre el explorador de archivos y muestra la imagen original"""
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png")])
        
        if file_path:
            self.path_imagen = file_path
            img = Image.open(file_path)
            self.mostrar_imagen(img)
            self.txt_resultados.delete("0.0", "end")

    def mostrar_imagen(self, pil_img):
        """Ajusta y muestra la imagen en el contenedor"""
        # Redimensionar manteniendo aspecto
        width, height = pil_img.size
        ratio = min(700/width, 550/height)
        new_size = (int(width*ratio), int(height*ratio))
        
        img_resized = pil_img.resize(new_size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_resized)
        
        self.image_label.configure(image=tk_img, text="")
        self.image_label.image = tk_img

    def analizar_emocion(self):
        """Procesa la imagen con DeepFace"""
        if not self.path_imagen:
            messagebox.showwarning("Advertencia", "Por favor, carga una imagen primero.")
            return

        try:
            # Analizar con DeepFace (Detector OpenCV es m??s r??pido para UI)
            results = DeepFace.analyze(img_path=self.path_imagen, 
                                       actions=['emotion'],
                                       enforce_detection=True,
                                       detector_backend='opencv')
            
            # Cargar imagen con OpenCV para dibujar el rect??ngulo
            img_cv = cv2.imread(self.path_imagen)
            res_texto = ""

            for face in results:
                # Obtener coordenadas del rostro
                region = face['region']
                x, y, w, h = region['x'], region['y'], region['w'], region['h']
                
                # Dibujar rect??ngulo y etiqueta
                dominante = face['dominant_emotion']
                es_dominante = self.emociones_es.get(dominante, dominante)
                
                cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img_cv, es_dominante, (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Compilar porcentajes
                res_texto += f"Dominante: {es_dominante.upper()}\n"
                res_texto += "-"*20 + "\n"
                for emo, valor in face['emotion'].items():
                    nombre = self.emociones_es.get(emo, emo)
                    res_texto += f"{nombre}: {valor:.1f}%\n"
                res_texto += "\n"

            # Convertir de BGR a RGB y mostrar
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            self.mostrar_imagen(Image.fromarray(img_rgb))
            
            # Mostrar texto
            self.txt_resultados.delete("0.0", "end")
            self.txt_resultados.insert("0.0", res_texto)

        except ValueError:
            messagebox.showerror("Error", "No se detect?? ning??n rostro en la imagen.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurri?? un error inesperado: {str(e)}")

if __name__ == "__main__":
    app = EmotionApp()
    app.mainloop()
