import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos" / "clinica.sqlite"
SQL_DIR = BASE_DIR / "consultas"
DB_PATH = BASE_DIR / "pipeline.duckdb"


def conectar():
    """Abre la base de DuckDB del proyecto (si no existe, la crea)."""
    return duckdb.connect(str(DB_PATH))


def read_sql(filename: str):
    """Lee un archivo .sql de la carpeta consultas/."""
    try:
        path = SQL_DIR / filename
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print("Error al leer el sql: ", str(e))
        return None


def count(table_name: str, con):
    """Devuelve la cantidad de filas de una tabla."""
    try:
        return con.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]
    except Exception as e:
        print(f"Hubo un error al hacer un count de la tabla {table_name} ", str(e))


def extraer():
    print("#################### Extraccion ####################")
    con = conectar()
    con.execute(f"ATTACH '{DATA_DIR}' AS origen (TYPE sqlite, READ_ONLY);")
    con.execute(read_sql("extract.sql"))
    con.execute("DETACH origen;")
    print("Valores extraidos (raw_turnos): ", count("raw_turnos", con))
    con.close()


def validar():
    print("#################### Validaciones ####################")
    con = conectar()
    con.execute(read_sql("validar.sql"))
    print("Filas en rechazados: ", count("rechazados", con))
    print(
        "Turnos distintos rechazados: ",
        con.execute("SELECT COUNT(DISTINCT id_turno) FROM rechazados;").fetchone()[0],
    )
    print("Valores validos: ", count("validos", con))
    print("Rechazos por regla:")
    print(con.execute("SELECT * FROM resumen_rechazos;").df().to_string(index=False))
    con.close()


def limpiar():
    print("#################### Limpieza ####################")
    con = conectar()
    df = con.execute("SELECT * FROM rechazados;").df()
    df = df.drop(columns=["motivo_rechazo"])
    df = df.drop_duplicates(subset=["id_turno"])
    fecha_iso = pd.to_datetime(df["fecha_turno"], format="%Y-%m-%d", errors="coerce")
    fecha_dma = pd.to_datetime(df["fecha_turno"], format="%d/%m/%Y", errors="coerce")
    df["fecha_turno"] = fecha_iso.fillna(fecha_dma)
    df["especialidad"] = df["especialidad"].str.strip().str.lower()
    df["especialidad"] = df["especialidad"].replace(
        {
            "cardiologia": "Cardiologia",
            "clinica medica": "Clinica medica",
            "dermatologia": "Dermatologia",
            "ginecologia": "Ginecologia",
            "pediatria": "Pediatria",
            "traumatologia": "Traumatologia",
        }
    )

    df["estado"] = df["estado"].str.strip().str.lower()
    df["obra_social"] = df["obra_social"].str.strip()
    df["medico"] = df["medico"].str.strip()
    df["edad"] = df["edad"].abs()
    medicos = con.execute(
        "SELECT DISTINCT id_medico, medico AS medico_correcto FROM validos;"
    ).df()
    df = pd.merge(df, medicos, on="id_medico", how="left")
    df["medico"] = df["medico"].fillna(df["medico_correcto"])
    df = df.drop(columns=["medico_correcto"])
    precios = con.execute(
        "SELECT DISTINCT especialidad, costo AS costo_correcto FROM validos;"
    ).df()
    df = pd.merge(df, precios, on="especialidad", how="left")
    df["costo"] = df["costo"].fillna(df["costo_correcto"])
    df = df.drop(columns=["costo_correcto"])
    df = df.drop_duplicates(subset=["id_turno"])
    con.register("rechazados_pandas", df)
    con.execute(read_sql("limpiar.sql"))
    con.unregister("rechazados_pandas")

    recuperados = count("rechazados_limpios", con)
    print("Turnos rechazados (sin repetir): ", len(df))
    print("Valores recuperados (rechazados_limpios): ", recuperados)
    print("No recuperables: ", len(df) - recuperados)
    con.close()


def unir():
    print("#################### Union ####################")
    con = conectar()
    con.execute(read_sql("unir.sql"))
    total = count("tabla_final", con)
    distintos = con.execute(
        "SELECT COUNT(DISTINCT id_turno) FROM tabla_final;"
    ).fetchone()[0]
    print("Valores en tabla_final: ", total)
    print(
        "id_turno distintos: ",
        distintos,
        "(si coincide con el total, no hay duplicados)",
    )
    print(
        con.execute("DESCRIBE tabla_final;")
        .df()[["column_name", "column_type"]]
        .to_string(index=False)
    )
    con.close()


def responder_preguntas():
    print("#################### Preguntas de negocio ####################")
    con = conectar()
    consultas = [q.strip() for q in read_sql("preguntas.sql").split(";")]
    consultas = [q for q in consultas if "SELECT" in q.upper()]
    for i, consulta in enumerate(consultas, start=1):
        con.execute(f"CREATE OR REPLACE TABLE pregunta_{i} AS {consulta}")
        print(f"\n--- Pregunta {i} ---")
        print(con.execute(f"SELECT * FROM pregunta_{i};").df().to_string(index=False))
    con.close()


def main():
    extraer()
    validar()
    limpiar()
    unir()
    responder_preguntas()


if __name__ == "__main__":
    main()
