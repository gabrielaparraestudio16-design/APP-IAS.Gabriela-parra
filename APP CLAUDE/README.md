# ◈ EmotiScan — Detector de Emociones Faciales

Aplicación de escritorio en Python que detecta emociones faciales en imágenes
estáticas usando **DeepFace** y presenta los resultados con una interfaz
visual estilo *dark-lab* construida con **Tkinter**.

---

## ✦ Capturas de pantalla

```
┌────────────────────────────────────────────────────────────────┐
│ ◈ EMOTISCAN  / detector de emociones faciales v1.0             │
├──────────────────────────────┬─────────────────────────────────┤
│                              │  EMOCIÓN DOMINANTE              │
│    [ Imagen con bounding     │  FELICIDAD                      │
│      box dibujado ]          │  Confianza: 97.3%               │
│                              │─────────────────────────────────│
│                              │  DISTRIBUCIÓN DE EMOCIONES      │
│                              │  ENOJO    ████░░░░░░  3.1%      │
│                              │  FELICIDAD████████████ 97.3%    │
│  [ ⊕ CARGAR ] [ ⚙ ANALIZAR] │  ...                            │
└──────────────────────────────┴─────────────────────────────────┘
```

---

## ✦ Requisitos del sistema

| Componente | Versión mínima |
|------------|----------------|
| Python     | 3.9            |
| pip        | 23.0           |
| RAM        | 4 GB           |
| Espacio en disco | ~2.5 GB (modelos de DeepFace) |

> **Windows**: requiere Visual C++ Redistributable (normalmente ya instalado).  
> **macOS**: recomendado Python de [python.org](https://python.org), no el del sistema.  
> **Linux**: necesita `python3-tk` → `sudo apt install python3-tk`

---

## ✦ Instalación paso a paso

### 1. Clona o descarga el proyecto

```bash
# Con Git:
git clone https://github.com/tu-usuario/emotiscan.git
cd emotiscan

# O descomprime el ZIP descargado y entra a la carpeta:
cd emotiscan
```

### 2. Crea un entorno virtual (recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Sabrás que el entorno está activo porque verás `(.venv)` al inicio del prompt.

### 3. Actualiza pip

```bash
python -m pip install --upgrade pip
```

### 4. Instala las dependencias

```bash
pip install -r requirements.txt
```

> ⏳ Este paso puede tardar **5–15 minutos** la primera vez, ya que descarga
> TensorFlow y sus dependencias (~600 MB).

### 5. Ejecuta la aplicación

```bash
python app.py
```

> La **primera vez** que ejecutes un análisis, DeepFace descargará
> automáticamente los modelos de detección facial (~150 MB). Esto ocurre
> solo una vez; los modelos se guardan en `~/.deepface/`.

---

## ✦ Uso de la aplicación

1. **Carga una imagen** → Haz clic en `⊕ CARGAR IMAGEN` y selecciona un archivo
   (JPG, PNG, BMP, WEBP o TIFF) con al menos un rostro visible.

2. **Analiza** → Haz clic en `⚙ ANALIZAR`. La aplicación procesará la imagen
   en segundo plano sin congelar la interfaz.

3. **Revisa los resultados**:
   - La imagen mostrará un **bounding box** de color alrededor del rostro.
   - El panel derecho mostrará la **emoción dominante** y las
     **barras de porcentaje** para cada emoción.

4. **Carga otra imagen** cuando quieras repetir el proceso.

---

## ✦ Emociones detectadas

| Inglés (interno) | Español (UI) |
|------------------|--------------|
| angry            | Enojo        |
| disgust          | Asco         |
| fear             | Miedo        |
| happy            | Felicidad    |
| sad              | Tristeza     |
| surprise         | Sorpresa     |
| neutral          | Neutro       |

---

## ✦ Manejo de errores

| Situación | Mensaje mostrado |
|-----------|-----------------|
| No hay rostro en la imagen | "No se detectó ningún rostro…" |
| Archivo de imagen corrupto | "No se pudo leer el archivo de imagen." |
| Error interno de DeepFace | Descripción técnica del error |

---

## ✦ Estructura del proyecto

```
emotiscan/
├── app.py                  # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md               # Este archivo
├── core/
│   ├── __init__.py
│   ├── analyzer.py         # Lógica de análisis (DeepFace + OpenCV)
│   └── image_utils.py      # Conversión de imágenes para Tkinter
└── ui/
    ├── __init__.py
    └── main_window.py      # Interfaz gráfica (Tkinter)
```

---

## ✦ Solución de problemas frecuentes

### `ModuleNotFoundError: No module named 'tkinter'` (Linux)
```bash
sudo apt install python3-tk   # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

### `ValueError: A KerasTensor cannot be used as input to a TensorFlow function`
Desde TF 2.16, Keras 3 es el backend por defecto y **no es compatible con DeepFace**.
La solución ya está incluida en este proyecto (`TF_USE_LEGACY_KERAS=1` en `app.py`
+ `tf-keras==2.18.0` en `requirements.txt`). Si el error persiste, verifica que
instalaste exactamente con `pip install -r requirements.txt`.

### `ModuleNotFoundError: No module named 'tf_keras'`
Significa que `tf-keras` no fue instalado. Ejecuta:
```bash
pip install tf-keras==2.18.0
```

### `ERROR: Could not build wheels for tensorflow`
Asegúrate de usar Python **3.9–3.11**. TensorFlow 2.18 no soporta Python 3.12+
en todas las plataformas aún.

### La aplicación tarda mucho la primera vez
Es normal: DeepFace descarga los modelos (~150 MB) en `~/.deepface/`.
Las ejecuciones posteriores son inmediatas.

### `OSError: [Errno 28] No space left on device`
Libera al menos **2.5 GB** de espacio en disco para los modelos.

---

## ✦ Licencia

MIT License — libre para uso personal y educativo.
