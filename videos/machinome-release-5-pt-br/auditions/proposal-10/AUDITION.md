# Python Brasil — experiência de leitura, tomada 10

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

O piloto aprovou a versão em 02d52e5 e pediu mais calma nas cenas de
código e especialmente no estúdio, preferindo nova interpretação de
Jessica. Pediu cinco segundos de leitura silenciosa em cada cena de código,
sem parar as animações. Não preencher o limite de cinco minutos: reservar
tempo para a introdução ao vivo.

Uma nova interpretação contínua, texto falado idêntico, Jessica / eleven_v3,
stability 0.0 e similarity_boost 0.75. Os tags em directedText chegam ao
provedor; emotion e direction são registros editoriais. Nenhuma emenda
entre interpretações, alteração de velocidade ou mudança de tom digital.
Take 9 não foi selecionado porque o estúdio não ganhou tempo suficiente.

Take 10 original: 208,400s, WAV PCM 24 kHz mono 16 bits, SHA-256
00f9c89751843f4b9f43b6568dd0dc838970c5749a5245f7fd040f175f8fdf1a.
O provedor colocou o fim do alinhamento em 208,698s. verify-ending.py
transcreveu o encerramento com faster-whisper/base local, sem fornecer
o roteiro, e confirmou “O que você quer construir?” completa. Isso não
valida emoção, pronúncia de todos os termos ou alinhamento fonético fino.

reading-pauses.mjs preserva todos os bytes falados, registra as inserções
e desloca alinhamento/legendas. Garante no mínimo cinco segundos após as
falas de face-reveal, testing, behind-the-film e mirror, com margem de
um quadro para arredondamento. Preserva a contemplação de três segundos
após ancestrais e dá pelo menos 1,3s entre as quatro ações do estúdio.
Acrescenta 0,348s no final para acomodar os timestamps terminais tardios,
sem cortar ou alterar o encerramento verificado.

Derivado: 231,309208s; SHA-256
ed8acceb3c75c27c95f8e8d487241343973fb40f2235f873af130e551647236e.
Filme ao vivo: 236,750s (3min56,75s), sobrando 63,250s em cinco minutos.
Estúdio, da primeira à última palavra: 19,642s, contra 15,232s na tomada 8.
As treze amostras do teste continuam até o último quadro de sua cena.

Revisão subjetiva da interpretação aguarda o piloto no viewer completo
http://127.0.0.1:8790/#movie. Nenhum MP4 novo foi renderizado.
Original da tomada 8 e prévia aprovada preservados; backup do documento,
mix e legendas em _build/approved-before-reading-pauses.
