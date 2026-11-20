# Informe — Pipeline ETL Clínica Santa Lucía (Tema 02)

**Fuente:** `datos/clinica.sqlite`, tabla `turnos` (2575 filas). **Resultado:** `tabla_final` con 2500 turnos únicos, 1481 válidos de origen y 1019 recuperados por la limpieza. Ningún turno quedó sin recuperar.

## 1. Problemas encontrados

- **Fechas en dos formatos:** 257 turnos con `DD/MM/AAAA` en lugar de `AAAA-MM-DD`. Se convirtieron probando cada formato por separado.
- **Especialidad mal escrita:** 206 turnos con mayúsculas o espacios. Se normalizó con `strip()`, `lower()` y `replace()`.
- **Estado con espacios:** 154 turnos. Se corrigió con `strip()`.
- **Médico vacío:** 158 turnos. se completó a partir de los turnos válidos.
- **Costo vacío:** 129 turnos, se completó a partir de los turnos válidos.
- **Edad negativa:** 101 turnos. Se tomó el valor absoluto, porque el resto de las edades va de 1 a 90.
- **Turnos duplicados:** 75 copias idénticas de un mismo `id_turno`. Se dejó una sola.


## 3. Respuestas a las preguntas de negocio

**P1. Turnos por especialidad:** Clínica médica 442 · Pediatría 431 · Dermatología 420 · Ginecología 419 · Traumatología 416 · Cardiología 372.

**P2. Ausentismo por especialidad**: Pediatría 18,79 % · Cardiología 18,01 % · Clínica médica 17,65 % · Ginecología 17,18 % · Traumatología 15,63 % · Dermatología 15,24 %.

**P3. Facturación de turnos atendidos, primeros 6 meses:**

| Mes | Atendidos | Facturado |
|---|---|---|
| Ene 2024 | 66 | $1.665.000 |
| Feb 2024 | 68 | $1.788.000 |
| Mar 2024 | 78 | $2.024.000 |
| Abr 2024 | 73 | $1.896.000 |
| May 2024 | 77 | $2.087.000 |
| Jun 2024 | 64 | $1.681.000 |

**P4. Top 5 médicos por turnos atendidos:** Dr. Romero C1 (124) · Dr. Lopez F1 (113) · Dr. Acosta E1 (111) · Dr. Lopez B1 (109) · Dr. Sosa B0 (105).

**P5. Edad promedio por obra social:** OSDE 46,3 · Sin cobertura 45,9 · Swiss Medical 45,9 · Galeno 45,4 · PAMI 44,8 años.

**Automatización:** el DAG `pipeline_clinica_santa_lucia` corre todos los días a las 2:00 con 5 tareas: extraer → validar → limpiar → unir → responder_preguntas.
