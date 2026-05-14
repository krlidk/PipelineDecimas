# Pipeline de Procesamiento: Gen Z Social Media Usage

Este repositorio contiene un script de Python diseñado para la **ingesta, limpieza, transformación y validación** de un dataset masivo (1M de registros) sobre el uso de redes sociales en la Generación Z. El objetivo es garantizar la integridad de los datos para análisis estadísticos o modelos de Machine Learning.

## 📊 Sobre el Dataset Original

El archivo `genz_social_media_usage_1M.csv` contiene las siguientes variables críticas:

* **Variables Demográficas:** `age` (13-27 años), `gender`, `country`.
* **Variables de Uso:** `daily_usage_hours`, `primary_platform`, `num_platforms_used`, `avg_session_minutes`.
* **Variables de Comportamiento:** `purpose`, `night_usage` (0/1), `screen_time_before_sleep`.
* **Variables de Bienestar:** `mental_health_score` (1-10), `addiction_level`.

---

## ⚙️ Proceso ETL y Validaciones

El pipeline se divide en cuatro capas de procesamiento:

### 1. Ingesta Estructurada
Carga de datos eficiente mediante **Pandas**, integrando un sistema de `logging` que permite rastrear el flujo de ejecución y detectar errores de lectura de forma temprana.

### 2. Validación Estructural
* **Integridad de Columnas:** Se verifica que el archivo contenga las 12 columnas definidas en la documentación.
* **Casteo de Tipos:** Se asegura que las variables numéricas sean `float64` o `int64` y las categóricas sean tratadas como `strings`, eliminando errores de formato.

### 3. Limpieza y Feature Engineering
* **Imputación de Nulos:** * Variables numéricas: Se utiliza la **mediana** para evitar el sesgo de valores atípicos (outliers).
    * Variables categóricas: Se utiliza la **moda** (valor más frecuente).
* **Normalización:** Estandarización de textos (Capitalize) para evitar duplicados como "Tiktok" e "tiktok".
* **Nueva Variable (`intensity_ratio`):** Se creó esta métrica calculando `daily_usage_hours / (num_platforms_used + 1)`. Esta variable ayuda a medir qué tan concentrado o disperso es el consumo digital del usuario por cada plataforma que utiliza.

### 4. Validación Semántica (Lógica de Negocio)
Para garantizar que los datos sean realistas, se aplican las siguientes reglas:
* **Filtro Etario:** Solo se mantienen registros de usuarios entre **13 y 27 años**.
* **Rango de Salud Mental:** Se eliminan registros con puntajes fuera del rango **1-10**.
* **Consistencia de Tiempo:** El tiempo de uso antes de dormir no puede ser superior al tiempo total de uso diario reportado.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **Pandas:** Manipulación y análisis de estructuras de datos.
* **NumPy:** Operaciones vectorizadas de alto rendimiento.
* **Logging:** Seguimiento de eventos del sistema.

---

## 🚀 Cómo empezar

1.  Asegúrate de tener el archivo `genz_social_media_usage_1M.csv` en la raíz del proyecto.
2.  Instala las dependencias:
    ```bash
    pip install pandas numpy supabase
    ```
3.  Ejecuta el script:
    ```bash
    python main.py
    ```
