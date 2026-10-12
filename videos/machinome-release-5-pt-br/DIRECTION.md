# Direção de voz — primeira proposta pt-BR

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

A voz é Leo Antonio, já escolhido para os estudos brasileiros do projeto.
A base é calma, com dicção clara e ritmo espaçado. A continuidade pertence
à interpretação inteira: nenhuma frase em inglês recebe uma tradução
logo depois, e nenhuma troca de idioma é anunciada.

| Passagem | Emoção e entrega |
| --- | --- |
| Revoluções, na abertura | Inspiração serena; firmeza tranquila, espaço antes de apresentar a história. |
| Leonardo e ancestralidade | Admiração contida, com um pouco mais de calor em “minhas ancestrais”; sem tristeza ou solenidade excessiva. |
| Apresentação da máquina | Guia de museu paciente. Mostrar uma relação de cada vez e pausar para observar eixo, biela, linguetas e cordas. |
| Reconstrução e código | Explicação clara e segura. Ler o import completo e “The waterwheel spin drives the crankshaft” em inglês, no fluxo da mesma voz. |
| Studio e testes | Convite acolhedor e precisão paciente; ações e verificações com tempo para serem entendidas. |
| Código do próprio filme | Curiosidade tranquila; leve sorriso na descoberta. Identificadores permanecem em inglês. |
| Tecnologias abertas | Entusiasmo moderado; cada nome legível, voltando à contemplação na corrente de tecnologias. |
| Revoluções e convite final | Retomar a inspiração, afirmar o propósito com confiança e fazer um convite humano, sem gritar. |

Emoção, velocidade e pausas são dirigidas separadamente. delivery.json
contém as etiquetas efetivamente enviadas à ElevenLabs, além desta
intenção editorial. Não se usa um campo de direção que o provedor ignore.

A documentação da ElevenLabs confirma que v3 recebe indicações entre
colchetes e usa pontuação para ritmo; não usa pausas SSML:
https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech

As indicações são sugestões generativas, não duração ou emoção garantida.
Não se força um idioma único na requisição, para permitir os trechos em
inglês. Esta primeira audição serve também para avaliar essa passagem
entre idiomas com a mesma voz.

Uma chamada para o roteiro inteiro, sem pickups, cortes, alongamento
digital ou inserção de silêncio. O filme será sincronizado depois da
escuta; o áudio não será apressado para caber no tempo do corte inglês.
