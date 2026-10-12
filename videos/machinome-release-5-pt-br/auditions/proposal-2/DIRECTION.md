# Direção de voz — segunda proposta pt-BR

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

A primeira proposta foi rejeitada pelo piloto por monotonia, transições
sem intenção audível e frases quebradas. As etiquetas foram enviadas, mas
o resultado não realizou a direção. A evidência anterior era técnica e
não comprovava a interpretação. A primeira proposta está preservada em
auditions/proposal-1 e seus arquivos locais em _build/proposal-1.

Nesta segunda proposta, Leo e Eleven v3 continuam. Stability passa de
0.5 para 0.0 para experimentar maior variação na entrega. Saem as repetidas
indicações de fala medida/lenta que concorriam com a emoção. Entram
curiosidade no convite à máquina, mudança de intenção no Studio, surpresa
e entusiasmo na revelação do filme e prazer explícito na autorreferência.
As etiquetas são aplicadas no ponto da mudança, não apenas no início
de um bloco longo. O ritmo deve continuar observável e sem pressa.

“Siga a corda para baixo e para o outro lado” perde as reticências internas.
“Uma roda, duas tarefas” permanece ligado por vírgula, com intenção de uma
única conclusão. A reconstrução passa à voz passiva. O inglês termina sua
ideia antes de “Você também pode criar modelos pelo navegador”.

Uma nova tomada completa é gerada. Nenhuma frase da primeira é enxertada.
Os controles continuam sendo sugestões ao modelo; esta direção não é
uma alegação de que a expressividade já foi ouvida e aprovada pelo agente.

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
| Código do próprio filme | Surpresa e entusiasmo audíveis na mudança de cena; prazer na revelação de “Olha que legal”. Identificadores permanecem em inglês. |
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
inglês. Esta segunda audição serve também para avaliar essa passagem
entre idiomas com a mesma voz.

Uma chamada para o roteiro inteiro, sem pickups, cortes, alongamento
digital ou inserção de silêncio. O filme será sincronizado depois da
escuta; o áudio não será apressado para caber no tempo do corte inglês.
