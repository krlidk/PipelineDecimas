import pandas as pd
import numpy as np
import logging
from supabase import create_client, Client

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- CONFIGURACIÓN DE SUPABASE ---
SUPABASE_URL = "https://axdingukvxjxpithwulw.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF4ZGluZ3VrdnhqeHBpdGh3dWx3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3ODQxMzEsImV4cCI6MjA5NDM2MDEzMX0.VtSyzym-koCsht4g9_kRI1u5adZ_d_dwm4xGktnMcWk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def process_pipeline(file_path):
    try:
        logging.info(f"Iniciando Pipeline para: {file_path}")
        
        # 1. INGESTA (Sin cabeceras)
        column_names = [
            'age', 'gender', 'country', 'daily_usage_hours', 
            'primary_platform', 'num_platforms_used', 'purpose', 
            'avg_session_minutes', 'night_usage', 'mental_health_score', 
            'addiction_level', 'screen_time_before_sleep'
        ]
        df = pd.read_csv(file_path, header=None, names=column_names)

        # 2. VALIDACIÓN ESTRUCTURAL (Casteo de tipos)
        # Columnas que son INT en la base de datos
        int_cols = ['age', 'num_platforms_used', 'night_usage', 'mental_health_score']
        # Columnas que son FLOAT en la base de datos
        float_cols = ['daily_usage_hours', 'avg_session_minutes', 'screen_time_before_sleep']

        for col in int_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        for col in float_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        # 3. LIMPIEZA Y TRANSFORMACIÓN
        # Imputación de nulos en texto y normalización
        df['gender'] = df['gender'].fillna('Other').str.strip().str.capitalize()
        df['primary_platform'] = df['primary_platform'].fillna('Unknown').str.strip().str.capitalize()
        df['addiction_level'] = df['addiction_level'].fillna('Medium').str.strip().str.capitalize()
        
        # Feature Engineering: Nueva Variable
        df['intensity_ratio'] = df['daily_usage_hours'] / (df['num_platforms_used'] + 1)

        # 4. VALIDACIÓN SEMÁNTICA (Reglas de Negocio)
        # Filtro Gen Z: 13 a 27 años
        df = df[(df['age'] >= 13) & (df['age'] <= 27)]
        # Rango Salud Mental: 1 a 10
        df = df[(df['mental_health_score'] >= 1) & (df['mental_health_score'] <= 10)]
        # Consistencia: No puede dormir más de lo que usa el cel al día (aprox)
        df = df[df['screen_time_before_sleep'] <= (df['daily_usage_hours'] * 60)]

        logging.info(f"Procesamiento completado. Registros válidos: {len(df)}")
        return df

    except Exception as e:
        logging.error(f"Error en el pipeline: {e}")
        return None

def upload_to_supabase(df, table_name, batch_size=1000):
    logging.info(f"Iniciando subida a Supabase...")
    
    # Convertir a lista de diccionarios para la API
    records = df.to_dict(orient='records')
    total_records = len(records)
    
    for i in range(0, total_records, batch_size):
        batch = records[i : i + batch_size]
        try:
            supabase.table(table_name).insert(batch).execute()
            if (i + batch_size) % 5000 == 0 or (i + batch_size) >= total_records:
                logging.info(f"Progreso: {min(i + batch_size, total_records)} / {total_records}")
        except Exception as e:
            logging.error(f"Fallo en lote {i}: {e}")

def main():
    file_name = 'genz_social_media_usage_1M.csv'
    
    # Ejecutar todo el proceso
    df_ready = process_pipeline(file_name)
    
    if df_ready is not None and not df_ready.empty:
        upload_to_supabase(df_ready, 'gen_z_usage')
    else:
        logging.warning("No hay datos válidos para subir.")

if __name__ == "__main__":
    main()