# Versão brasileira — evidências de produção

Data: 7 de outubro de 2026. Produção cancelada pelo piloto.

A renderização foi interrompida por SIGINT (saída 130), após o último
progresso de 1.351/4.308 quadros. Não há MP4 final verificado ou narração
aprovada. O piloto rejeitou o ritmo e a expressividade da voz e decidiu
narrar pessoalmente. Servidor português fechado; fontes e caches mantidos.
Os resultados técnicos abaixo não constituem aprovação da performance.

## Voz e gravação

Raquel — Expressive and Energetic, identificada como pt-BR na biblioteca
ElevenLabs — foi adicionada à conta após a liberação de voices_write.
O identificador retornado é `GDzHdQOi6jjf8zaXhCYD`; metadados públicos em
`voice.json`. Nenhuma credencial está nos fontes ou artefatos de revisão.

Foram feitas duas gravações completas de 2.508 caracteres. A primeira
durou 172,40 segundos, mas sua pausa final de 0,373 segundo não atendia à
direção. Ela continua no cache, sem ser usada no corte. A segunda usa
`[long pause]` na solicitação e tem 174,16 segundos. Não há emendas,
silêncio inserido ou mudança de velocidade. SHA-256 do WAV escolhido:
`a7fd0c7960e9abd1078930522f75d28a212ee411b80633a42414251320ed831e`.

O sinal mede uma pausa de 2,411 segundos abaixo de −42 dBFS, entre
159,95075 e 162,36196 segundos do áudio. A análise decodifica até as
primeiras palavras seguintes: o alinhamento pode começar uma vogal dentro
do silêncio precedente. A pausa não é medida apenas pelo texto.
O áudio inteiro decodifica: média −17,1 dBFS, pico −0,1 dBFS.

A instrução de pausa é omitida somente das tabelas de alinhamento e
legendas. Todos os tempos das palavras permanecem os do provedor, e a
resposta bruta é preservada. `speech-test.mjs` verifica Unicode, tempos,
ausência de mutação da entrada e preservação de instruções desconhecidas.
Uma execução posterior de `speech.mjs` confirmou a reutilização sem
nova solicitação. Os dois recibos e gravações continuam no cache.

## Temporização e fontes

A tomada escolhida fornece 68 legendas e 35 âncoras de navegação.
“The waterwheel drives the crankshaft” ocupa 87,224–89,364 segundos;
“Em português” começa em 89,631. O filme coloca toda a gravação em +3 s.
Tem duração de 179,5 segundos, 4.308 quadros a 24 fps e 2,34 segundos de
cauda após o WAV completo. A pergunta final começa em 175,06 segundos do
filme; VOCÊ em maiúsculas dirige a ênfase, sem atestar aprovação auditiva.

Os 17 planos compilam. A verificação nativa de documento, fontes fixadas,
layout e âncoras passa. Sete destaques acompanham a relação bilíngue.
As linhas vazias reais 25 e 604 são preservadas no código dos testes.
Há oito tecnologias CAD, sete ferramentas na corrente e cartão final
localizado com a URL completa. A primeira chegada da corrente ocorre
3,635 segundos depois de seu início, com aceleração; o último nome toca
a roda 0,12 segundo após começar a passagem para a roda física.

Os fontes mecânicos não mudam. A revisão anterior de 43 testes B-rep
permanece como evidência, sem repetição para esta tradução editorial.
Exportação, desenho, marcas, logotipo Python, fontes e dicionário são
reutilizados. O inglês terminou antes de qualquer captura portuguesa.

## Captura e revisão

A prévia inicial passou com a primeira gravação. A inspeção da gravação
escolhida passou em 69 amostras, com repetição pixel a pixel idêntica.
Verifica cada quadro para evitar destaques simultâneos indevidos e para
manter a mesma fase, com aceleração estritamente crescente, entre a roda
gráfica e a física durante os 1,25 segundos da passagem. Todos os sete
nomes possuem amostras de contato com a roda acima da linha azul.

Foram inspecionadas imagens em tamanho integral dos destaques ingleses
e portugueses, dos testes, do código do próprio filme, da dissolução das
rodas e do cartão final. A prévia nativa da gravação escolhida, o MP4 e o
reprodutor ainda serão registrados após conclusão. Não confundir a prévia
anterior com evidência da tomada final.

Os cortes 3 e 4 em inglês permanecem intactos. `releaseReady` continua
falso: endereços públicos da galeria e licença de distribuição de
Videomaker permanecem pendentes. Nada publicado. Verificações de sinal,
alinhamento e pixels não substituem escuta humana de pronúncia, entrega
e mixagem; não foi declarada aprovação auditiva.
