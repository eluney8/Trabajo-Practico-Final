import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    con = duckdb.connect("pipeline.duckdb", read_only=True)
    return (con,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT especialidad,
               COUNT(*) AS cantidad_turnos
        FROM tabla_final
        GROUP BY especialidad
        ORDER BY cantidad_turnos DESC, especialidad
        """,
        engine=con
    )
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT t.especialidad,
               t.total_turnos,
               a.ausentes,
               ROUND(100.0 * a.ausentes / t.total_turnos, 2) AS porcentaje_ausentismo
        FROM (SELECT especialidad, COUNT(*) AS total_turnos
              FROM tabla_final
              GROUP BY especialidad) AS t
        JOIN (SELECT especialidad, COUNT(*) AS ausentes
              FROM tabla_final
              WHERE estado = 'ausente'
              GROUP BY especialidad) AS a
          ON t.especialidad = a.especialidad
        ORDER BY porcentaje_ausentismo DESC, t.especialidad
        """,
        engine=con
    )
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT DATE_TRUNC('month', fecha_turno) AS mes,
               COUNT(*)   AS turnos_atendidos,
               SUM(costo) AS facturado
        FROM tabla_final
        WHERE estado = 'atendido'
        GROUP BY mes
        ORDER BY mes
        LIMIT 6
        """,
        engine=con
    )
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT id_medico,
               medico,
               COUNT(*) AS turnos_atendidos
        FROM tabla_final
        WHERE estado = 'atendido'
        GROUP BY id_medico, medico
        ORDER BY turnos_atendidos DESC, medico
        LIMIT 5
        """,
        engine=con
    )
    return


@app.cell
def _(con, mo):
    _df = mo.sql(
        f"""
        SELECT obra_social,
               ROUND(AVG(edad), 1) AS edad_promedio,
               COUNT(*)            AS cantidad_turnos
        FROM tabla_final
        GROUP BY obra_social
        ORDER BY edad_promedio DESC, obra_social
        """,
        engine=con
    )
    return


if __name__ == "__main__":
    app.run()
