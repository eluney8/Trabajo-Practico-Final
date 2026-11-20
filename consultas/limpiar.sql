CREATE OR REPLACE TABLE rechazados_limpios AS
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
    estado
FROM rechazados_pandas
WHERE id_turno IS NOT NULL
  AND fecha_turno IS NOT NULL
  AND id_paciente > 0
  AND edad > 0 AND edad <= 120
  AND especialidad IN ('Cardiologia', 'Clinica medica', 'Dermatologia',
                       'Ginecologia', 'Pediatria', 'Traumatologia')
  AND id_medico IS NOT NULL
  AND medico IS NOT NULL
  AND obra_social IN ('Galeno', 'OSDE', 'PAMI', 'Sin cobertura', 'Swiss Medical')
  AND costo > 0
  AND estado IN ('atendido', 'ausente', 'cancelado');
