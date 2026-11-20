import sys
from pathlib import Path

import pendulum

try:
    from airflow.sdk import DAG
except ImportError:
    from airflow import DAG

try:
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.python import PythonOperator

PROYECTO = Path.home() / "tema_02_clinica"
sys.path.insert(0, str(PROYECTO))

import pipeline

with DAG(
    dag_id="pipeline_clinica_santa_lucia",
    description="ETL de turnos medicos: extraer, validar, limpiar, unir y responder preguntas",
    schedule="0 2 * * *",
    start_date=pendulum.datetime(2026, 11, 1, tz="America/Argentina/Buenos_Aires"),
    catchup=False,
    tags=["tp_final", "etl", "clinica"],
) as dag:
    t_extraer = PythonOperator(task_id="extraer", python_callable=pipeline.extraer)
    t_validar = PythonOperator(task_id="validar", python_callable=pipeline.validar)
    t_limpiar = PythonOperator(task_id="limpiar", python_callable=pipeline.limpiar)
    t_unir = PythonOperator(task_id="unir", python_callable=pipeline.unir)
    t_preguntas = PythonOperator(
        task_id="responder_preguntas", python_callable=pipeline.responder_preguntas
    )

    t_extraer >> t_validar >> t_limpiar >> t_unir >> t_preguntas
