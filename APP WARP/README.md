# FaceEmotion Analyzer

Aplicación de escritorio que **detecta emociones faciales** en imágenes estáticas
usando [DeepFace](https://github.com/serengil/deepface) y una interfaz gráfica
construida con **Tkinter**.

---

## Características

| Función | Descripción |
|---|---|
| Carga de imágenes | JPG, PNG, BMP, WEBP, TIFF |
| Detección de rostros | Backend OpenCV integrado en DeepFace |
| Bounding-box | Rectángulo de color sobre cada rostro detectado |
| Emoción dominante | Resultado en **español** con porcentaje de confianza |
| Distribución completa | Barras de progreso para las 7 emociones |
| Análisis no bloqueante | Hilo secundario → la UI permanece responsiva |
| Tema dark-mode | Paleta oscura con acento en cian eléctrico |

---

## Requisitos previos

| Herramienta | Versión mínima |
|---|---|
| Python | 3.9 – 3.12 (recomendado **3.11**) |
| pip | 23+ |

> **Nota para Windows:** Tkinter viene incluido con la instalación oficial de
> Python desde [python.org](https://www.python.org/downloads/).  
> En Linux puede ser necesario instalar `python3-tk`:
> ```bash
> sudo apt install python3-tk   # Debian/Ubuntu
> ```

---

## Instalación paso a paso

### 1. Clonar o descargar el proyecto

```bash
# Con Git:
git clone <URL-del-repositorio>
cd FaceEmotionAnalyzer

# O descomprimir el ZIP y abrir la carpeta en la terminal.
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> La primera instalación puede tardar varios minutos porque descarga
> TensorFlow (~500 MB) y los modelos de DeepFace.

#### Nota para Python 3.12+

Si usas Python 3.12 o superior, instala adicionalmente:

```bash
pip install tf-keras
```

---

## Ejecución

Desde la raíz del proyecto (con el entorno virtual activo):

```bash
python main.py
```

La primera vez que se haga clic en **Analizar**, DeepFace descargará
automáticamente los modelos de reconocimiento facial (~100 MB adicionales)
y los guardará en `~/.deepface/weights/`.

---

## Uso de la aplicación

1. **Cargar foto** — abre el explorador de archivos; selecciona una imagen.
2. **Analizar** — inicia la detección (barra de estado en naranja mientras procesa).
3. Cuando termine verás:
   - La imagen con un **rectángulo de color** alrededor del rostro.
   - La **emoción dominante** en el panel derecho.
   - Las **barras de confianza** para las 7 emociones.

### Errores comunes

| Mensaje | Solución |
|---|---|
| "No se detectó ningún rostro" | Usa una foto con un rostro frontal y bien iluminado |
| `ModuleNotFoundError: deepface` | Activa el entorno virtual y repite `pip install -r requirements.txt` |
| `ImportError: tf-keras` | Ejecuta `pip install tf-keras` (Python 3.12+) |
| La ventana se congela | Normal durante la primera carga de modelos; espera unos segundos |

---

## Estructura del proyecto

```
FaceEmotionAnalyzer/
│
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
├── README.md             # Este archivo
│
└── app/
    ├── __init__.py
    ├── ui.py             # Interfaz gráfica Tkinter (AppUI)
    ├── image_loader.py   # Carga y redimensionado de imágenes (ImageLoader)
    ├── emotion_engine.py # Análisis con DeepFace (EmotionEngine)
    └── face_drawer.py    # Anotaciones visuales OpenCV (FaceDrawer)
```

---

## Decisiones de diseño

- **Alta cohesión / bajo acoplamiento**: cada módulo tiene una única responsabilidad
  y no conoce los detalles internos de los demás.
- **Análisis en hilo secundario** (`threading.Thread`): evita que la UI se congele.
- **Importación lazy de DeepFace**: la ventana abre instantáneamente; TensorFlow
  se carga solo cuando el usuario presiona *Analizar*.
- **Manejo de errores explícito**: `ValueError` para "sin rostro", `RuntimeError`
  para fallos del motor; ambos se muestran en un diálogo claro al usuario.

---

## Licencia

MIT — úsalo, modifícalo y distribúyelo libremente.
