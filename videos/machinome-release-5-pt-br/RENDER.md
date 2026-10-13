# Render pt-BR — 13 de outubro de 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Correção posterior: retirar o título não solicitado

Removidos “Serraria hidráulica” e “LEONARDO DA VINCI” do plano ancestor,
sem outra mudança editorial. A remoção fica em finish.mjs para preservar
o arquivo movie.py mostrado no próprio filme e o cache desses planos.
Comparação estrutural do documento antes/depois: apenas a declaração,
o posicionamento e a animação desse título foram retirados; todo o resto
é idêntico. Fonte da correção: commit 6ffb665ff491.

Render incremental: somente ancestor recapturado, 622 quadros; os demais
4.393 quadros foram reutilizados nas mesmas gerações do cache. Mantidos
5.015 quadros, 1920×1080, 24 fps e 208,958333s. A trilha AAC anterior e
a nova têm o mesmo hash de conteúdo:
bf4d2cf4319c29da77636bbb68be8fb4e168c8e36e08a885b53dab62380dd394.

Novo MP4: 27.839.492 bytes; SHA-256 conferido contra o manifesto:
e7d91497f71ba1ef1fc78a0f592ca0afe8c2ccfbce1a48b89c1a43292add7604.
Inspecionados a folha overview-000 e o quadro 318 decodificados do MP4:
título ausente, máquina e enquadramento preservados. Pacote de revisão:
_build/review-packs/4e3b61fc4bc7-e7d91497f71b-e4a28278-09e2-4d6b-8de0-22e30e9a93ca/.
Player atualizado no mesmo endereço. O registro abaixo descreve o render
anterior; a correção acima é a entrega atual.

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
Conferência geral: 118 amostras/âncoras passaram antes do render.

Render concluído a partir do commit 7719337130c5, sem nova síntese.
MP4 H.264, 1920×1080, 24 fps, 5.015 quadros, 208,958333s;
AAC estéreo a 48 kHz; 27.934.643 bytes. SHA-256 conferido contra o manifesto:
11b7e2fe46144b4e56e9746cbb6de98d90ba690f0ddf518aef72da9fd9236680.
O manifesto de áudio confirma uma única tomada com o hash aprovado acima.

Inspecionadas as quatro folhas de visão geral extraídas do MP4 e os
quadros completos 2756 (conversa portuguesa), 3657 (código da cena) e
4982 (encerramento). Pacote automático íntegro em
_build/review-packs/5730c0791413-11b7e2fe4614-1830a0a4-4a36-4815-80da-6603c10bb64e/.
Isso é inspeção visual amostrada, não nova revisão auditiva da interpretação:
a tomada é a mesma já aprovada pelo piloto.

Player em http://127.0.0.1:8786/film/; testados no Chromium os metadados,
reprodução, pausa e salto para 115s. O servidor simples anterior não
suportava avanço: serve-listening.py acrescenta byte ranges, mantendo as
audições no mesmo endereço. A prévia interativa voltou na porta 8790.
Não houve envio de mensagem ao agente nem publicação externa.

Os registros herdados em HANDOFF.md e VERIFICATION.md são do inglês.
Mantidos o rótulo de fonte e a linha final de licença explicitamente
pedidos pelo piloto no corte de origem, conforme HANDOFF.md; a divergência
da linha de licença com o AGPL-3.0-only da galeria continua declarada em
description.md, não resolvida por este render. Nenhuma publicação.
