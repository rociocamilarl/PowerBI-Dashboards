#!/usr/bin/env python3
"""Genera datos ficticios para el demo 'Informe de Venta Diaria - Laboratorio Clinico'.
Todos los nombres, montos y volumenes son inventados (semilla fija = reproducible)."""
import csv, json, random, os
from datetime import date, timedelta

random.seed(42)
OUT = os.path.dirname(os.path.abspath(__file__))  # escribe junto al script

SEDES = [  # sede, ciudad, zona, peso relativo de venta
    ("Santiago Centro", "Santiago", "Zona Centro", 1.00),
    ("Providencia", "Santiago", "Zona Centro", 0.85),
    ("Las Condes", "Santiago", "Zona Centro", 0.90),
    ("Maipú", "Santiago", "Zona Centro", 0.60),
    ("Viña del Mar", "Viña del Mar", "Zona Costa", 0.55),
    ("Valparaíso", "Valparaíso", "Zona Costa", 0.45),
    ("Concepción", "Concepción", "Zona Sur", 0.50),
    ("Antofagasta", "Antofagasta", "Zona Norte", 0.40),
]
CLIENTES = [  # cliente, convenio, peso
    ("Particular", "Particular", 0.30),
    ("Fonasa", "Institucional", 0.22),
    ("Isapre Andina", "Isapre", 0.12),
    ("Isapre Cumbre", "Isapre", 0.09),
    ("Minera Norte SpA", "Empresa", 0.06),
    ("Constructora Pacífico Ltda.", "Empresa", 0.05),
    ("Colegio San Martín", "Empresa", 0.03),
    ("Seguro Vida Austral", "Seguro", 0.04),
    ("Municipalidad Demo", "Institucional", 0.03),
    ("Logística del Sur S.A.", "Empresa", 0.03),
    ("Centro Deportivo Cordillera", "Empresa", 0.02),
    ("Clínica Asociada", "Interclínico", 0.01),
]
EXAMENES = [  # prestacion, descripcion, area, precio base CLP
    ("HEM-001", "Hemograma completo", "Hematología", 8900),
    ("HEM-002", "Perfil de coagulación", "Hematología", 12400),
    ("QUI-001", "Perfil bioquímico", "Química Clínica", 14900),
    ("QUI-002", "Perfil lipídico", "Química Clínica", 9800),
    ("QUI-003", "Glicemia", "Química Clínica", 4200),
    ("QUI-004", "Perfil hepático", "Química Clínica", 11600),
    ("QUI-005", "Creatinina", "Química Clínica", 4600),
    ("END-001", "TSH", "Endocrinología", 8700),
    ("END-002", "Perfil tiroideo", "Endocrinología", 16800),
    ("END-003", "Insulina basal", "Endocrinología", 9900),
    ("INM-001", "Vitamina D", "Inmunología", 15400),
    ("INM-002", "PCR ultrasensible", "Inmunología", 7800),
    ("INM-003", "Panel alergias", "Inmunología", 32500),
    ("MIC-001", "Urocultivo", "Microbiología", 9200),
    ("MIC-002", "Coprocultivo", "Microbiología", 10800),
    ("MIC-003", "Test rápido Streptococo", "Microbiología", 8100),
    ("ORI-001", "Orina completa", "Orina", 5300),
    ("IMG-001", "Radiografía de tórax", "Imagenología", 18900),
    ("IMG-002", "Ecografía abdominal", "Imagenología", 34500),
    ("IMG-003", "Mamografía", "Imagenología", 29800),
    ("GEN-001", "Test PCR respiratorio", "Biología Molecular", 24900),
    ("GEN-002", "Panel genético básico", "Biología Molecular", 58000),
    ("TOM-001", "Toma de muestra domicilio", "Servicios", 7500),
    ("KIN-001", "Electrocardiograma", "Cardiología", 13200),
]

START, END = date(2025, 1, 1), date(2026, 7, 12)
DOW_F = {0: 1.05, 1: 1.10, 2: 1.08, 3: 1.02, 4: 0.98, 5: 0.55, 6: 0.18}  # lun..dom

def month_growth(d):
    months = (d.year - 2025) * 12 + (d.month - 1)
    return 1.0 + 0.012 * months  # ~1.2% mensual

ventas_path = os.path.join(OUT, "ventas.csv")
with open(ventas_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Fecha_Registro", "Sede", "Cliente", "Convenio",
                "Prestación", "DescripcionExamen", "Área", "Cantidad", "Monto Neto"])
    d = START
    daily_totals = {}
    while d <= END:
        f_day = DOW_F[d.weekday()] * month_growth(d)
        for sede, ciudad, zona, peso in SEDES:
            n_lineas = max(2, int(random.gauss(9, 2) * peso * (0.4 if d.weekday() == 6 else 1)))
            for _ in range(n_lineas):
                cli = random.choices(CLIENTES, weights=[c[2] for c in CLIENTES])[0]
                ex = random.choice(EXAMENES)
                qty = max(1, int(random.gauss(6, 3) * f_day))
                desc = 1 - (0.12 if cli[1] in ("Isapre", "Empresa", "Seguro") else 0.0)
                monto = int(ex[3] * qty * desc * random.uniform(0.95, 1.05))
                w.writerow([d.isoformat(), sede, cli[0], cli[1],
                            ex[0], ex[1], ex[2], qty, monto])
                key = (d.isoformat(), sede)
                t = daily_totals.setdefault(key, [0, 0])
                t[0] += monto; t[1] += qty
        d += timedelta(days=1)

with open(os.path.join(OUT, "sedes.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Sede", "Ciudad2", "Zona2", "Grupo"])
    for sede, ciudad, zona, _ in SEDES:
        w.writerow([sede, ciudad, zona, "Red Propia"])

with open(os.path.join(OUT, "clientes.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Cliente", "Convenio"])
    for c, conv, _ in CLIENTES:
        w.writerow([c, conv])

with open(os.path.join(OUT, "examenes.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Prestación_1", "DescripcionExamen", "Área", "Precio Lista"])
    for p, desc, area, precio in EXAMENES:
        w.writerow([p, desc, area, precio])

# PPTO mensual por sede ($ y Q) = promedio real del mes año anterior * 1.10 (o mes actual * 1.05 para 2025)
from collections import defaultdict
mensual = defaultdict(lambda: [0, 0])
for (fecha, sede), (m, q) in daily_totals.items():
    mensual[(fecha[:7], sede)][0] += m
    mensual[(fecha[:7], sede)][1] += q
with open(os.path.join(OUT, "presupuesto.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Mes_Año", "Sede", "PPTO $", "PPTO Q"])
    for (mes, sede) in sorted(mensual):
        y, mm = int(mes[:4]), int(mes[5:7])
        prev = mensual.get((f"{y-1}-{mm:02d}", sede))
        if prev:
            ppto, pptoq = int(prev[0] * 1.10), int(prev[1] * 1.10)
        else:
            ppto, pptoq = int(mensual[(mes, sede)][0] * 1.05), int(mensual[(mes, sede)][1] * 1.05)
        w.writerow([mes, sede, ppto, pptoq])

# ---- agregados para el dashboard HTML ----
agg = {"dailyJul": [], "sedesMTD": [], "convMTD": [], "monthly": [], "kpi": {}}
jul = [(k, v) for k, v in daily_totals.items() if k[0].startswith("2026-07")]
by_day = defaultdict(lambda: [0, 0])
for (fecha, sede), (m, q) in jul:
    by_day[fecha][0] += m; by_day[fecha][1] += q
ppto_jul = sum(int(mensual[(f"2025-07", s[0])][0] * 1.10) for s in SEDES)
req_diaria = ppto_jul / 31
for fecha in sorted(by_day):
    agg["dailyJul"].append({"d": fecha, "v": by_day[fecha][0], "q": by_day[fecha][1]})
agg["kpi"]["reqDiaria"] = int(req_diaria)
agg["kpi"]["pptoJul"] = ppto_jul

sede_mtd = defaultdict(lambda: [0, 0])
for (fecha, sede), (m, q) in jul:
    sede_mtd[sede][0] += m; sede_mtd[sede][1] += q
for sede, ciudad, zona, _ in SEDES:
    ppto_s = int(mensual[("2025-07", sede)][0] * 1.10)
    ppto_prorrateado = ppto_s * 12 / 31
    agg["sedesMTD"].append({"s": sede, "z": zona, "v": sede_mtd[sede][0],
                            "pptoMes": ppto_s, "cumpl": round(sede_mtd[sede][0] / ppto_prorrateado * 100, 1)})

# convenios MTD desde ventas.csv (releer solo julio 2026)
conv = defaultdict(lambda: [0, 0])
with open(ventas_path, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f, delimiter=";"):
        if row["Fecha_Registro"].startswith("2026-07"):
            conv[row["Cliente"]][0] += int(row["Monto Neto"])
            conv[row["Cliente"]][1] += int(row["Cantidad"])
for c in sorted(conv, key=lambda x: -conv[x][0]):
    agg["convMTD"].append({"c": c, "v": conv[c][0], "q": conv[c][1]})

months = sorted({m for m, s in mensual})
for mes in months[-13:]:
    tot = sum(mensual[(mes, s[0])][0] for s in SEDES)
    y, mm = int(mes[:4]), int(mes[5:7])
    prev = [mensual.get((f"{y-1}-{mm:02d}", s[0])) for s in SEDES]
    ppto = sum(int(p[0] * 1.10) for p in prev) if all(prev) else int(tot * 1.05)
    agg["monthly"].append({"m": mes, "v": tot, "ppto": ppto})

# KPIs cabecera
last_day = max(by_day)
mtd = sum(v[0] for v in by_day.values())
mtd_q = sum(v[1] for v in by_day.values())
jul25 = [(k, v) for k, v in daily_totals.items() if k[0].startswith("2025-07") and int(k[0][8:10]) <= 12]
mtd_prev = sum(v[0] for k, v in jul25)
agg["kpi"].update({
    "fecha": last_day, "ventaDia": by_day[last_day][0], "qDia": by_day[last_day][1],
    "mtd": mtd, "mtdQ": mtd_q,
    "cumplMTD": round(mtd / (ppto_jul * 12 / 31) * 100, 1),
    "varAnoAnt": round((mtd / mtd_prev - 1) * 100, 1),
})
with open(os.path.join(os.path.dirname(OUT), "agregados_demo.json"), "w", encoding="utf-8") as f:
    json.dump(agg, f, ensure_ascii=False)

n = sum(1 for _ in open(ventas_path, encoding="utf-8-sig")) - 1
print(f"ventas.csv: {n} filas | {os.path.getsize(ventas_path)//1024} KB")
print("KPI:", json.dumps(agg["kpi"], ensure_ascii=False))
print("Sedes MTD:", [(s['s'], s['cumpl']) for s in agg['sedesMTD']])
