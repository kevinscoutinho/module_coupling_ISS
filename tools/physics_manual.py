# Gera o HTML da seção "Física do jogo" (texto, equações e diagramas SVG)
import math

def eq(body, n):
    return f'<div class="eq"><div class="eq-m">{body}</div><span class="eq-n">({n})</span></div>'
def fr(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'
def v(x):
    return f'<span class="vec">{x}</span>'
def i(x):
    return f'<i>{x}</i>'

def arrow(x1, y1, x2, y2, cls='A', w=3, dash=False):
    d = ' stroke-dasharray="6 5"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="s{cls}" stroke-width="{w}" marker-end="url(#ah{cls})"{d}/>'
def line(x1, y1, x2, y2, cls='D', w=1.5, dash=False):
    d = ' stroke-dasharray="5 5"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="s{cls}" stroke-width="{w}"{d}/>'
def text(x, y, s, cls='ink', anchor='start', size=None, extra=''):
    sz = f' font-size="{size}"' if size else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{sz}{extra}>{s}</text>'
def mod(x, y, s=1.0, rot=0.0, op=1.0):
    return f'<use href="#gm" transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({s})" opacity="{op}"/>'
def rock(x, y, r, label=None):
    out = f'<use href="#gr" transform="translate({x:.1f},{y:.1f}) scale({r})"/>'
    if label: out += text(x, y + 5, label, 'ink', 'middle', 12)
    return out
def gas(x, y, dx, dy, n=14, spread=0.35, length=150, seed=1):
    import random
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        t = (k + rnd.random()) / n
        dist = 14 + t * length
        px, py = -dy, dx
        off = (rnd.random() - 0.5) * 2 * spread * dist
        cx, cy = x + dx * dist + px * off, y + dy * dist + py * off
        rr = 2 + t * 3.5
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" class="fC" opacity="{0.9 - t*0.6:.2f}"/>')
    return ''.join(out)
def arc(cx, cy, r, a0, a1, cls='R', sweep=0, w=3):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" class="s{cls}" stroke-width="{w}" fill="none" marker-end="url(#ah{cls})"/>'
def svg(vb_w, vb_h, body, label):
    return f'<svg class="fig" viewBox="0 0 {vb_w} {vb_h}" role="img" aria-label="{label}">{body}</svg>'
def figure(n, svgcode, cap):
    return f'<figure>{svgcode}<figcaption><b>Figura {n}.</b> {cap}</figcaption></figure>'

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
''' + ''.join(f'<marker id="ah{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="f{c}"/></marker>' for c in 'ACGRD') + '''
<g id="gm">
  <rect x="-66" y="-14" width="8" height="28" rx="2" fill="#3a404a"/>
  <rect x="-60" y="-20" width="110" height="40" rx="6" fill="#e8edf2" stroke="#9aa6b4" stroke-width="1.2"/>
  <rect x="-50" y="-20.5" width="32" height="41" fill="#d9a440" opacity="0.85"/>
  <line x1="-4" y1="-20" x2="-4" y2="20" stroke="#9aa6b4"/><line x1="36" y1="-20" x2="36" y2="20" stroke="#9aa6b4"/>
  <path d="M50,-20 L62,-13 L62,13 L50,20 z" fill="#8b939e"/>
  <rect x="62" y="-2" width="12" height="4" fill="#8b939e"/>
  <circle cx="75" cy="0" r="3.2" fill="#ffb547"/>
  <circle cx="16" cy="-5" r="3.4" fill="#10202e"/><circle cx="28" cy="-5" r="3.4" fill="#10202e"/>
  <circle cx="0" cy="0" r="3" fill="#ff8fbf" stroke="#7a2a4c" stroke-width="1"/>
</g>
<path id="gr" d="M1,0 L0.83,0.5 L0.45,0.92 L-0.1,1.02 L-0.6,0.8 L-0.98,0.3 L-0.95,-0.25 L-0.7,-0.75 L-0.2,-1.0 L0.35,-0.93 L0.8,-0.6 Z" fill="#6a5d52" stroke="#a8968a" stroke-width="1.4" vector-effect="non-scaling-stroke"/>
</defs></svg>'''

# ------------------------------------------------------------------ figuras
def fig1():
    b = text(20, 28, 'NA TERRA, COM ATRITO', 'lbl')
    b += line(20, 112, 660, 112, 'D', 2)
    for k in range(0, 660, 18): b += line(20 + k, 112, 10 + k, 122, 'D', 1)
    xs = [30, 180, 290, 365, 415]
    for k, x in enumerate(xs):
        op = 0.25 + 0.75 * k / 4
        b += f'<rect x="{x}" y="72" width="50" height="40" rx="3" class="crate" opacity="{op:.2f}"/>'
        b += text(x + 25, 140, f't = {k} s' if k == 0 else f'{k} s', 'dim', 'middle', 12)
    b += arrow(520, 92, 476, 92, 'A', 3) + text(530, 74, 'atrito freia:', 'ink', 'start', 13) + text(530, 89, 'cada segundo', 'dim', 'start', 12) + text(530, 103, 'anda menos', 'dim', 'start', 12)
    b += text(20, 182, 'NO ESPAÇO, SEM ATRITO', 'lbl')
    xs = [70, 195, 320, 445, 570]
    for k, x in enumerate(xs):
        b += mod(x, 240, 0.48, 0, 0.25 + 0.75 * k / 4)
        b += text(x, 282, f't = {k} s' if k == 0 else f'{k} s', 'dim', 'middle', 12)
        if k < 4:
            b += f'<line x1="{x+4}" y1="208" x2="{x+121}" y2="208" class="sG" stroke-width="2" marker-start="url(#ahG)" marker-end="url(#ahG)"/>'
            b += text(x + 62, 200, 'Δx', 'fG', 'middle', 13)
    b += text(660, 182, 'mesma distância a cada segundo', 'dim', 'end', 12)
    return svg(680, 296, b, 'Comparação: caixa freada pelo atrito na Terra e módulo em velocidade constante no espaço')

def fig2():
    b = mod(330, 130, 1.0)
    b += gas(404, 118, 1, 0, 16, 0.1, 170, 3) + gas(404, 142, 1, 0, 16, 0.1, 170, 7)
    b += arrow(430, 70, 600, 70, 'C', 3) + text(515, 58, 'gás expelido para a DIREITA', 'fC', 'middle', 13)
    b += text(515, 90, 'massa m · velocidade v', 'dim', 'middle', 12)
    b += arrow(250, 70, 90, 70, 'A', 4) + text(170, 58, 'módulo empurrado para a ESQUERDA', 'fA', 'middle', 13)
    b += text(170, 90, 'massa M · ganho de velocidade Δv', 'dim', 'middle', 12)
    b += f'<rect x="300" y="190" width="60" height="38" rx="5" class="keycap"/>' + text(330, 216, 'D', 'ink', 'middle', 20, ' font-weight="700"')
    b += text(372, 206, 'tecla D: liga o jato do', 'dim', 'start', 12) + text(372, 222, 'lado direito do módulo', 'dim', 'start', 12)
    return svg(680, 245, b, 'Terceira lei de Newton: o gás sai para a direita e o módulo é empurrado para a esquerda')

def fig3():
    X = lambda t: 70 + t * 47.5
    Y = lambda vv: 250 - vv * 190
    b = ''
    for t in range(0, 13, 2): b += line(X(t), Y(0), X(t), Y(1.0), 'L', 1) + text(X(t), 268, str(t), 'dim', 'middle', 12)
    for vv in [0, 0.25, 0.5, 0.75, 1.0]: b += line(X(0), Y(vv), X(12), Y(vv), 'L', 1) + text(X(0) - 8, Y(vv) + 4, f'{vv:.2f}'.replace('.', ','), 'dim', 'end', 12)
    pts = [(0, 0), (2, 0.84), (10, 0.84), (12, 0)]
    poly = ' '.join(f'{X(t):.1f},{Y(vv):.1f}' for t, vv in pts)
    b += f'<polygon points="{poly}" class="area"/>'
    b += f'<polyline points="{poly}" class="sG" stroke-width="3.5" fill="none"/>'
    b += line(X(0), Y(0), X(12), Y(0), 'D', 1.5) + line(X(0), Y(0), X(0), Y(1.0), 'D', 1.5)
    b += text(X(1) + 8, Y(0.42) + 4, 'acelera', 'ink', 'start', 13)
    b += text(X(6), Y(0.84) - 12, 'inércia: velocidade constante, jatos desligados', 'ink', 'middle', 13)
    b += text(X(11) - 8, Y(0.42) + 4, 'freia', 'ink', 'end', 13)
    b += text(X(6), Y(0.38), 'área sob a linha = distância', 'fG', 'middle', 14)
    b += text(X(6), Y(0.38) + 18, '0,84 + 6,72 + 0,84 = 8,4 m', 'dim', 'middle', 13)
    b += text(X(0) - 52, Y(1.0) - 14, 'velocidade (m/s)', 'dim', 'start', 12)
    b += f'<rect x="{X(0):.1f}" y="292" width="{X(2)-X(0):.1f}" height="12" rx="2" class="fC"/>' + text(X(1), 318, 'A ligado', 'fC', 'middle', 12)
    b += f'<rect x="{X(10):.1f}" y="292" width="{X(12)-X(10):.1f}" height="12" rx="2" class="fC"/>' + text(X(11), 318, 'D ligado', 'fC', 'middle', 12)
    b += text(X(12), 284, 'tempo (s)', 'dim', 'end', 12)
    return svg(680, 326, b, 'Gráfico de velocidade por tempo: acelera por 2 segundos, segue constante por 8 segundos, freia por 2 segundos')

def fig4():
    cx, cy, s = 330, 150, 1.4
    b = mod(cx, cy, s)
    xn, xt = cx + 1.25 * 30.6 * s, cx - 1.6 * 30.6 * s
    yb, yt = cy + 0.9 * 30.6 * s, cy - 0.9 * 30.6 * s
    b += gas(xn, yb, 0, 1, 10, 0.25, 70, 11) + gas(xt, yt, 0, -1, 10, 0.25, 70, 13)
    b += arrow(xn, cy - 30, xn, cy - 92, 'A', 4) + text(xn + 10, cy - 70, 'F', 'mi fA')
    b += arrow(xt, cy + 30, xt, cy + 92, 'A', 4) + text(xt - 22, cy + 82, 'F', 'mi fA')
    b += text(xn + 12, yb + 40, 'gás para baixo', 'fC', 'start', 12) + text(xt - 34, yt - 30, 'gás para cima', 'fC', 'end', 12)
    b += f'<line x1="{xt:.1f}" y1="268" x2="{xn:.1f}" y2="268" class="sD" stroke-width="1.5" marker-start="url(#ahD)" marker-end="url(#ahD)"/>'
    b += line(xt, cy + 96, xt, 274, 'D', 1, True) + line(xn, cy + 20, xn, 274, 'D', 1, True)
    b += text((xt + xn) / 2, 288, 'd = 2,85 m (braço entre os dois jatos)', 'ink', 'middle', 13)
    b += arc(cx, cy, 128, -25, -155, 'R', 0, 3)
    b += text(cx, 14, 'tecla Q: os dois jatos juntos giram o módulo no sentido anti-horário', 'fR', 'middle', 13)
    b += text(520, 140, 'as duas forças', 'ink', 'start', 13) + text(520, 157, 'se anulam para', 'ink', 'start', 13) + text(520, 174, 'andar, mas', 'ink', 'start', 13) + text(520, 191, 'somam para girar', 'fR', 'start', 13)
    return svg(680, 300, b, 'Binário de forças: um jato no nariz empurra para cima e outro na cauda empurra para baixo, girando o módulo')

def fig5():
    O = (90, 270)
    b = arrow(O[0], O[1], 650, O[1], 'D', 1.5) + arrow(O[0], O[1], O[0], 24, 'D', 1.5)
    b += text(640, O[1] + 22, 'x (tela / mundo)', 'dim', 'end', 12) + text(O[0] + 8, 30, 'y', 'dim', 'start', 12)
    cx, cy, th = 400, 150, 30
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    b += mod(cx, cy, 1.0, -th)
    b += line(cx, cy, cx + 175, cy, 'D', 1.2, True)
    b += arrow(cx, cy, cx + 190 * c, cy - 190 * s, 'C', 1.8) + text(cx + 196 * c, cy - 196 * s - 4, "x′ (módulo)", 'fC', 'start', 12)
    b += arrow(cx, cy, cx - 110 * s, cy - 110 * c, 'C', 1.8) + text(cx - 116 * s - 4, cy - 116 * c - 6, "y′", 'fC', 'end', 13)
    b += arc(cx, cy, 70, 0, -th, 'R', 0, 2) + text(cx + 82, cy - 14, 'θ', 'mi fR')
    F = 170
    fx, fy = cx - F * c, cy + F * s
    b += line(cx, cy, fx, cy, 'A', 2, True) + line(fx, cy, fx, fy, 'A', 2, True)
    b += arrow(cx, cy, fx, fy, 'A', 4)
    b += text((cx + fx) / 2, cy - 8, 'F · cos θ', 'mi fA', 'middle')
    b += text(fx - 10, (cy + fy) / 2 + 5, 'F · sen θ', 'mi fA', 'end')
    b += text(fx + 4, fy + 22, 'empuxo do jato D', 'fA', 'start', 12)
    nx, ny = cx + 80 * c, cy - 80 * s
    b += gas(nx, ny, c, -s, 10, 0.2, 90, 21)
    return svg(680, 300, b, 'Módulo inclinado 30 graus: o empuxo do jato D se divide em componente horizontal F cos theta e vertical F sen theta')

def fig6():
    labels = [('1. Ler', 'teclas'), ('2. Somar', 'forças'), ('3. Calcular', 'a = F/m'), ('4. Atualizar', 'v += a·Δt'), ('5. Atualizar', 'x += v·Δt'), ('6. Testar', 'colisões')]
    b = ''
    for k, (l1, l2) in enumerate(labels):
        x = 10 + k * 112
        b += f'<rect x="{x}" y="40" width="96" height="68" rx="5" class="box"/>'
        b += text(x + 48, 68, l1, 'ink', 'middle', 13) + text(x + 48, 88, l2, 'fC', 'middle', 13)
        if k < 5: b += arrow(x + 98, 74, x + 120, 74, 'D', 1.8)
    b += f'<path d="M626,110 L626,150 L58,150 L58,114" class="sD" stroke-width="1.8" fill="none" marker-end="url(#ahD)"/>'
    b += text(340, 174, 'repete a cada Δt = 1/120 s, ou seja, 120 vezes por segundo', 'ink', 'middle', 13)
    return svg(680, 186, b, 'Ciclo da simulação: ler teclas, somar forças, calcular aceleração, atualizar velocidade e posição, testar colisões')

def fig7():
    b = line(226, 20, 226, 220, 'L', 1) + line(453, 20, 453, 220, 'L', 1)
    b += text(113, 26, 'ANTES', 'lbl', 'middle') + text(340, 26, 'CONTATO', 'lbl', 'middle') + text(566, 26, 'DEPOIS', 'lbl', 'middle')
    k = 200
    b += rock(70, 130, 34, 'A · 30 t') + rock(176, 130, 22, 'B · 8 t')
    b += arrow(40, 82, 40 + 0.30 * k, 82, 'G', 3) + text(70, 70, '0,30 m/s', 'fG', 'middle', 12)
    b += arrow(196, 82, 196 - 0.10 * k, 82, 'G', 3) + text(180, 70, '0,10 m/s', 'fG', 'middle', 12)
    b += rock(305, 130, 34, 'A') + rock(361, 130, 22, 'B')
    b += line(250, 130, 420, 130, 'R', 1.2, True) + text(420, 122, 'n', 'mi fR', 'end')
    b += arrow(345, 186, 405, 186, 'A', 3.5) + text(410, 191, '+J', 'mi fA')
    b += arrow(335, 206, 275, 206, 'A', 3.5) + text(270, 211, '−J', 'mi fA', 'end')
    b += rock(505, 130, 34, 'A') + rock(590, 130, 22, 'B')
    b += arrow(490, 82, 490 + 0.165 * k, 82, 'G', 3) + text(505, 70, '0,17 m/s', 'fG', 'middle', 12)
    b += arrow(575, 82, 575 + 0.405 * k, 82, 'G', 3) + text(610, 70, '0,41 m/s', 'fG', 'middle', 12)
    b += text(340, 250, 'momento antes: 30 000 × 0,30 − 8 000 × 0,10 = 8 200 kg·m/s', 'ink', 'middle', 13)
    b += text(340, 272, 'momento depois: 30 000 × 0,165 + 8 000 × 0,405 = 8 200 kg·m/s', 'ink', 'middle', 13)
    b += text(340, 294, 'o total não muda: só foi redistribuído entre as duas rochas', 'fG', 'middle', 13)
    return svg(680, 306, b, 'Colisão frontal entre dois asteroides: antes, contato com impulsos iguais e opostos, e depois, com o momento total conservado')

def fig8():
    b = text(200, 26, 'CHOQUE PERTO DO NARIZ', 'lbl', 'middle') + text(560, 26, 'CHOQUE NO CENTRO', 'lbl', 'middle')
    b += line(410, 20, 410, 280, 'L', 1)
    cx, cy, s = 190, 150, 1.2
    b += mod(cx, cy, s)
    px, py = cx + 70, cy + 24
    b += rock(px, py + 32, 32)
    b += f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" class="sR" stroke-width="2" stroke-dasharray="5 4"/>' + text(cx + 26, cy + 30, 'r', 'mi fR')
    b += arrow(px, py, px, py - 66, 'A', 4) + text(px + 10, py - 52, 'J', 'mi fA')
    b += f'<circle cx="{px}" cy="{py}" r="4" class="fA"/>' + text(px + 10, py + 6, 'P', 'mi ink')
    b += arrow(cx, cy, cx, cy - 78, 'G', 3) + text(cx - 10, cy - 68, 'Δv', 'mi fG', 'end')
    b += arc(cx, cy, 108, 20, -60, 'R', 0, 3) + text(cx + 112, cy - 92, 'Δω', 'mi fR')
    b += text(200, 262, 'o empurrão desloca o centro de massa', 'ink', 'middle', 12) + text(200, 278, 'e faz o módulo girar', 'fR', 'middle', 12)
    cx2 = 560
    b += mod(cx2, cy, 0.8)
    b += rock(cx2, cy + 16 + 22, 22)
    b += arrow(cx2, cy + 14, cx2, cy - 60, 'A', 4) + text(cx2 + 10, cy - 46, 'J', 'mi fA')
    b += text(cx2, 262, 'r e n na mesma linha: r × n = 0', 'ink', 'middle', 12) + text(cx2, 278, 'só empurra, não gira', 'fG', 'middle', 12)
    return svg(680, 290, b, 'Choque fora do centro faz o módulo andar e girar; choque alinhado ao centro só empurra')

def fig9():
    b = f'<rect x="470" y="70" width="190" height="160" rx="6" class="mBody"/>'
    b += f'<rect x="458" y="112" width="14" height="76" rx="2" class="mGrey"/>' + f'<rect x="452" y="128" width="8" height="44" class="mDark"/>'
    b += text(565, 156, 'porto da ISS', 'dimdark', 'middle', 13)
    b += line(20, 150, 452, 150, 'D', 1.2, True)
    b += f'<rect x="396" y="125" width="56" height="50" class="band"/>'
    b += f'<line x1="410" y1="125" x2="410" y2="175" class="sA" stroke-width="1.5" marker-start="url(#ahA)" marker-end="url(#ahA)"/>'
    b += text(424, 194, '± 0,25 m', 'fA', 'middle', 12)
    th = 3
    mx, my = 300, 156
    b += mod(mx, my, 1.0, -th)
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    b += line(mx, my, mx + 150 * c, my - 150 * s, 'C', 1.2, True)
    b += line(mx, my, mx + 160, my, 'D', 1, True)
    b += arc(mx, my, 96, 0, -th - 5, 'R', 0, 2) + text(mx + 70, my - 40, 'atitude θ ≤ 4°', 'fR', 'middle', 12)
    b += arrow(230, 230, 330, 230, 'G', 3) + text(280, 252, 'aproximação ≤ 0,25 m/s', 'fG', 'middle', 12)
    b += arrow(110, 226, 110, 196, 'G', 3) + text(110, 252, 'lateral ≤ 0,10 m/s', 'fG', 'middle', 12)
    b += arc(mx, my, 44, 140, 210, 'R', 1, 2) + text(mx - 54, my + 46, 'ω ≤ 2 °/s', 'fR', 'end', 12)
    b += text(20, 40, 'OS CINCO CRITÉRIOS PRECISAM VALER AO MESMO TEMPO', 'lbl')
    return svg(680, 268, b, 'Critérios de acoplamento: velocidade de aproximação, velocidade lateral, atitude, rotação e alinhamento')

def fig10():
    ex, ey, er = 210, 200, 108
    b = f'<circle cx="{ex}" cy="{ey}" r="{er}" class="earth"/>'
    b += f'<circle cx="{ex}" cy="{ey}" r="{er+6}" class="atm"/>'
    b += f'<circle cx="{ex}" cy="{ey}" r="160" class="sD" fill="none" stroke-width="1.2" stroke-dasharray="4 6"/>'
    b += text(ex, ey + 5, 'Terra', 'ink', 'middle', 14)
    sx, sy = ex, ey - 160
    b += f'<rect x="{sx-7}" y="{sy-5}" width="14" height="10" rx="2" class="mBody"/>'
    b += arrow(sx, sy, sx + 110, sy, 'G', 3) + text(sx + 116, sy + 4, '≈ 7,8 km/s', 'fG', 'start', 12)
    b += arrow(sx, sy + 4, sx, sy + 62, 'A', 3) + text(sx - 8, sy + 54, 'gravidade', 'fA', 'end', 12)
    b += text(ex, 372, 'a ≈ 400 km de altura, uma volta a cada ≈ 90 min', 'dim', 'middle', 12)
    b += f'<rect x="408" y="30" width="264" height="310" rx="6" class="box"/>'
    b += line(sx + 8, sy - 6, 408, 30, 'L', 1, True) + line(sx + 8, sy + 6, 408, 340, 'L', 1, True)
    b += text(540, 54, 'ZOOM: A CENA DO JOGO', 'lbl', 'middle')
    b += f'<rect x="580" y="110" width="58" height="34" rx="4" class="mBody"/>' + text(609, 160, 'ISS', 'dim', 'middle', 11)
    b += mod(470, 127, 0.33)
    for x0 in (452, 586):
        b += arrow(x0, 196, x0 + 52, 196, 'G', 3)
        b += arrow(x0 + 20, 214, x0 + 20, 258, 'A', 3)
    b += text(540, 286, 'mesma velocidade e mesma queda:', 'ink', 'middle', 12)
    b += text(540, 304, 'um em relação ao outro,', 'fG', 'middle', 12) + text(540, 322, 'quase parados', 'fG', 'middle', 12)
    return svg(680, 386, b, 'Módulo e ISS estão em órbita e caem juntos em direção à Terra, por isso o jogo mostra só o movimento de um em relação ao outro')

# ------------------------------------------------------------------ texto
S = []
S.append(('inercia', 'Sem atrito, sem freio', f'''
<p>Na Terra, quase tudo que se move acaba parando sozinho. Um carrinho de supermercado empurrado e solto rola um pouco e para. Parece natural, mas quem freia o carrinho é o <b>atrito</b> (com o chão e com o ar). Tire o atrito e o carrinho nunca mais para.</p>
<p>É exatamente isso que acontece no espaço. Lá não há chão nem ar para frear o módulo. Isaac Newton resumiu esse comportamento na sua <b>primeira lei</b>, a lei da inércia:</p>
<blockquote>Um corpo continua parado, ou continua andando em linha reta com velocidade constante, até que uma força mude isso.</blockquote>
{figure(1, fig1(), 'Na Terra o atrito rouba velocidade a cada instante. No espaço, sem atrito, o módulo percorre a mesma distância Δx a cada segundo, para sempre, até um jato agir.')}
<p>Quando a velocidade é constante, a posição muda sempre no mesmo ritmo. A equação é:</p>
{eq(f'{i("x")} = {i("x")}<sub>0</sub> + {i("v")} · {i("t")}', 1)}
<p>onde {i("x")}<sub>0</sub> é a posição inicial, {i("v")} é a velocidade e {i("t")} é o tempo. Se o módulo anda a 0,5 m/s, em 10 s ele anda 5 m, em 60 s anda 30 m, e assim por diante.</p>
<div class="box"><b>No jogo.</b> É por isso que soltar a tecla não para o módulo. A telemetria continua mostrando a mesma Vel. X e Vel. Y depois que você solta tudo. A linha tracejada laranja à frente do módulo é a equação (1) desenhada: onde ele vai estar nos próximos 25 s se você não fizer nada.</div>
'''))

S.append(('acao', 'Ação e reação: como um jato empurra', f'''
<p>Se não existe chão para empurrar, como o módulo consegue se mover? A resposta está na <b>terceira lei de Newton</b>: quando um corpo empurra outro, o outro empurra de volta com a mesma força, no sentido oposto.</p>
<p>O jato de ar comprimido empurra gás para fora em alta velocidade. O gás, então, empurra o módulo para o lado contrário. É o mesmo que acontece quando você solta um balão de festa cheio sem amarrar: o ar sai por trás e o balão dispara para a frente.</p>
{figure(2, fig2(), 'Ao apertar D, o jato do lado direito solta gás para a direita. Pela terceira lei, o gás empurra o módulo para a esquerda.')}
<p>Para medir “quanto movimento” um corpo tem, os físicos usam o <b>momento linear</b> (também chamado de quantidade de movimento):</p>
{eq(f'{v("p")} = {i("m")} · {v("v")}', 2)}
<p>A setinha em cima da letra indica que é um <b>vetor</b>: tem tamanho, direção e sentido. Antes do jato ligar, tudo está parado e o momento total é zero. Depois, o gás tem momento para a direita e o módulo tem o mesmo momento para a esquerda, e a soma continua zero:</p>
{eq(f'{i("m")}<sub>gás</sub> · {i("v")}<sub>gás</sub> = {i("M")}<sub>módulo</sub> · Δ{i("v")}<sub>módulo</sub>', 3)}
<p>Como o módulo é muito mais pesado que o gás que sai, ele ganha só um pouquinho de velocidade a cada instante. Quanto mais gás por segundo ({i("ṁ")}) e mais rápido ele sai ({i("v")}<sub>e</sub>), maior a força do jato, chamada de <b>empuxo</b>:</p>
{eq(f'{i("F")}<sub>empuxo</sub> = {i("ṁ")} · {i("v")}<sub>e</sub>', 4)}
<div class="box"><b>Sendo honesto.</b> No jogo, cada jato empurra o módulo de 9 toneladas com cerca de 3 800 N. Jatos reais de gás frio são bem mais fracos, geralmente de poucos newtons a algumas dezenas de newtons. Aumentamos a força para a partida não durar uma hora.</div>
'''))

S.append(('newton2', 'Acelerar e frear: a segunda lei', f'''
<p>A <b>segunda lei de Newton</b> diz quanto a velocidade muda quando uma força age: quanto maior a força, maior a aceleração; quanto maior a massa, menor a aceleração.</p>
{eq(f'{v("F")} = {i("m")} · {v("a")} &nbsp;&nbsp;⟹&nbsp;&nbsp; {v("a")} = {fr(v("F"), i("m"))}', 5)}
<p>No jogo, cada jato produz uma aceleração de {i("a")} = 0,42 m/s². Isso quer dizer que, a cada segundo com o jato ligado, a velocidade aumenta 0,42 m/s. Com aceleração constante, valem estas duas equações:</p>
{eq(f'{i("v")} = {i("v")}<sub>0</sub> + {i("a")} · {i("t")}', 6)}
{eq(f'{i("x")} = {i("x")}<sub>0</sub> + {i("v")}<sub>0</sub> · {i("t")} + {fr("1", "2")} {i("a")} · {i("t")}<sup>2</sup>', 7)}
{figure(3, fig3(), 'Uma viagem completa. O jato A acelera por 2 s, depois o módulo segue por inércia por 8 s, e o jato D freia por 2 s. A área verde sob a linha é a distância percorrida.')}
<div class="box"><b>Exemplo resolvido.</b> Partindo do repouso, você segura A por 2 s.<br>
Velocidade final, pela equação (6): {i("v")} = 0 + 0,42 × 2 = <b>0,84 m/s</b>.<br>
Distância nesses 2 s, pela (7): {i("x")} = ½ × 0,42 × 2² = <b>0,84 m</b>.<br>
Agora repare: 0,84 m/s é mais de três vezes o limite de 0,25 m/s para acoplar, e passa até do limite de 0,8 m/s que destrói o módulo numa batida. Dois segundos de jato já são demais. Pilotos de verdade dão toques curtos.</div>
<p>Para frear, a ideia é a mesma, só que com o jato do lado oposto. A força passa a apontar contra o movimento, a aceleração fica negativa e a velocidade diminui. Para parar exatamente, o tempo de freada precisa ser igual ao tempo de aceleração (se os jatos têm a mesma força).</p>
'''))

S.append(('torque', 'Girar: torque e momento de inércia', f'''
<p>Para girar, não basta uma força: importa <b>onde</b> ela é aplicada. Pense numa porta: empurrar perto da maçaneta abre fácil, empurrar perto da dobradiça quase não funciona. Esse “poder de girar” se chama <b>torque</b> (τ, a letra grega tau):</p>
{eq(f'τ = {i("F")} · {i("d")}', 8)}
<p>onde {i("d")} é a distância entre a linha da força e o ponto de giro. O módulo usa um truque: dois jatos ao mesmo tempo, um no nariz e outro na cauda, empurrando em sentidos opostos. Esse par de forças se chama <b>binário</b>.</p>
{figure(4, fig4(), 'Um binário. As duas forças são iguais e opostas, então o empurrão total é zero e o módulo não sai do lugar. Mas as duas giram para o mesmo lado, então os torques se somam. O ponto rosa é o centro de massa.')}
<p>Assim como a massa resiste a mudanças de velocidade, o <b>momento de inércia</b> ({i("I")}) resiste a mudanças de rotação. Ele depende da massa e de como ela está espalhada: massa longe do centro gira com mais dificuldade. Para um cilindro de massa {i("m")}, raio {i("R")} e comprimento {i("L")}, girando em torno do meio:</p>
{eq(f'{i("I")} = {fr(f"{i("m")} · (3{i("R")}<sup>2</sup> + {i("L")}<sup>2</sup>)", "12")}', 9)}
<p>A “segunda lei para rotação” fica igual à equação (5), trocando força por torque, massa por momento de inércia e aceleração por <b>aceleração angular</b> α:</p>
{eq(f'α = {fr("τ", i("I"))}', 10)}
{eq(f'ω = ω<sub>0</sub> + α · {i("t")} &nbsp;&nbsp;&nbsp;&nbsp; θ = θ<sub>0</sub> + ω · {i("t")}', 11)}
<p>Aqui ω (ômega) é a velocidade de rotação e θ (teta) é o ângulo. Repare como as equações (11) são “gêmeas” das (6) e (1).</p>
<div class="box"><b>No jogo.</b> O módulo tem {i("m")} = 9 000 kg, {i("R")} = 0,85 m e {i("L")} = 4,4 m. Pela equação (9): {i("I")} ≈ 16 150 kg·m². O jogo gira o módulo com α = 10 °/s², que é 0,1745 rad/s². Pela (10), o torque é τ = 16 150 × 0,1745 ≈ 2 820 N·m. Com braço {i("d")} = 2,85 m, cada jato empurra com {i("F")} = τ/{i("d")} ≈ 990 N.<br>E a rotação também tem inércia: depois de soltar Q, o módulo continua girando até você usar E pelo mesmo tempo.</div>
'''))

S.append(('referencial', 'Jatos presos no casco: o referencial do módulo', f'''
<p>Os jatos estão parafusados no módulo. Por isso, “jato da direita” quer dizer direita <b>do módulo</b>, não direita da tela. Se o módulo estiver inclinado, o empurrão sai inclinado também.</p>
{figure(5, fig5(), 'Com o módulo girado de θ = 30°, o empuxo do jato D aponta ao longo do eixo do módulo. A trigonometria separa esse empurrão em uma parte horizontal e outra vertical.')}
<p>Usando seno e cosseno, que você vê no triângulo retângulo, a força se divide em duas componentes:</p>
{eq(f'{i("F")}<sub>x</sub> = {i("F")} · cos θ &nbsp;&nbsp;&nbsp;&nbsp; {i("F")}<sub>y</sub> = {i("F")} · sen θ', 12)}
<p>Em geral, um empurrão com componentes ({i("f")}<sub>x′</sub>, {i("f")}<sub>y′</sub>) medidas no módulo vira, na tela:</p>
{eq(f'{i("F")}<sub>x</sub> = {i("f")}<sub>x′</sub> cos θ − {i("f")}<sub>y′</sub> sen θ<br>{i("F")}<sub>y</sub> = {i("f")}<sub>x′</sub> sen θ + {i("f")}<sub>y′</sub> cos θ', 13)}
<div class="box"><b>Dica de piloto.</b> Se o módulo estiver de lado, apertar A não leva ele para a direita da tela: leva para onde o nariz aponta. Por isso, alinhar o ângulo primeiro (com Q e E) e só depois avançar costuma ser a estratégia mais fácil.</div>
'''))

S.append(('simulacao', 'Como o computador simula tudo isso', f'''
<p>O computador não resolve as equações de uma vez para o futuro inteiro. Ele avança o tempo em passos minúsculos de Δ{i("t")} = 1/120 s (cerca de 8 milésimos de segundo) e, a cada passo, repete a mesma receita:</p>
{figure(6, fig6(), 'O ciclo da física do jogo, repetido 120 vezes por segundo.')}
{eq(f'{v("v")}<sub>novo</sub> = {v("v")} + {v("a")} · Δ{i("t")}', 14)}
{eq(f'{v("x")}<sub>novo</sub> = {v("x")} + {v("v")}<sub>novo</sub> · Δ{i("t")}', 15)}
<p>Esse método se chama <b>Euler semi-implícito</b>. Ele usa a velocidade já atualizada para mover a posição, o que deixa a simulação estável. Como o passo é muito pequeno, o resultado fica praticamente igual ao das equações (6) e (7). O mesmo vale para a rotação: ω recebe α·Δ{i("t")} e θ recebe ω·Δ{i("t")}.</p>
<p>O passo é fixo de propósito. Se o seu computador estiver lento e desenhar menos quadros por segundo, a física faz vários passos por quadro e continua igual. Assim, o módulo se comporta do mesmo jeito em qualquer máquina.</p>
'''))

S.append(('colisoes', 'Colisões e conservação do momento', f'''
<p>Quando duas coisas batem, cada uma empurra a outra durante um instante curtíssimo. Pela terceira lei, esses empurrões são iguais e opostos. O efeito total desse empurrão rápido se chama <b>impulso</b> ({i("J")}). Ele muda o momento de cada corpo:</p>
{eq(f'Δ{v("p")} = {v("J")} &nbsp;&nbsp;&nbsp;&nbsp; Δ{v("v")} = {fr(v("J"), i("m"))}', 16)}
<p>Como um corpo recebe +{i("J")} e o outro recebe −{i("J")}, o momento total não muda. Esta é uma das leis mais importantes da física, a <b>conservação do momento</b>:</p>
{eq(f'{i("m")}<sub>A</sub> {v("v")}<sub>A</sub> + {i("m")}<sub>B</sub> {v("v")}<sub>B</sub> = {i("m")}<sub>A</sub> {v("v")}′<sub>A</sub> + {i("m")}<sub>B</sub> {v("v")}′<sub>B</sub>', 17)}
<p>O apóstrofo (′) indica “depois da colisão”. Mas só essa lei não basta para saber o resultado: falta dizer se a batida é “elástica” como bola de borracha ou “mole” como massinha. Isso é o <b>coeficiente de restituição</b> {i("e")}, um número entre 0 e 1. Com {i("e")} = 1 nenhuma energia se perde; com {i("e")} = 0 os corpos grudam. Juntando tudo, o tamanho do impulso é:</p>
{eq(f'{i("J")} = {fr(f"−(1 + {i("e")}) · {i("v")}<sub>rel</sub>", f"{fr("1", i("m") + "<sub>A</sub>")} + {fr("1", i("m") + "<sub>B</sub>")}")}', 18)}
<p>onde {i("v")}<sub>rel</sub> é a velocidade com que um se aproxima do outro, medida ao longo da linha que liga os centros (a <b>normal</b> {v("n")}).</p>
{figure(7, fig7(), 'Colisão frontal entre um asteroide de 30 t e outro de 8 t, com e = 0,6. Os impulsos são iguais e opostos, e o momento total é o mesmo antes e depois.')}
<div class="box"><b>Exemplo resolvido (Figura 7).</b> {i("v")}<sub>rel</sub> = −0,10 − 0,30 = −0,40 m/s (estão se aproximando).<br>
{i("J")} = 1,6 × 0,40 ÷ (1/30 000 + 1/8 000) ≈ <b>4 042 N·s</b>.<br>
A: 0,30 − 4 042/30 000 ≈ <b>0,165 m/s</b>. B: −0,10 + 4 042/8 000 ≈ <b>0,405 m/s</b>.<br>
Energia de movimento antes: ½·30 000·0,30² + ½·8 000·0,10² = 1 390 J. Depois: ≈ 1 067 J. Os 323 J que “sumiram” viraram calor, som e rachaduras na rocha. O momento se conserva sempre; a energia de movimento, só se {i("e")} = 1.</div>
<p>A massa de cada asteroide vem do seu volume e da densidade da rocha ({i("ρ")} = 2 000 kg/m³, típica de rochas porosas):</p>
{eq(f'{i("m")} = {i("ρ")} · {fr("4", "3")} π {i("r")}<sup>3</sup>', 19)}
<p>Como o raio está ao cubo, dobrar o tamanho multiplica a massa por 8. Uma rocha de raio 0,7 m tem cerca de 2,9 t; uma de raio 2,1 m chega a 78 t. Por isso as pequenas são jogadas longe e as grandes quase não desviam.</p>
<div class="box"><b>No jogo.</b> Os asteroides só mudam de rumo quando colidem: com outro asteroide, com o módulo ou com a estação. Fora isso, seguem em linha reta, e a linha fina que sai de cada um mostra para onde vão nos próximos 20 s. Usamos {i("e")} = 0,6 entre rochas e {i("e")} = 0,35 entre rocha e módulo.</div>
'''))

S.append(('giro', 'Choques fora do centro fazem girar', f'''
<p>Se o impulso não passa pelo centro de massa, ele também produz torque, e o corpo começa a girar. É o que acontece quando um asteroide raspa o nariz do módulo.</p>
{figure(8, fig8(), 'À esquerda, o impulso J age no ponto P, longe do centro de massa: o módulo ganha velocidade Δv e rotação Δω. À direita, o impulso passa pelo centro: só empurra.')}
<p>Chamando de {v("r")} a seta que vai do centro de massa até o ponto de contato P, a variação de rotação é:</p>
{eq(f'Δω = {fr(f"({v("r")} × {v("n")}) · {i("J")}", i("I"))}', 20)}
<p>O símbolo × é o <b>produto vetorial</b>. Em duas dimensões ele é simples: {i("r")}<sub>x</sub>·{i("n")}<sub>y</sub> − {i("r")}<sub>y</sub>·{i("n")}<sub>x</sub>. Ele vale zero quando {v("r")} e {v("n")} estão na mesma linha (choque centralizado) e é máximo quando são perpendiculares. Na prática, ele faz o papel do braço {i("d")} da equação (8).</p>
<p>Um detalhe importante: um ponto na ponta de um corpo que gira se move mais rápido que o centro. Por isso, a velocidade usada na colisão é a do ponto de contato:</p>
{eq(f'{v("v")}<sub>P</sub> = {v("v")} + ω × {v("r")}', 21)}
<p>Juntando as equações (18), (20) e (21), o impulso entre o módulo e uma rocha é:</p>
{eq(f'{i("J")} = {fr(f"−(1 + {i("e")}) · {i("v")}<sub>rel</sub>", f"{fr("1", i("M"))} + {fr("1", i("m"))} + {fr(f"({v("r")} × {v("n")})<sup>2</sup>", i("I"))}")}', 22)}
<div class="box"><b>Teste feito no jogo.</b> Simulamos uma rocha de 41 t batendo de raspão no módulo de 9 t. O momento linear total ficou exatamente igual antes e depois. O momento angular variou só 0,02%, por causa de um pequeno ajuste de posição que impede os dois corpos de ficarem um dentro do outro. A estação, com cerca de 420 t, é tratada como fixa: num choque, o movimento dela é desprezível.</div>
'''))

S.append(('acoplamento', 'Acoplamento: por que tão devagar?', f'''
<p>O acoplamento só é aceito se cinco condições valerem ao mesmo tempo. A razão principal é a <b>energia cinética</b>, a energia do movimento:</p>
{eq(f'{i("E")}<sub>c</sub> = {fr("1", "2")} {i("m")} · {i("v")}<sup>2</sup>', 23)}
<p>A velocidade está ao quadrado. Triplicar a velocidade multiplica a energia por 9. Para o módulo de 9 t:</p>
<div class="box">A 0,25 m/s: {i("E")}<sub>c</sub> = ½ × 9 000 × 0,25² ≈ <b>281 J</b>, parecido com soltar um saco de cimento de 50 kg de 57 cm de altura.<br>
A 0,8 m/s: {i("E")}<sub>c</sub> = ½ × 9 000 × 0,8² = <b>2 880 J</b>, como soltar o mesmo saco de quase 6 m de altura. Os mecanismos de acoplamento não aguentam isso.</div>
{figure(9, fig9(), 'Os cinco critérios do jogo. A sonda no nariz do módulo precisa tocar o porto dentro da faixa laranja, devagar, reto e sem girar.')}
<p>Na vida real os limites são ainda mais apertados. Veja a comparação com o Padrão Internacional de Acoplamento (IDSS), usado nos portos novos da ISS:</p>
<div class="tbl"><table>
<thead><tr><th>Critério</th><th>No jogo</th><th>Na vida real (IDSS)</th></tr></thead>
<tbody>
<tr><td>Velocidade de aproximação</td><td>até 0,25 m/s</td><td>0,05 a 0,10 m/s</td></tr>
<tr><td>Velocidade lateral</td><td>até 0,10 m/s</td><td>até 0,04 m/s</td></tr>
<tr><td>Desalinhamento lateral</td><td>até 0,25 m</td><td>até 0,10 m</td></tr>
<tr><td>Ângulo (atitude)</td><td>até 4°</td><td>até 4°</td></tr>
<tr><td>Rotação</td><td>até 2 °/s</td><td>até 0,20 °/s</td></tr>
</tbody></table></div>
<p class="src">Fonte dos valores reais: NASA, <i>International Docking System Standard (IDSS) Interface Definition Document</i>, Revisão F (2022), Tabela 3.3.1.1-2, “Initial Contact Conditions”.</p>
'''))

S.append(('gravidade', 'E a gravidade? Tudo cai junto', f'''
<p>A ISS está a cerca de 400 km de altura. Lá, a gravidade ainda é forte: usando a lei da gravitação de Newton, ela vale cerca de 89% da gravidade na superfície.</p>
{eq(f'{i("g")}<sub>400 km</sub> = {i("g")}<sub>0</sub> · ({fr(i("R") + "<sub>T</sub>", i("R") + "<sub>T</sub> + " + i("h"))})<sup>2</sup> = 9,81 · ({fr("6 371", "6 771")})<sup>2</sup> ≈ 8,7 m/s²', 24)}
<p>Então por que os astronautas flutuam? Porque a estação está <b>caindo</b> o tempo todo. Ela anda tão rápido para o lado (cerca de 28 000 km/h, segundo a NASA) que, enquanto cai, a superfície curva da Terra “foge” embaixo dela. Ela cai em volta da Terra, sem nunca chegar ao chão, e completa uma volta a cada 90 minutos mais ou menos. Isso é estar em <b>órbita</b>.</p>
{figure(10, fig10(), 'O módulo e a ISS estão na mesma órbita, com quase a mesma velocidade e a mesma queda. No jogo vemos só o movimento de um em relação ao outro, que é pequeno e lento.')}
<p>O módulo também está em órbita, colado na estação. Os dois caem juntos, com a mesma aceleração. Por isso, olhando de dentro da estação, é como se não houvesse gravidade: só aparece o movimento de um em relação ao outro. É esse movimento relativo que o jogo mostra.</p>
<div class="box"><b>A simplificação do jogo.</b> Isso não é perfeito. Pequenas diferenças de altura e um efeito parecido com o de Coriolis fazem objetos próximos em órbita derivarem devagar uns em relação aos outros. Para o módulo a 0,25 m/s, essas acelerações ficam perto de 0,0006 m/s², umas 700 vezes menores que a dos jatos do jogo. Mas, em dois minutos, poderiam desviar o módulo uns 4 m. Na vida real, os computadores de bordo compensam isso. No jogo, deixamos de fora para ficar mais simples de entender e de jogar.</div>
'''))

S.append(('numeros', 'Os números do jogo', f'''
<p>Todos os valores usados na simulação, para você conferir as contas:</p>
<div class="tbl"><table>
<thead><tr><th>Grandeza</th><th>Valor</th><th>De onde vem</th></tr></thead>
<tbody>
<tr><td>Massa do módulo {i("M")}</td><td>9 000 kg</td><td>escolhido</td></tr>
<tr><td>Momento de inércia {i("I")}</td><td>≈ 16 150 kg·m²</td><td>equação (9)</td></tr>
<tr><td>Aceleração de cada jato</td><td>0,42 m/s²</td><td>escolhido</td></tr>
<tr><td>Força de cada jato</td><td>≈ 3 780 N</td><td>equação (5)</td></tr>
<tr><td>Aceleração angular</td><td>10 °/s²</td><td>escolhido</td></tr>
<tr><td>Torque de rotação</td><td>≈ 2 820 N·m</td><td>equação (10)</td></tr>
<tr><td>Passo de tempo Δ{i("t")}</td><td>1/120 s</td><td>seção 6</td></tr>
<tr><td>Densidade dos asteroides</td><td>2 000 kg/m³</td><td>rocha porosa</td></tr>
<tr><td>Massa dos asteroides</td><td>2,9 a 78 t</td><td>equação (19)</td></tr>
<tr><td>Restituição rocha-rocha</td><td>0,6</td><td>escolhido</td></tr>
<tr><td>Restituição rocha-módulo</td><td>0,35</td><td>escolhido</td></tr>
<tr><td>Restituição módulo-estação</td><td>0,3</td><td>escolhido</td></tr>
<tr><td>Batida que destrói (estação)</td><td>0,8 m/s</td><td>escolhido</td></tr>
<tr><td>Batida que destrói (asteroide)</td><td>0,6 m/s</td><td>escolhido</td></tr>
</tbody></table></div>
<div class="box"><b>Para ir além: por que o combustível acaba?</b> Cada jato joga massa fora. Quanto de velocidade uma nave consegue ganhar no total depende de quanto gás ela carrega e da velocidade com que ele sai. Essa é a <b>equação do foguete</b>, de Konstantin Tsiolkovsky:
<div class="eq"><div class="eq-m">Δ{i("v")} = {i("v")}<sub>e</sub> · ln {fr(i("m") + "<sub>inicial</sub>", i("m") + "<sub>final</sub>")}</div><span class="eq-n">(25)</span></div>
Gás frio, como nitrogênio, sai a cerca de 700 m/s, bem mais devagar que o escape de um motor de foguete. Por isso cada toque nos jatos custa caro, e pilotar com economia faz parte do desafio.</div>
'''))

def build():
    nav = ''.join(f'<button class="chip" data-target="phy-{sid}">{k+1}. {title}</button>' for k, (sid, title, _) in enumerate(S))
    secs = ''.join(f'<section class="phy-sec" id="phy-{sid}"><h3><span class="secn">{k+1}</span>{title}</h3>{body}</section>' for k, (sid, title, body) in enumerate(S))
    return f'''
  <section id="physics" hidden role="dialog" aria-modal="true" aria-labelledby="phyTitle">
    {DEFS}
    <header class="phy-head">
      <div><p class="eyebrow">Manual do piloto</p><h2 id="phyTitle">A física por trás do jogo</h2></div>
      <button class="btn" id="phyClose"><kbd>Esc</kbd>Voltar ao jogo</button>
    </header>
    <nav class="phy-nav" aria-label="Seções">{nav}</nav>
    <div class="phy-scroll" id="phyScroll">
      <article class="phy-article">
        <p class="lead">Encaixar um módulo numa estação espacial parece fácil até você tentar. Aqui está toda a física que o jogo calcula, passo a passo. Você só precisa de um pouco de álgebra e trigonometria do ensino médio.</p>
        {secs}
        <p class="end">Pronto para tentar de novo? <button class="cta" id="phyBack">Voltar ao jogo</button></p>
      </article>
    </div>
  </section>
'''

if __name__ == '__main__':
    open('physics.html', 'w').write(build())
    print(len(build()))
