CREATE OR REPLACE TABLE rechazados AS

SELECT *, 'id_turno_nulo' AS motivo_rechazo
FROM raw_turnos
WHERE id_turno IS NULL OR TRIM(id_turno) = ''

UNION ALL
SELECT *, 'id_turno_duplicado' AS motivo_rechazo
FROM raw_turnos
WHERE id_turno IN (
    SELECT id_turno FROM raw_turnos
    GROUP BY id_turno
    HAVING COUNT(*) > 1
)

UNION ALL

SELECT *, 'fecha_invalida' AS motivo_rechazo
FROM raw_turnos
WHERE TRY_CAST(fecha_turno AS DATE) IS NULL

UNION ALL

SELECT *, 'id_paciente_invalido' AS motivo_rechazo
FROM raw_turnos
WHERE id_paciente IS NULL OR id_paciente <= 0

UNION ALL

SELECT *, 'edad_invalida' AS motivo_rechazo
FROM raw_turnos
WHERE edad IS NULL OR edad <= 0 OR edad > 120

UNION ALL

SELECT *, 'especialidad_no_permitida' AS motivo_rechazo
FROM raw_turnos
WHERE especialidad IS NULL
   OR especialidad NOT IN ('Cardiologia', 'Clinica medica', 'Dermatologia',
                           'Ginecologia', 'Pediatria', 'Traumatologia')

UNION ALL

SELECT *, 'id_medico_nulo' AS motivo_rechazo
FROM raw_turnos
WHERE id_medico IS NULL OR TRIM(id_medico) = ''

UNION ALL

SELECT *, 'medico_nulo' AS motivo_rechazo
FROM raw_turnos
WHERE medico IS NULL OR TRIM(medico) = ''

UNION ALL

SELECT *, 'obra_social_no_permitida' AS motivo_rechazo
FROM raw_turnos
WHERE obra_social IS NULL
   OR obra_social NOT IN ('Galeno', 'OSDE', 'PAMI', 'Sin cobertura', 'Swiss Medical')

UNION ALL

SELECT *, 'costo_invalido' AS motivo_rechazo
FROM raw_turnos
WHERE costo IS NULL OR costo <= 0

UNION ALL

SELECT *, 'estado_no_permitido' AS motivo_rechazo
FROM raw_turnos
WHERE estado IS NULL OR estado NOT IN ('atendido', 'ausente', 'cancelado');


CREATE OR REPLACE TABLE validos AS
SELECT * FROM raw_turnos
WHERE id_turno IS NOT NULL
  AND id_turno NOT IN (SELECT id_turno FROM rechazados WHERE id_turno IS NOT NULL);

CREATE OR REPLACE TABLE resumen_rechazos AS
SELECT motivo_rechazo, COUNT(*) AS cantidad
FROM rechazados
GROUP BY motivo_rechazo
ORDER BY cantidad DESC;
