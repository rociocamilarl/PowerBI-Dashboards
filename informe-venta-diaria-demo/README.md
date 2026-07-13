# Informe de Venta Diaria — Laboratorio Clínico (DEMO)

Réplica de portafolio de un informe productivo de **venta diaria** construido en Power BI
para un laboratorio clínico multisede. **Todos los datos son ficticios**: clientes, sedes,
montos y volúmenes fueron generados con un script reproducible; ningún dato real del
cliente está incluido.

![Vista previa del dashboard](preview.png)

## Qué muestra

- **KPIs del día**: venta neta, exámenes realizados, cumplimiento de presupuesto
  prorrateado (MTD) y variación contra el año anterior.
- **Venta diaria vs. venta requerida** para cumplir el presupuesto del mes.
- **Cumplimiento de presupuesto por sede** (8 sedes en 4 zonas).
- **Venta por cliente / convenio** (particular, institucional, isapres, empresas).
- **Tendencia mensual vs. presupuesto** (últimos 13 meses).

## Estructura del modelo (igual al informe productivo)

| Tabla | Contenido |
|---|---|
| `Ventas` | Detalle diario: fecha, sede, cliente, convenio, prestación, cantidad, monto neto |
| `Sedes` | Sede, ciudad, zona, grupo |
| `Clientes` | Cliente y tipo de convenio |
| `Examenes` | Prestación, descripción, área clínica, precio lista |
| `Presupuesto` | PPTO $ y PPTO Q mensual por sede |
| `Calendario` | Tabla de fechas (generada en Power BI) |

## Contenido de la carpeta

- [`demo_dashboard.html`](demo_dashboard.html) — demo interactivo (abrir en el navegador:
  tooltips, modo claro/oscuro automático).
- [`datos_ficticios/`](datos_ficticios/) — CSVs listos para conectar desde Power BI
  Desktop (separador `;`, codificación UTF-8): `ventas.csv` (22.000+ filas, ene 2025 –
  jul 2026), `sedes.csv`, `clientes.csv`, `examenes.csv`, `presupuesto.csv`.

## Resultado para el cliente

El informe productivo reemplazó una planilla manual que se armaba cada mañana:
la gerencia comercial pasó de conocer la venta del día anterior al mediodía a tenerla
disponible a primera hora, con alertas de cumplimiento por sede y convenio.

---
*DataconsultingRRL — automatización, IA y dashboards para PYMEs.*
