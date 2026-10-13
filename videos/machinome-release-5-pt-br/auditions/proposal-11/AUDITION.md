# Python Brasil — tomada 11, pausas de três segundos

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Nova interpretação contínua solicitada após o piloto ouvir interrupções
em “momentos” e “E aqui está”. Jessica / eleven_v3, mesmas configurações.
Retirado o tag de pausa entre ângulos e momentos. Nenhuma edição no
interior do estúdio. Texto de encerramento: “Eu sou Machinome!”, seguido
por contemplação, propósito, contemplação e pergunta sem ênfase em você.

Original de 202,960s, SHA-256
a08d4ec2b68e33ff6b201f9e6078d1de2cbd02ce95dffd7043430f33190bbc54.
verify-ending.py confirmou a pergunta final completa por ASR local,
sem roteiro; verify-pauses.py manteve a transcrição independente completa.
Esses testes não avaliam emoção e os tempos ASR são aproximados.

Correção do editor: um cruzamento por zero não prova silêncio e pode
estar dentro de uma sílaba. A versão anterior se apoiava nisso e no
alinhamento do provedor. Nesta tomada o alinhamento também deriva:
a pausa acústica anterior a “E aqui” é 160,697–161,446s, enquanto o
provedor dizia 161,197–161,670s. A inserção agora fica em 161,071s,
antes do início independente de “E” (ASR: 161,300s), nunca em “aqui”.
Todas as inserções exigem pelo menos 120ms de silêncio contínuo abaixo
de -45dBFS. Timestamps são calibrados para essas fronteiras; os bytes
da voz não são esticados, apagados, trocados ou acelerados.

Quatro pausas de código: 3s; ancestralidade: 3s; após identidade: 1,5s;
após propósito: 2s. Uma margem de um quadro evita encurtar a pausa ao
arredondar a montagem. O teste continua amostrando durante o silêncio.
Derivado: 216,838750s, SHA-256
f41ec22469fc6ede1a90189c22696a2d95ee32d0fa946f24405c094c988ed1b1.
Filme no viewer: 222,125s; restam 77,875s na lightning talk de cinco minutos.

Escuta subjetiva aguarda o piloto em http://127.0.0.1:8790/#movie.
Mesma interface e porta. Nenhum MP4 novo. Tomadas e experimentos anteriores
preservados; backup da prévia 10 em _build/previous-take-10.
