import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ══════════════════════════════════════════════════════════════════════════════
# CANVAS — aspect 1:1 so circles are circles and proportions are true
# ══════════════════════════════════════════════════════════════════════════════
XMIN, XMAX = 0.0, 26.0
YMIN, YMAX = 2.6, 12.9
fig, ax = plt.subplots(figsize=(XMAX - XMIN, YMAX - YMIN))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')
ax.set_facecolor('#F8F9FA')

# ══════════════════════════════════════════════════════════════════════════════
# GRID CONSTANTS — everything derives from these, so the layout stays symmetric
# ══════════════════════════════════════════════════════════════════════════════
ML, MR = 0.4, 25.6          # left / right content margins (centre = 13.0)
CENTER = (ML + MR) / 2      # 13.0

# Row 1 — chain of 7 boxes evenly spaced edge to edge
N_CHAIN = 7
BLK_W   = 3.0
BLK_H   = 1.70
BLK_CY  = 9.90
CHAIN_GAP = ((MR - ML) - N_CHAIN * BLK_W) / (N_CHAIN - 1)   # = 0.70

def chain_cx(i):
    return ML + BLK_W / 2 + i * (BLK_W + CHAIN_GAP)

# Alarm region (left) and notes column (right)
ALARM_L, ALARM_R = ML, 15.6
ALARM_C = (ALARM_L + ALARM_R) / 2          # 8.0
NOTES_L, NOTES_R = 16.4, MR

# Alarm columns — symmetric about ALARM_C
COL_OFF = 3.6
COMP1_X = ALARM_C - COL_OFF                 # 4.4
COMP2_X = ALARM_C + COL_OFF                 # 11.6
CMP_W, CMP_H = 4.4, 1.70
CMP_CY = 6.10                                # box: 5.25 – 6.95
LED_W, LED_H = 4.4, 1.30
LED_CY = 3.70                                # box: 3.05 – 4.35

BUS_Y = 7.75                                 # green distribution bus
DIV_Y = 8.45                                 # red section divider

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def rbox(x, y, w, h, fc, ec, lw=2.0, r=0.28):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3))

def arr(x0, y0, x1, y1, color, lw=2.2, scale=15):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=scale), zorder=4)

def pill(x, y, txt, fc, ec='none', fs=8.5, tc='white', pad=0.28):
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', zorder=7,
            bbox=dict(boxstyle=f'round,pad={pad}', facecolor=fc,
                      edgecolor=ec, linewidth=1.2, alpha=0.97))

# ══════════════════════════════════════════════════════════════════════════════
# TITLE — centred on the canvas
# ══════════════════════════════════════════════════════════════════════════════
ax.text(CENTER, 12.55,
        'Sistema de Monitoreo de Frecuencia Cardíaca (ECG simulado)',
        ha='center', va='center', fontsize=17, fontweight='bold', color='#1A252F')
ax.text(CENTER, 12.18,
        'Diagrama de bloques · Avance 1 · Circuitos Integrados Lineales · '
        'Implementación únicamente con amplificadores operacionales 741',
        ha='center', va='center', fontsize=9, color='#6C7A89')
ax.plot([6, 20], [11.95, 11.95], color='#BDC3C7', lw=0.9)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 HEADER — full content width
# ══════════════════════════════════════════════════════════════════════════════
H1_Y, H1_H = 11.30, 0.46
ax.add_patch(FancyBboxPatch((ML, H1_Y), MR - ML, H1_H,
    boxstyle='round,pad=0,rounding_size=0.18',
    facecolor='none', edgecolor='#2E86AB', linewidth=1.8, zorder=2))
ax.plot([ML, ML], [H1_Y, H1_Y + H1_H], color='#2E86AB', lw=5,
        solid_capstyle='round', zorder=3)
ax.text(ML + 0.45, H1_Y + H1_H / 2,
        'CADENA DE ACONDICIONAMIENTO Y PROCESAMIENTO DE SEÑAL',
        ha='left', va='center', fontsize=9.5, color='#1A5276', fontweight='bold')

# ══════════════════════════════════════════════════════════════════════════════
# CHAIN — 6 numbered blocks + output box, evenly spaced
# ══════════════════════════════════════════════════════════════════════════════
chain = [
    ('1', 'Generador de\nfunciones (ECG)',
     '5 – 50 mVpp\n1 – 2.5 Hz · 60 – 150 BPM',  '#1A5276', '#EAF4FB', '#2E86C1'),
    ('2', 'Seguidor de\nvoltaje (buffer)',
     'Ganancia = 1\nAlta Z_in · aislamiento',      '#1A5276', '#EAF4FB', '#2E86C1'),
    ('3', 'Amplificador\nno inversor',
     'A_v = 1 + Rf / Ri\nAcondiciona amplitud',    '#1A5276', '#EAF4FB', '#2E86C1'),
    ('4', 'Filtro activo\n(pasa-bajas)',
     'Reduce ruido\nf_c por encima de 2.5 Hz',     '#1A3A5C', '#D6EAF8', '#2471A3'),
    ('5', 'Comparador (V_R)\ndetector de latidos',
     'Umbral V_R\nGenera tren de pulsos',           '#1A5276', '#EAF4FB', '#2E86C1'),
    ('6', 'Convertidor\nfrecuencia-voltaje',
     'F → V (CD)\nSalida 0-10 V ≈ BPM',           '#145A32', '#D5F5E3', '#1E8449'),
    (None, 'Salida\nproporcional',
     'Señal continua 0–10 V\n∝ frecuencia (BPM)', '#145A32', '#D5F5E3', '#1E8449'),
]

for i, (num, title, sub, nc, bfc, bec) in enumerate(chain):
    cx = chain_cx(i)
    bx, by = cx - BLK_W / 2, BLK_CY - BLK_H / 2
    rbox(bx, by, BLK_W, BLK_H, bfc, bec, lw=2.0)
    if num:
        ax.add_patch(plt.Circle((bx + 0.33, by + BLK_H - 0.33), 0.21,
                                 color=nc, zorder=5))
        ax.text(bx + 0.33, by + BLK_H - 0.33, num,
                ha='center', va='center', fontsize=8.5, color='white',
                fontweight='bold', zorder=6)
    ax.text(cx, BLK_CY + 0.24, title,
            ha='center', va='center', fontsize=9,
            color='#1A252F', fontweight='bold', zorder=5)
    ax.text(cx, BLK_CY - 0.44, sub,
            ha='center', va='center', fontsize=7.5, color='#5D6D7E', zorder=5)

# inter-block arrows — signal labels float above the arrows, clear of the boxes
labels = ['mV', 'buffer', 'amplif.', 'filtrada', 'pulsos', 'V ∝ BPM']
lcolors = ['#2471A3', '#2471A3', '#2471A3', '#2471A3', '#1E8449', '#1E8449']
LABEL_Y = BLK_CY + BLK_H / 2 + 0.24

for i in range(N_CHAIN - 1):
    x0 = chain_cx(i) + BLK_W / 2
    x1 = chain_cx(i + 1) - BLK_W / 2
    color = '#1E8449' if i >= 5 else '#34495E'
    arr(x0, BLK_CY, x1, BLK_CY, color, lw=2.0, scale=14)
    pill((x0 + x1) / 2, LABEL_Y, labels[i], lcolors[i], fs=7.5, pad=0.20)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 DIVIDER — red rule, alarm region only (nothing crosses it)
# ══════════════════════════════════════════════════════════════════════════════
ax.plot([ALARM_L, ALARM_R], [DIV_Y, DIV_Y], color='#C0392B', lw=2.0, zorder=2)
ax.plot([ALARM_L, ALARM_L], [DIV_Y - 0.26, DIV_Y + 0.26],
        color='#C0392B', lw=5, solid_capstyle='round', zorder=3)
ax.text(ML + 0.45, DIV_Y + 0.14,
        'ETAPA DE ALARMAS (FUERA DE RANGO NORMAL)',
        ha='left', va='bottom', fontsize=9.5, color='#922B21', fontweight='bold')

# ══════════════════════════════════════════════════════════════════════════════
# GREEN BUS — drops from block 6, runs left, feeds both comparators
# ══════════════════════════════════════════════════════════════════════════════
B6_X = chain_cx(5)
ax.plot([B6_X, B6_X], [BLK_CY - BLK_H / 2, BUS_Y],
        color='#1E8449', lw=2.5, zorder=4)                       # vertical drop
ax.plot([COMP1_X, B6_X], [BUS_Y, BUS_Y],
        color='#1E8449', lw=2.5, zorder=4)                       # horizontal bus

for xd in (COMP1_X, COMP2_X):                                     # junction dots
    ax.plot(xd, BUS_Y, 'o', color='#1E8449', ms=8, zorder=5)
    arr(xd, BUS_Y, xd, CMP_CY + CMP_H / 2, '#1E8449', lw=2.2)    # drops

# bus label — pill ON the line, centred between the two taps
pill(ALARM_C, BUS_Y, 'V_out (0–10 V) — alimenta los comparadores de alarma',
     '#1E8449', ec='#145A32', fs=8.5)

# ══════════════════════════════════════════════════════════════════════════════
# COMPARATORS — symmetric columns about ALARM_C
# ══════════════════════════════════════════════════════════════════════════════
comparators = [
    (COMP1_X, 'Comparador 1 — Bradicardia',
     ['Compara V_out vs V_ref (60 BPM)', 'Se activa si BPM < 60',
      '(V_out por debajo del umbral)'], '#FDFBE4', '#D4AC0D'),
    (COMP2_X, 'Comparador 2 — Taquicardia',
     ['Compara V_out vs V_ref (100 BPM)', 'Se activa si BPM > 100',
      '(V_out por encima del umbral)'], '#FDEDEC', '#C0392B'),
]

for cx, title, subs, fc, ec in comparators:
    rbox(cx - CMP_W / 2, CMP_CY - CMP_H / 2, CMP_W, CMP_H, fc, ec, lw=2.2)
    ax.text(cx, CMP_CY + 0.44, title,
            ha='center', va='center', fontsize=9.5,
            fontweight='bold', color='#1A252F', zorder=5)
    for j, s in enumerate(subs):
        ax.text(cx, CMP_CY + 0.06 - j * 0.32, s,
                ha='center', va='center', fontsize=8, color='#5D6D7E', zorder=5)

# ══════════════════════════════════════════════════════════════════════════════
# LEDS — same columns and widths as the comparators
# ══════════════════════════════════════════════════════════════════════════════
leds = [
    (COMP1_X, '#F1C40F', '#D4AC0D', 'LED 1', 'Alarma bradicardia'),
    (COMP2_X, '#E74C3C', '#C0392B', 'LED 2', 'Alarma taquicardia'),
]

for cx, dot_c, ec, label, sublabel in leds:
    rbox(cx - LED_W / 2, LED_CY - LED_H / 2, LED_W, LED_H, 'white', ec, lw=2.2)
    ax.add_patch(plt.Circle((cx - LED_W / 2 + 0.65, LED_CY), 0.27,
                             color=dot_c, zorder=5))
    ax.text(cx + 0.25, LED_CY + 0.18, label,
            ha='center', va='center', fontsize=10,
            fontweight='bold', color='#1A252F', zorder=5)
    ax.text(cx + 0.25, LED_CY - 0.22, sublabel,
            ha='center', va='center', fontsize=8.5, color='#5D6D7E', zorder=5)
    arr(cx, CMP_CY - CMP_H / 2, cx, LED_CY + LED_H / 2,
        '#2C3E50', lw=2.0, scale=14)

# ══════════════════════════════════════════════════════════════════════════════
# NOTES — right column, top aligned with comparators, bottom with LEDs
# ══════════════════════════════════════════════════════════════════════════════
NY0 = LED_CY - LED_H / 2                      # 3.05  (LED bottom)
NY1 = CMP_CY + CMP_H / 2                      # 6.95  (comparator top)
rbox(NOTES_L, NY0, NOTES_R - NOTES_L, NY1 - NY0, 'white', '#AEB6BF',
     lw=1.8, r=0.28)
ax.text(NOTES_L + 0.35, NY1 - 0.38, 'Notas de diseño',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color='#1A252F', zorder=5)
ax.plot([NOTES_L + 0.25, NOTES_R - 0.25], [NY1 - 0.62] * 2,
        color='#BDC3C7', lw=1, zorder=4)

notes = [
    ('Todas las etapas con AO 741. No superar el voltaje de saturación\n'
     '(≈ ±V_sat) en ninguna etapa.', 2),
    ('El filtro activo (etapa 4) atenúa el ruido antes de la comparación;\n'
     'cubre el requisito del Avance 2 de mostrar la "señal filtrada".', 2),
    ('La rama de alarmas parte del convertidor F-V: como V_out ≈ BPM,\n'
     'comparar contra dos voltajes equivale a 60 y 100 BPM.', 2),
    ('Rango normal: 60–100 BPM (ninguna alarma activa).', 1),
]

ny = NY1 - 0.92
LINE_H, GAP_N = 0.25, 0.34
for text, n_lines in notes:
    ax.plot(NOTES_L + 0.42, ny, 's', color='#2C3E50', ms=4.5, zorder=5)
    ax.text(NOTES_L + 0.70, ny + 0.09, text, ha='left', va='top',
            fontsize=8, color='#2C3E50', zorder=5, linespacing=1.45)
    ny -= n_lines * LINE_H + GAP_N

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
plt.savefig('diagrama_ecg_mejorado.png', dpi=300, bbox_inches='tight',
            pad_inches=0.15, facecolor=fig.get_facecolor())
print('Saved: diagrama_ecg_mejorado.png')
