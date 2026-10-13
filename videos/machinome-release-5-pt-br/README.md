# Revoluções — release-5-pt-br

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Versão brasileira do corte 5, com a tomada 7 de Jessica aprovada pelo
piloto em 13 de outubro de 2026. O áudio original de 203,280 segundos
permanece no cache e em _build/approved, sem regeneração, cortes,
aceleração ou efeitos. O filme tem 1920×1080, 24 fps e cerca de 3min29s,
incluindo três segundos de entrada e a saída da imagem.

[Vídeo local](http://127.0.0.1:8786/film-sem-titulo/) ·
[Prévia interativa](http://127.0.0.1:8790/#movie) ·
[Áudio aprovado](http://127.0.0.1:8786/proposal-7/) ·
[Roteiro e direção](delivery.json) · [Registro de render](RENDER.md).

movie.py é a declaração portuguesa; narration.py lê o texto aprovado
de delivery.json. A interface do Studio foi recapturada com resposta
demonstrativa em português, e “Há mais um ajuste:” é digitado na conversa.
Nenhuma mensagem foi enviada e nenhuma sessão de agente foi criada.
Os identificadores do código-fonte permanecem em inglês. Textos
explicativos do filme e trechos de narração mostrados no código estão em
português. A versão inglesa e as audições anteriores permanecem intactas.

## Reproduzir usando somente o áudio aprovado

O export local _build/model é uma cópia byte a byte do export recuperado
do corte 5 inglês. O histórico dessa origem permanece em SOURCE-README.md.
Pare somente a prévia portuguesa antes de reevaluar e finalizar.
Na raiz deste repositório:

```sh
node videos/machinome-release-5-pt-br/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-5-pt-br/movie.py
node videos/machinome-release-5-pt-br/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-5-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

finish.mjs requer uma avaliação nova de movie.py; não é idempotente.
Reutiliza apenas o cache da tomada aprovada. O render também é cache-only.
O mix padrão do Videomaker acrescenta a entrada/saída e normaliza o nível;
isso não altera a velocidade nem a interpretação da gravação original.
Não execute audition.mjs --generate para renderizar: isso é uma nova
audição e exige pedido do piloto. speech.mjs é apenas uma verificação
do cache aprovado e não gera fala.

Prévia: o mesmo comando acima com live no lugar de render e --port 8790.
Player com reprodução e avanço: `python3 videos/machinome-release-5-pt-br/serve-listening.py`.
Ele serve _build/listening na porta 8786; film-sem-titulo/index.html é uma
cópia de watch.html, que aponta para revolucoes-pt-br-e7d91497f71b.mp4,
cópia do MP4 renderizado identificada pelo prefixo de seu SHA-256.
Conferência no navegador: inspect-preview.mjs, inspect-studio.mjs,
inspect-studio-interaction.mjs e inspect-relation-sync.mjs recebem o
checkout do Videomaker e http://127.0.0.1:8790 como argumentos.

As audições ficam em auditions/proposal-N e _build/listening/proposal-N.
A gravação aprovada tem SHA-256
d2dc2542d7a15e0fdb83451e002dea8a2c8dbbf4d6b71564d68086bcc23e2b2d.
As marcações do provedor são aproximadas; sua pontuação terminal passa
0,167s do PCM, com fechamento completo confirmado por transcrição local.
Nenhum tempo do recibo original foi alterado. O filme tem margem no final.

Nada foi publicado. description.md conserva a atribuição, a declaração
de uso de IA e as pendências de direitos e URLs do corte inglês.
