# Acoplamento ISS

Jogo de navegador em 2.5D: pilote um módulo espacial com jatos de gás comprimido e acople na Estação Espacial Internacional. A física é newtoniana e sem atrito: cada impulso muda a velocidade, e o módulo continua derivando até um jato oposto anular o movimento. O mesmo vale para a rotação.

## Como jogar

Abra o `index.html` no navegador (Chrome, Edge, Firefox ou Safari). Não precisa de servidor nem de internet: a biblioteca 3D está na pasta `vendor/`. Sem internet, o HUD usa as fontes do sistema.

| Controle | Ação |
|---|---|
| `D` / `A` | jato pela direita / esquerda do módulo (empurra para o lado oposto) |
| `W` / `S` | jato por cima / por baixo |
| `Q` / `E` | par de jatos de rotação anti-horária / horária |
| Mouse ou toque | segurar em volta do módulo dispara o jato daquele lado |
| `T` | liga ou desliga os asteroides |
| `F` | abre o manual de física |
| `P` / `M` / `R` | pausa / som / reiniciar |

Os jatos são presos ao casco: "direita" é a direita do módulo, não da tela.

**Para acoplar**, a sonda do nariz precisa tocar o porto com os cinco critérios valendo ao mesmo tempo: aproximação até 0,25 m/s, velocidade lateral até 0,10 m/s, atitude dentro de ±4°, rotação até 2 °/s e alinhamento dentro de ±0,25 m.

## Física

- Integração de Euler semi-implícita com passo fixo de 1/120 s.
- Módulo de 9 000 kg com momento de inércia de cilindro (≈ 16 150 kg·m²).
- Asteroides opcionais em rotas aleatórias, com massa pela densidade de 2 000 kg/m³ (2,9 a 78 t). Colidem entre si, com o módulo e com a estação por impulso de corpo rígido, que conserva momento linear e angular.
- A câmera fica fixa no referencial da estação.

O botão **Anatomia do jogo** abre, em outra aba, um mapa interativo da estrutura do código: o HTML, o CSS e o JavaScript divididos em blocos pelo que fazem, com a explicação de como cada um faz e com quais outros conversa.

O botão **Física do jogo** abre um manual didático, escrito para estudantes do ensino médio, com 25 equações e 10 diagramas. Os limites reais de acoplamento citados vêm de: NASA, *International Docking System Standard (IDSS) Interface Definition Document*, Rev. F (2022), Tabela 3.3.1.1-2.

**Simplificações:** os jatos são mais fortes que jatos reais de gás frio, para o jogo não ficar lento; os efeitos de mecânica orbital entre objetos próximos são ignorados; e as rochas colidem como esferas sem atrito.

## Estrutura

```
index.html               jogo completo (HTML, CSS e JavaScript)
anatomia-acoplamento-iss.html  mapa de blocos interativo do código, aberto pelo botão "Anatomia do jogo"
vendor/three.min.js      three.js r128 (licença MIT, em vendor/three-LICENSE.txt)
tools/physics_manual.py  gerador do HTML do manual de física (equações e diagramas SVG)
```
