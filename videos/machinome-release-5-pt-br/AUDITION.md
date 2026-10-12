# Primeira proposta de áudio — 12 de outubro de 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Leo Antonio / Eleven v3. Duração medida: 194,960 segundos. Uma chamada
contínua, 2.514 caracteres falados e 3.024 caracteres incluindo direção.
Sem efeitos, cortes, montagem de frases, normalização, aceleração ou pausas
digitais acrescentadas. MP3 a 192 kbps para escuta; WAV PCM mono, 24 kHz,
16 bits, preservado como matriz.

SHA-256 do WAV:
0e7a0b455842b9fab8bef058579ff7477fe9c977c86a235a086cfa3f712390f6

O texto retorna integralmente no alinhamento do provedor, após remover
somente as indicações não faladas. Entretanto, a marcação final avança
0,144 segundo além do PCM e atribui duração zero a CONSTRUIR. A primeira
validação detectou isso e reteve o recibo sem fazer nova chamada.

A transcrição independente dos últimos 24,96 segundos, com Whisper base
local e sem o roteiro como prompt, confirmou a frase final completa:
“O que você quer construir?”. O áudio não foi cortado. O relatório está
em _build/ending-check.json, associado ao mesmo hash. Os tempos originais
do provedor estão preservados; a navegação é aproximada. Legendas e
sincronização do vídeo aguardam novo alinhamento da tomada aprovada.

O MP3 decodifica integralmente. A intenção emocional está em delivery.json
e DIRECTION.md; essas indicações foram efetivamente enviadas ao provedor.
As verificações técnicas não equivalem a uma avaliação auditiva de emoção,
ritmo ou pronúncia dos trechos em inglês. A proposta aguarda a escuta do piloto.

O vídeo inglês de main e seus arquivos de áudio permanecem inalterados.
Os arquivos visuais e finalizadores nesta pasta são a cópia desse corte,
ainda com âncoras inglesas. Esta entrega é a primeira audição, não um
vídeo português sincronizado.
