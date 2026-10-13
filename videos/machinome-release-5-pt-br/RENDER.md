# Render pt-BR — 13 de outubro de 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Pedido: renderizar usando exatamente a proposta 7 aprovada, com a conversa
do Studio em português. Nenhuma nova síntese de voz.

## Fontes e sincronização

delivery.json continua sendo a fonte aprovada. narration.py o importa;
movie.py usa âncoras portuguesas, mantendo os trechos de código em inglês.
Atualizado o import do módulo de filme para o machinome_movie instalado.
CrankStroke e ThisScene mostram as próprias declarações do filme, com
seus textos portugueses. Os destaques continuam ligados às palavras.

Raw WAV aprovado: 203,280s, SHA-256
d2dc2542d7a15e0fdb83451e002dea8a2c8dbbf4d6b71564d68086bcc23e2b2d.
Mantido no cache original e em _build/approved. O mix padrão do Videomaker
normaliza o nível e acrescenta três segundos de entrada e a saída;
nada de efeitos, cortes, alongamento ou regeneração da voz.
Tempos do provedor preservados, inclusive a imprecisão terminal de 0,167s;
a última fala está completa, como a checagem independente já documentou.

A sequência tem 75 planos (incluindo poses de um quadro para o scrub),
208,958333s, 1920×1080 e 24 fps. O export é a cópia do recuperado no corte
inglês, com sua procedência original, sem recalcular geometria.

## Studio

Recaptura real de uma janela Firefox 153 em display isolado, 3840×2160.
A resposta demonstrativa do agente e o rótulo Construtor estão em
português. O prompt digitado é “Há mais um ajuste:”. A captura confirmou
zero mutações e zero erros: não abriu sessão nem enviou mensagem.
O modelo real é composto em movimento no espaço da captura.
Os menus do aplicativo e os identificadores do modelo não foram
falsamente apresentados como uma tradução do produto.

## Ajuste visual medido

O primeiro teste encontrou sobreposição dos nomes no fluxo de tecnologias:
a fala portuguesa deixa uma janela menor que a inglesa. Preservados
14 quadros de leitura estacionária por nome e a curva descendente.
A saída acelerada passa de 0,5 para 0,25s; handoff ajustado para manter
1,25s de giro gráfico antes da roda física. A aceleração da roda passa
a 56 graus/s² para preservar o fechamento rápido no novo tempo.
Áudio e duração da fala inalterados.

## Verificação e entrega

Studio: 13 amostras de entrada/layout; interação: 23 amostras, giro curto,
scrub até zero, saída rápida, movimento do modelo e digitação; relação:
8 amostras de destaque, com os tempos desta tomada e não do inglês.
Captura do chat e quadros de código/Studio/tecnologias inspecionados.
Conferência geral e MP4: resultados finais registrados após o render.

Os registros herdados em HANDOFF.md e VERIFICATION.md são do inglês.
Mantidos o rótulo de fonte e a linha final de licença explicitamente
pedidos pelo piloto no corte de origem, conforme HANDOFF.md; a divergência
da linha de licença com o AGPL-3.0-only da galeria continua declarada em
description.md, não resolvida por este render. Nenhuma publicação.
