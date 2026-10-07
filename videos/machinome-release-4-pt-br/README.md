# Machinome — corte 4, português brasileiro

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

[Assistir localmente](http://127.0.0.1:8785/) · [MP4](_build/rehearsal.mp4) ·
[Narração original](_build/raw-narration.wav) · [Fonte](movie.py) ·
[Texto](narration.py) · [Descrição](description.md).

Versão brasileira independente do candidato a lançamento 4, com Raquel,
voz nativa pt-BR. A relação entre roda e eixo é lida em inglês e traduzida
imediatamente. Os identificadores Python permanecem reais; os destaques
acompanham as duas leituras. Importação e testing_steps também recebem
explicações em português. A pergunta final enfatiza VOCÊ.

As decisões visuais e as oito tecnologias CAD do inglês são preservadas,
incluindo a corrente com React e Manifold, a roda acelerando em fase,
a marca laranja, o texto final ampliado e a URL do framework.
[Direção](DIRECTION.md) e [verificação](VERIFICATION.md) registram as
escolhas e os limites. Nada publicado.

Estado atual: produção automática cancelada pelo piloto em 7 de outubro
de 2026. Ele fará a narração portuguesa pessoalmente. A voz gerada foi
rejeitada por ritmo rápido, pouca emoção e falta de pausas entre frases.
A renderização foi interrompida; não há master português aprovado, e o
servidor de revisão está fechado. Fontes, tomadas e cache foram preservados.
Não gerar voz nem reiniciar a captura sem uma nova instrução do piloto.
Os comandos abaixo são registro de reprodução, não uma fila de trabalho.
O corte 4 em inglês permanece inalterado.

## Reproduzir

A partir da raiz do repositório Leonardo, com o ambiente existente:

```sh
node videos/machinome-release-4-pt-br/prepare.mjs
node videos/machinome-release-4-pt-br/speech-test.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-4-pt-br/narration.py
node videos/machinome-release-4-pt-br/speech.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-4-pt-br/audio-evidence.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-4-pt-br/movie.py
node videos/machinome-release-4-pt-br/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/machinome-release-4-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/machinome-release-4-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 1280
node videos/machinome-release-4-pt-br/inspect.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-4-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/machinome-release-4-pt-br/postflight.mjs
python videos/machinome-revolutions-v2/serve-review.py --port 8785 --directory videos/machinome-release-4-pt-br
```

O servidor fica em primeiro plano. Em outro terminal:
`node videos/machinome-release-4-pt-br/check-player.mjs /home/asa/devel/machinome/videomaker`.
Executar os comandos em sequência. `finish.mjs` sempre segue uma nova
avaliação de `movie.py`, nunca outra execução de si mesmo.

A voz deve estar disponível na conta configurada. O identificador fica
em `narration.py`; a chave permanece apenas no ambiente privado do
Videomaker. A geração inicial usa `speech.mjs <videomaker> --generate`.
Sem essa opção, somente o cache é usado. Não há retentativa paga automática,
emendas, alteração de velocidade ou pausas inseridas.

O áudio é colocado em +3 segundos; todo o corte segue seu alinhamento.
Reutilizamos a exportação, desenho e marcas do corte 3, o logotipo Python
do corte 2 e fontes/dicionário do corte 1. Capturas têm cache próprio.
Não se reexporta CAD nem se sobrescrevem os cortes anteriores.
A exportação registra a revisão `94a8562cc70e96de0cad1b85a4a7c1e092d2ed5c`
e seu estado modificado real. Fontes mecânicos e testes não mudaram.
Se essa exportação local faltar, criar outra explicitamente, sem
sobrescrever a evidência do corte 3.

A URL do framework não substitui as URLs pendentes da galeria.
A descrição preserva as ressalvas de distribuição e o registro de
produção. Pronúncia, naturalidade e mixagem ainda precisam de escuta humana.
