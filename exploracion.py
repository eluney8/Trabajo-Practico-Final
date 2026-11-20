import marimo

__generated_with = "0.10.0"
app = marimo.App()


@app.cell
def _():
    import duckdb
    import pandas as pd
    return duckdb, pd


@app.cell
def _(duckdb):
    con = duckdb.connect()
    con.execute("ATTACH 'datos/clinica.sqlite' AS origen (TYPE sqlite, READ_ONLY);")
    df = con.execute("SELECT * FROM origen.turnos;").df()
    df.head(10)
    return con, df


@app.cell
def _(df):
    df.shape
    return


@app.cell
def _(df):
    df.dtypes
    return

@app.cell
def _(df):
    df.isna().sum()
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell
def _(df):
    df["especialidad"].value_counts()
    return


@app.cell
def _(df):
    df["estado"].value_counts()
    return


@app.cell
def _(df):
    df["obra_social"].value_counts()
    return


@app.cell
def _(df):
    df["id_turno"].duplicated().sum()
    return


@app.cell
def _(df):
    fechas_raras = df[~df["fecha_turno"].str.match(r"^\d{4}-\d{2}-\d{2}$")]
    fechas_raras[["id_turno", "fecha_turno"]]
    return


@app.cell
def _(df):
    df[df["edad"] <= 0][["id_turno", "edad"]]
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id_medico, COUNT(DISTINCT medico) AS medicos_distintos
        FROM origen.turnos
        WHERE medico IS NOT NULL
        GROUP BY id_medico
        ORDER BY medicos_distintos DESC
    """).df()
    return


@app.cell
def _(con):
    con.execute("""
        SELECT TRIM(LOWER(especialidad)) AS especialidad,
               COUNT(DISTINCT costo) AS precios_distintos,
               MAX(costo) AS precio
        FROM origen.turnos
        WHERE costo IS NOT NULL
        GROUP BY TRIM(LOWER(especialidad))
    """).df()
    return


if __name__ == "__main__":
    app.run()
