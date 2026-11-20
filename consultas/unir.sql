CREATE OR REPLACE TABLE tabla_final AS
SELECT
    id_turno,
    CAST(fecha_turno AS DATE)    AS fecha_turno,
    CAST(id_paciente AS INTEGER) AS id_paciente,
    CAST(edad AS INTEGER)        AS edad,
    especialidad,
    id_medico,
    medico,
    obra_social,
    CAST(costo AS DOUBLE)        AS costo,
    estado,
    'valido'                     AS origen
FROM validos

UNION ALL

SELECT
    id_turno,
    fecha_turno,
    id_paciente,
    edad,
    especialidad,
    id_medico,
    medico,
    obra_social,
    costo,
    estado,
    'recuperado'                 AS origen
FROM rechazados_limpios
WHERE id_turno NOT IN (SELECT id_turno FROM validos);
