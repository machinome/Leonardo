# Revoluções — corte 5 em português brasileiro

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Segunda proposta de narração do filme inteiro, baseada na cópia do corte 5 de main
(e8e16a8) em 12 de outubro de 2026. Voz: Leo Antonio, Eleven v3.
Uma tomada contínua, sem efeitos sonoros, cortes, montagem de frases,
aceleração ou silêncio acrescentado. Os trechos de código são falados em
inglês, sem tradução intercalada; o restante é português brasileiro.

[Ouvir a segunda proposta](http://127.0.0.1:8786/proposal-2/) ·
[Comparar com a primeira](http://127.0.0.1:8786/proposal-1/) ·
[Direção e roteiro](delivery.json) · [Direção emocional](DIRECTION.md).

O áudio é uma proposta para escuta. O vídeo português ainda não foi
sincronizado: movie.py, narration.py e os finalizadores preservam a base
inglesa copiada. Não execute esses finalizadores para produzir a versão
portuguesa antes de adaptar suas âncoras à tomada aprovada. O registro da
origem está em SOURCE-README.md e SOURCE-DIRECTION.md.

A produção de áudio desta etapa é independente desses arquivos:

```sh
node videos/machinome-release-5-pt-br/audition.mjs /home/asa/devel/machinome/videomaker --check
node videos/machinome-release-5-pt-br/audition.mjs /home/asa/devel/machinome/videomaker --generate
```

Use --generate apenas para uma nova proposta autorizada. Sem essa opção,
o comando reaproveita a tomada existente. Um recibo bem-sucedido é guardado
antes de interpretar a resposta; não há repetição automática de chamadas.

delivery.json é a fonte do roteiro português e das indicações enviadas à
voz. Cada seção registra separadamente a intenção emocional. As etiquetas
entre colchetes orientam a geração e não fazem parte das legendas.
A duração é medida na gravação, sem limite herdado do corte inglês.

_build/narration.wav preserva integralmente a tomada; audition-2.mp3 é uma
cópia comprimida para escuta. O manifesto registra duração, hash, texto,
tempos das seções e a ausência de edição. Os recibos e gravações são locais
e ignorados pelo Git. A escuta do piloto decide a interpretação e a
pronúncia; alinhamento textual não comprova emoção nem fluência bilíngue.

O player de escuta é servido de _build/listening, na porta 8786. O corte
inglês permanece disponível separadamente na porta 8785.
