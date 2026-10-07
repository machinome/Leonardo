# Audições — evidência técnica, não aprovação de interpretação

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

7 de outubro de 2026. Três gravações da abertura, cada uma em uma única
solicitação Eleven v3. O texto falado corresponde exatamente a OPENING
de narration.py: 411 caracteres, 70 palavras, terminando antes das peças.
Nada foi gerado para o restante do roteiro ou capturado em vídeo.

| Opção | Voz | Duração | Palavras/min, incluindo pausas | Pausas ≥0,5 s |
| --- | --- | ---: | ---: | ---: |
| A | Leo Antonio | 31,12 s | 135 | 7 |
| B | Sávio | 30,64 s | 137 | 8 |
| C | Carla | 39,60 s | 106 | 7 |

Pausas medidas abaixo de −42 dBFS. O áudio original não sofreu emendas,
mudança de velocidade ou inserção de silêncio. Os MP3 de comparação têm
somente normalização de volume e codificação. WAVs, respostas brutas,
alinhamentos, hashes e relatórios permanecem em ../_build/auditions-1.

SHA-256 dos WAVs:

- Leo: `0f4487297d4d61c538c1b34200858257acd0750974b4d6c5a58bb78d2da4b823`
- Sávio: `a11fce3cd7dd7e18ce303be8448c4177006629baa27c63308b0ab5a41d3c1d8a`
- Carla: `eef7f0567743d0edd5a92d9843c7ac070bfbabbffaa35b2d3f5e70cdd504378b`

O provedor marca o ponto final 54–56 ms além do PCM, mas todos os últimos
caracteres falados terminam dentro do áudio. A validação distingue a
pontuação do conteúdo falado; nenhum tempo foi corrigido ou áudio esticado.
As respostas de Sávio e Carla foram recuperadas do recibo já salvo após
essa distinção, sem nova compra. Andrea não estava compartilhável e não
gerou áudio; Leo substituiu a opção A.

check.mjs passou: três áudios com duração válida, reprodução e busca,
reprodução exclusiva, HTTP 206, links e downloads, desktop e largura
390 px sem overflow ou erros. As duas capturas do reprodutor foram
inspecionadas. Não há elemento de vídeo nessa página.

Ritmo medido não certifica emoção, naturalidade ou gosto. As direções
vocais são hipóteses para o piloto ouvir. A escolha da voz e a aprovação
da futura narração completa estão pendentes; o render continua parado.
