# Terceira proposta de áudio — 12 de outubro de 2026

Status posterior: aprovada pelo piloto (“está ok”). Preservada enquanto
se experimenta Jessica com exatamente o mesmo texto e direção.

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Revisão solicitada após a segunda proposta: singular em “e os humanos
constroem a sua”, mais pausa e contraste de entonação nas mudanças de cena
de código e Studio. Uma comparação automática do roteiro sem etiquetas
confirmou que esta é a única mudança de palavras. Voz e parâmetros iguais.
A segunda proposta está preservada em auditions/proposal-2 e no seu player.

Leo Antonio / Eleven v3, stability 0.0, similarity_boost 0.75.
Uma nova chamada contínua: 2.506 caracteres falados, 3.030 com direção.
Duração medida: 193,600 segundos. Sem efeitos, cortes, montagem de frases,
normalização, aceleração ou silêncio acrescentado. WAV mono PCM 24 kHz,
16 bits; cópia MP3 a 192 kbps para escuta.

SHA-256 do WAV:
cf6430525ed37fd0cfecb188bdecdce14f1fc931c4395eb67de149d434be4bbd

Intervalos segundo o alinhamento do provedor, não medição fonética:

| Transição | Proposta 2 | Proposta 3 |
| --- | ---: | ---: |
| Reconstrução → código | 0,608 s | 0,940 s |
| Código → Studio | 0,596 s | 1,112 s |
| Studio → testes | 0,790 s | 0,661 s |
| Testes → código do filme | 1,007 s | 1,230 s |

A pausa pedida não aumentou em todas as transições. Os controles são
generativos, não garantias. Não houve avaliação auditiva da entonação pelo
agente; a interpretação continua sujeita à escuta do piloto.

A marcação terminal do provedor ultrapassa o PCM em 0,141 segundo.
O recibo foi retido e não houve nova chamada: Whisper base local, sem
roteiro como prompt, confirmou o singular e a pergunta final completa.
Relatório: _build/ending-check.json. Os tempos originais são preservados,
a navegação é aproximada e as legendas desta tomada aguardam realinhamento.
As legendas anteriores foram movidas para _build/proposal-2/captions.srt
para não serem confundidas com as desta tomada.

Player: http://127.0.0.1:8786/proposal-3/
Comparação: http://127.0.0.1:8786/proposal-2/

O vídeo inglês permanece inalterado. Esta entrega é apenas áudio completo;
o vídeo português ainda não está sincronizado.
