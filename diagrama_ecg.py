import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── canvas ────────────────────────────────────────────────────────────────────
FW, FH = 26, 12.5
fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(2.9, FH)          # clip bottom empty space
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')
ax.set_facecolor('#F8F9FA')

# ── helpers ───────────────────────────────────────────────────────────────────
def rbox(x, y, w, h, fc, ec, lw=2.0, r=0.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3))

def arr(x0, y0, x1, y1, color, lw=2.2, scale=14, conn=None):
    kw = dict(arrowstyle='->', color=color, lw=lw, mutation_scale=scale)
    if conn:
        kw['connectionstyle'] = conn
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=kw, zorder=4)

def pill(x, y, txt, fc, ec='none', fs=8.5, tc='white', pad=0.32):
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', zorder=7,
            bbox=dict(boxstyle=f'round,pad={pad}', facecolor=fc,
                      edgecolor=ec, linewidth=1.3, alpha=0.97))

def sec_header(x, y, w, h, ec, lc, text, tc):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle='round,pad=0,rounding_size=0.2',
        facecolor='none', edgecolor=ec, linewidth=1.8, zorder=2))
    ax.plot([x, x], [y, y + h], color=lc, lw=5, solid_capstyle='round', zorder=3)
    ax.text(x + 0.45, y + h / 2, text, ha='left', va='center',
            fontsize=9.5, color=tc, fontweight='bold')

# ── layout constants ──────────────────────────────────────────────────────────
BLK_W, BLK_H = 2.9, 1.65
BLK_CY  = 9.45     # vertical centre of main blocks
GAP     = 0.50     # gap between consecutive blocks
BUS_Y   = 7.55     # horizontal distribution bus
COMP1_X = 5.0
COMP2_X = 11.5
CMP_W, CMP_H = 3.8, 1.6
CMP_CY  = 5.75
LED_W, LED_H = 3.8, 1.25
LED_CY  = 3.9

def blk_cx(i):
    return 0.55 + BLK_W / 2 + i * (BLK_W + GAP)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(13, 12.1,
        'Sistema de Monitoreo de Frecuencia Cardíaca (ECG simulado)',
        ha='center', va='center', fontsize=17, fontweight='bold', color='#1A252F')
ax.text(13, 11.73,
        'Diagrama de bloques · Avance 1 · Circuitos Integrados Lineales · '
        'Implementación únicamente con amplificadores operacionales 741',
        ha='center', va='center', fontsize=9, color='#6C7A89')
ax.plot([5, 21], [11.5, 11.5], color='#BDC3C7', lw=0.9)

# ── CADENA section header ────────────────────────────────────────────────────
chain_right = blk_cx(5) + BLK_W / 2 + 0.35
# header top aligns just above LABEL_Y (which isn't defined yet at module scope;
# use the explicit value: BLK_CY + BLK_H/2 + 0.19 = 9.45+0.825+0.19 = 10.465)
sec_header(0.4, 10.70, chain_right - 0.4, 0.46,
           '#2E86AB', '#2E86AB',
           'CADENA DE ACONDICIONAMIENTO Y PROCESAMIENTO DE SEÑAL',
           '#1A5276')

# ── BLOCKS 1-6 ───────────────────────────────────────────────────────────────
block_specs = [
    ('1', 'Generador de\nfunciones (ECG)',
     '5 – 50 mVpp\n1 – 2.5 Hz · 60 – 150 BPM',   '#1A5276', '#EAF4FB', '#2E86C1'),
    ('2', 'Seguidor de\nvoltaje (buffer)',
     'Ganancia = 1\nAlta Z_in · aislamiento',       '#1A5276', '#EAF4FB', '#2E86C1'),
    ('3', 'Amplificador\nno inversor',
     'A_v = 1 + Rf / Ri\nAcondiciona amplitud',     '#1A5276', '#EAF4FB', '#2E86C1'),
    ('4', 'Filtro activo\n(pasa-bajas)',
     'Reduce ruido\nf_c por encima de 2.5 Hz',      '#1A3A5C', '#D6EAF8', '#2471A3'),
    ('5', 'Comparador (V_R)\ndetector de latidos',
     'Umbral V_R\nGenera tren de pulsos',            '#1A5276', '#EAF4FB', '#2E86C1'),
    ('6', 'Convertidor\nfrecuencia-voltaje',
     'F → V (CD)\nSalida 0-10 V ≈ BPM',            '#145A32', '#D5F5E3', '#1E8449'),
]

for i, (num, title, sub, nc, bfc, bec) in enumerate(block_specs):
    cx = blk_cx(i)
    bx, by = cx - BLK_W / 2, BLK_CY - BLK_H / 2
    rbox(bx, by, BLK_W, BLK_H, bfc, bec, lw=2.0)
    ax.add_patch(plt.Circle((bx + 0.38, by + BLK_H - 0.38), 0.26,
                             color=nc, zorder=5))
    ax.text(bx + 0.38, by + BLK_H - 0.38, num,
            ha='center', va='center', fontsize=9, color='white',
            fontweight='bold', zorder=6)
    ax.text(cx, BLK_CY + 0.22, title,
            ha='center', va='center', fontsize=9.5,
            color='#1A252F', fontweight='bold', zorder=5)
    ax.text(cx, BLK_CY - 0.46, sub,
            ha='center', va='center', fontsize=7.5, color='#5D6D7E', zorder=5)

# ── INTER-BLOCK ARROWS  +  labels positioned ON the arrow line ───────────────
arrow_labels = ['buffer', 'amplif.', 'filtrado', 'pulsos']
pill_colors  = ['#2471A3', '#2471A3', '#1E8449', '#1E8449']

LABEL_Y = BLK_CY + BLK_H / 2 + 0.19   # just above block tops, inside section header

for i in range(5):
    x0 = blk_cx(i) + BLK_W / 2
    x1 = blk_cx(i + 1) - BLK_W / 2
    xm = (x0 + x1) / 2
    arr(x0, BLK_CY, x1, BLK_CY, '#34495E', lw=2.0, scale=13)
    if i < 4:
        # labels float ABOVE block tops — no overlap with block content
        pill(xm, LABEL_Y, arrow_labels[i], pill_colors[i],
             ec=pill_colors[i], fs=7.5, pad=0.22)

# ── SALIDA PROPORCIONAL ───────────────────────────────────────────────────────
SP_W, SP_H = 3.2, 1.65
SP_LEFT = blk_cx(5) + BLK_W / 2 + 0.65
SP_CX   = SP_LEFT + SP_W / 2
SP_CY   = BLK_CY

rbox(SP_LEFT, SP_CY - SP_H / 2, SP_W, SP_H, '#D5F5E3', '#1E8449', lw=2.2, r=0.3)
ax.text(SP_CX, SP_CY + 0.28, 'Salida proporcional',
        ha='center', va='center', fontsize=9.5, fontweight='bold',
        color='#145A32', zorder=5)
ax.text(SP_CX, SP_CY - 0.22,
        'Señal continua 0–10 V\nproporcional a la\nfrecuencia cardíaca (BPM)',
        ha='center', va='center', fontsize=8, color='#1E8449', zorder=5)

# horizontal arrow block-6 → Salida proporcional
arr(blk_cx(5) + BLK_W / 2, BLK_CY, SP_LEFT, SP_CY, '#1E8449', lw=2.2)

# ── GREEN BUS ─────────────────────────────────────────────────────────────────
# vertical drop block-6 bottom → bus
arr(blk_cx(5), BLK_CY - BLK_H / 2, blk_cx(5), BUS_Y, '#1E8449', lw=2.5)

# horizontal bus line (no arrowhead)
ax.plot([COMP1_X, blk_cx(5)], [BUS_Y, BUS_Y],
        color='#1E8449', lw=2.5, zorder=4)

# junction dots
for xd in [COMP1_X, COMP2_X]:
    ax.plot(xd, BUS_Y, 'o', color='#1E8449', ms=9, zorder=5)

# bus label: solid pill ABOVE the line, centred over its span
bus_lx = (COMP1_X + blk_cx(5)) / 2
pill(bus_lx, BUS_Y + 0.46,
     'V_out (0–10 V)  —  alimenta los comparadores de alarma',
     '#1E8449', ec='#145A32', fs=9)

# ── ALARMAS section header ────────────────────────────────────────────────────
sec_header(0.4, 6.98, 14.8, 0.46,
           '#C0392B', '#C0392B',
           'ETAPA DE ALARMAS (FUERA DE RANGO NORMAL)',
           '#922B21')

# ── COMPARATORS ──────────────────────────────────────────────────────────────
for cx, title, subs, fc, ec in [
    (COMP1_X, 'Comparador 1 — Bradicardia',
     ['Compara V_out vs V_ref (60 BPM)', 'Se activa si BPM < 60',
      '(V_out por debajo del umbral)'],
     '#FDFBE4', '#D4AC0D'),
    (COMP2_X, 'Comparador 2 — Taquicardia',
     ['Compara V_out vs V_ref (100 BPM)', 'Se activa si BPM > 100',
      '(V_out por encima del umbral)'],
     '#FDEDEC', '#C0392B'),
]:
    rbox(cx - CMP_W / 2, CMP_CY - CMP_H / 2, CMP_W, CMP_H, fc, ec, lw=2.2)
    ax.text(cx, CMP_CY + 0.38, title,
            ha='center', va='center', fontsize=9.5,
            fontweight='bold', color='#1A252F', zorder=5)
    for j, s in enumerate(subs):
        ax.text(cx, CMP_CY + 0.02 - j * 0.33, s,
                ha='center', va='center', fontsize=8, color='#5D6D7E', zorder=5)
    arr(cx, BUS_Y, cx, CMP_CY + CMP_H / 2, '#1E8449', lw=2.2)

# ── LEDs ─────────────────────────────────────────────────────────────────────
for cx, dot_c, ec, label, sublabel in [
    (COMP1_X, '#F1C40F', '#D4AC0D', 'LED 1', 'Alarma bradicardia'),
    (COMP2_X, '#E74C3C', '#C0392B', 'LED 2', 'Alarma taquicardia'),
]:
    rbox(cx - LED_W / 2, LED_CY - LED_H / 2, LED_W, LED_H,
         'white', ec, lw=2.2)
    ax.add_patch(plt.Circle((cx - LED_W / 2 + 0.55, LED_CY), 0.28,
                             color=dot_c, zorder=5))
    ax.text(cx + 0.2, LED_CY + 0.16, label,
            ha='center', va='center', fontsize=10,
            fontweight='bold', color='#1A252F', zorder=5)
    ax.text(cx + 0.2, LED_CY - 0.2, sublabel,
            ha='center', va='center', fontsize=8.5, color='#5D6D7E', zorder=5)
    arr(cx, CMP_CY - CMP_H / 2, cx, LED_CY + LED_H / 2,
        '#2C3E50', lw=2.0, scale=13)

# ── DESIGN NOTES ─────────────────────────────────────────────────────────────
NX, NY, NW, NH = 16.0, 3.15, 9.65, 4.3
rbox(NX, NY, NW, NH, 'white', '#AEB6BF', lw=1.8, r=0.3)
ax.text(NX + 0.3, NY + NH - 0.35, 'Notas de diseño',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color='#1A252F', zorder=5)
ax.plot([NX + 0.2, NX + NW - 0.2], [NY + NH - 0.58] * 2,
        color='#BDC3C7', lw=1, zorder=4)

notes = [
    ('Todas las etapas con AO 741. No superar el voltaje de\n'
     'saturación (≈ ±V_sat) en ninguna etapa.', 2),
    ('El filtro activo (etapa 4) atenúa el ruido antes de la\n'
     'comparación; cubre el requisito del Avance 2 de\n'
     'mostrar la "señal filtrada".', 3),
    ('La rama de alarmas parte de la salida del convertidor F-V:\n'
     'como V_out ≈ BPM, comparar contra dos voltajes\n'
     'equivale a 60 y 100 BPM.', 3),
    ('Rango normal: 60–100 BPM (ninguna alarma activa).', 1),
]

ny = NY + NH - 0.85
LINE_H = 0.255   # height per line of text
GAP_N  = 0.38    # extra gap between notes

for text, n_lines in notes:
    ax.plot(NX + 0.38, ny, 's', color='#2C3E50', ms=4.5, zorder=5)
    ax.text(NX + 0.65, ny, text, ha='left', va='top',
            fontsize=8, color='#2C3E50', zorder=5, linespacing=1.45)
    ny -= n_lines * LINE_H + GAP_N

# ── SAVE ─────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig('diagrama_ecg_mejorado.png', dpi=180, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print('Saved: diagrama_ecg_mejorado.png')
