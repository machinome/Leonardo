# Audições brasileiras — abertura

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Nova comissão do piloto: voltar à narração por máquina e comparar vozes
somente até antes da apresentação das peças. Não reabrir o render.
As tomadas completas anteriores foram rejeitadas por rapidez e pouca emoção.

Três vozes nativas pt-BR: Leo Antonio, Sávio e Carla. As descrições de caráter
em opening.json são direções de interpretação baseadas na biblioteca,
não certificações de qualidade por escuta. As três usam o mesmo texto,
terminando em “Vou mostrar como ela funciona.” Sem mecanismo, vídeo ou música.

Andrea foi considerada inicialmente, mas sua inclusão retornou
sharing_not_enabled. Nenhum áudio foi comprado com essa voz; Leo Antonio
substitui essa opção.

Solicitar uma leitura contemplativa, curiosa, com calor ao reconhecer a
ancestral e pausas entre frases. Eleven v3 recebe instruções de emoção,
ritmo lento e pausas; não um parâmetro speed, que sua documentação específica
declara indisponível nesse modelo. Não há alteração de velocidade posterior,
emendas ou silêncio inserido. WAV original e recibo bruto são conservados.
Os MP3 de comparação recebem somente normalização de volume e codificação.

Os arquivos ficam no cache separado ../_build/auditions-1. Nada substitui
a narração do filme. Uma chamada por voz; sem repetição paga automática.

## Aprovações obrigatórias

1. O piloto ouve as opções e escolhe voz e interpretação.
2. Só depois se prepara a narração completa para uma nova aprovação.
3. Nenhum vídeo é renderizado antes da aprovação explícita dessa narração.

## Reproduzir

Na raiz do Leonardo:

```sh
node videos/machinome-release-4-pt-br/auditions/generate.mjs --check
node videos/machinome-release-4-pt-br/auditions/generate.mjs --generate
```

Sem opção, generate.mjs usa somente os recibos existentes. --generate
autoriza somente as três audições de opening.json, não o filme inteiro.

O reprodutor usa o servidor local já existente, sem captura de vídeo:

```sh
python videos/machinome-revolutions-v2/serve-review.py --port 8785 --directory videos/machinome-release-4-pt-br
```

Abrir http://127.0.0.1:8785/auditions/.

Validação: `node videos/machinome-release-4-pt-br/auditions/check.mjs`.
Resultados em [VERIFICATION.md](VERIFICATION.md). Aprovação auditiva pendente.

Fontes de configuração consultadas:

- https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
- https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- ElevenLabs Voice Library API: pt, brazilian, metadados consultados em 7/10/2026.
