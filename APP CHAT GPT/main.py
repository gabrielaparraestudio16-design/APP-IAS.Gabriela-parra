
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from deepface import DeepFace

class EmotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Emociones")
        self.root.geometry("800x600")
        self.image_path = None

        self.create_widgets()

    def create_widgets(self):
        self.btn_load = tk.Button(self.root, text="Cargar Imagen", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_analyze = tk.Button(self.root, text="Analizar Emocion", command=self.analyze_image)
        self.btn_analyze.pack(pady=10)

        self.canvas = tk.Label(self.root)
        self.canvas.pack()

        self.result_text = tk.Text(self.root, height=10)
        self.result_text.pack(pady=10)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((400, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.tk_img)

    def analyze_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return

        try:
            result = DeepFace.analyze(self.image_path, actions=['emotion'])
            emotions = result[0]['emotion']
            dominant = result[0]['dominant_emotion']

            # Draw bounding box
            img = Image.open(self.image_path)
            draw = ImageDraw.Draw(img)
            region = result[0]['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            draw.rectangle([x, y, x+w, y+h], outline="red", width=3)

            img = img.resize((400, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.tk_img)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Emocion dominante: {dominant}\n\n")

            for emo, val in emotions.items():
                self.result_text.insert(tk.END, f"{emo}: {val:.2f}%\n")

        except Exception as e:
            messagebox.showerror("Error", "No se detecto ningun rostro o hubo un problema.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionApp(root)
    root.mainloop()
