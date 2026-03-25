import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np
from deepface import DeepFace
import threading
import os

class EmotionDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EmotionVision")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2c3e50")
        
        self.current_image = None
        self.photo_image = None
        self.emotions_data = None
        self.is_processing = False
        
        self.setup_ui()
        self.update_status("Listo. Carga una imagen.")
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para imagen
        self.image_canvas = tk.Canvas(main_frame, bg="#34495e", width=500, height=400)
        self.image_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.image_canvas.create_text(250, 200, text="Sin imagen", fill="white")
        
        # Panel derecho
        right_panel = tk.Frame(main_frame, bg="#34495e")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones
        self.load_btn = tk.Button(right_panel, text="Cargar Foto", command=self.load_image, bg="#3498db", fg="white", font=("Arial", 12))
        self.load_btn.pack(pady=10, fill=tk.X)
        
        self.analyze_btn = tk.Button(right_panel, text="Analizar", command=self.analyze_image, bg="#e74c3c", fg="white", font=("Arial", 12), state=tk.DISABLED)
        self.analyze_btn.pack(pady=10, fill=tk.X)
        
        # Resultado
        self.result_label = tk.Label(right_panel, text="Emocion Dominante: ---", bg="#34495e", fg="white", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=20)
        
        self.status_label = tk.Label(right_panel, text="Estado: Listo", bg="#34495e", fg="#27ae60")
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(right_panel, mode='indeterminate', length=200)
    
    def update_status(self, msg, is_error=False):
        color = "#e74c3c" if is_error else "#27ae60"
        self.status_label.config(text=f"Estado: {msg}", fg=color)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.current_image = Image.open(file_path)
                display = self.current_image.copy()
                display.thumbnail((480, 380))
                self.photo_image = ImageTk.PhotoImage(display)
                self.image_canvas.delete("all")
                self.image_canvas.create_image(250, 200, image=self.photo_image)
                self.analyze_btn.config(state=tk.NORMAL)
                self.update_status(f"Imagen cargada: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def analyze_image(self):
        if not self.current_image:
            return
        
        self.is_processing = True
        self.analyze_btn.config(state=tk.DISABLED)
        self.load_btn.config(state=tk.DISABLED)
        self.progress.pack(pady=10)
        self.progress.start()
        self.update_status("Analizando...")
        
        thread = threading.Thread(target=self._analyze_thread)
        thread.daemon = True
        thread.start()
    
    def _analyze_thread(self):
        try:
            img = np.array(self.current_image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            result = DeepFace.analyze(img_path=img, actions=['emotion'], enforce_detection=True)
            self.emotions_data = result[0] if isinstance(result, list) else result
            self.root.after(0, self._update_results)
        except Exception as e:
            error_msg = str(e)
            if "face" in error_msg.lower():
                self.root.after(0, lambda: messagebox.showwarning("Error", "No se detecto ningun rostro"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.update_status("Error", True))
        finally:
            self.root.after(0, self._finish_analysis)
    
    def _update_results(self):
        if self.emotions_data:
            emotions = self.emotions_data.get('emotion', {})
            if emotions:
                dominant = max(emotions, key=emotions.get)
                trans = {'happy':'FELIZ','sad':'TRISTE','angry':'ENFADADO','surprise':'SORPRESA','fear':'MIEDO','disgust':'ASCO','neutral':'NEUTRAL'}
                self.result_label.config(text=f"Emocion Dominante: {trans.get(dominant, dominant)} ({emotions[dominant]:.1f}%)")
                self.update_status("Analisis completado")
    
    def _finish_analysis(self):
        self.is_processing = False
        self.analyze_btn.config(state=tk.NORMAL)
        self.load_btn.config(state=tk.NORMAL)
        self.progress.stop()
        self.progress.pack_forget()

def main():
    root = tk.Tk()
    app = EmotionDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()