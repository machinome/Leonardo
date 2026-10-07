# Revoluções

A roda faz revoluções. Uma máquina encontra uma de suas ancestrais:
a reconstrução da serraria hidráulica de Leonardo da Vinci. Acompanhe
a roda, a manivela, a serra, a catraca e as cordas; depois, conheça o
código-fonte da reconstrução, dos testes de geometria e deste vídeo.

Simulação interativa: {{simulationUrl}}
Código da máquina e do vídeo: {{sourceUrl}}

## Reconstrução e limites

Este modelo educativo segue a interpretação de serra hidráulica do museu
de Milão, IGB-37 (1952–1953), e a pesquisa do projeto sobre o Codex
Atlanticus 1078r. Não é uma máquina renascentista sobrevivente nem uma
réplica certificada. Dimensões e elementos ocultos incluem escolhas
documentadas. O movimento é prescrito. Água, corte e abertura da madeira
são ilustrativos; forças, atrito, tensões, estabilidade do enrolamento
e remoção de material não são simulados. Alguns movimentos são
desacelerados para a explicação.

Referências históricas registradas pelo projeto:

- https://www.museoscienza.org/en/collections/objects/hydraulic-saw
- https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica
- https://www.leonardodigitale.com/en/browse/Codex-atlanticus/1078-r/

O desenho do Codex Atlanticus 1078r vem do Wikimedia Commons:
https://commons.wikimedia.org/wiki/File:000R-1078.jpg
O Commons atribui a imagem a Leonardo da Vinci e codex-atlanticus.it e
registra domínio público (PD-Art / PD-old). A imagem baixada não foi alterada.
A fotografia do museu não é exibida; o desenho continua na tela enquanto
a narração menciona fotos de museus como fontes de pesquisa.

A cena de testes mostra o teste real de folga da lâmina.
`@testing_steps(13, end=4)` verifica treze instantes dos primeiros quatro
segundos. A verificação de posições amostradas não prova folga contínua
nem segurança física.

## Créditos e uso de IA

Leonardo da Vinci Gallery. Copyright (C) 2026 Luis Henrique Cassis
Fagundes. CAD, código e documentação originais da galeria usam
AGPL-3.0-only; consulte LICENSE e NOTICE do repositório. A galeria registra
os modelos como produzidos por Astra a partir de comissões humanas.

A direção, a adaptação da narração, as declarações do filme e o palco
deste corte foram gerados por um agente de programação de IA a partir
do roteiro humano e das orientações posteriores. O narrador em primeira
pessoa é Machinome como personagem composto: ferramentas, framework,
fundição e agente de IA. As afirmações sobre reconstrução e pesquisa se
referem ao trabalho registrado pelo projeto, não a uma nova pesquisa
histórica realizada por uma pessoa falando no vídeo. A voz brasileira é
Raquel, do ElevenLabs, em uma gravação contínua.

A identidade Machinome usa o símbolo e a marca laranja aprovados de brand/v1,
sem alterações. Permissões sobre a arte e a marca são separadas da licença
do código da galeria. Space Grotesk e IBM Plex Mono mantêm seus avisos da
SIL Open Font License. As dependências conservam suas próprias licenças.

Os oito raios da roda representam OpenSCAD, SolidPython, CadQuery, Build123d,
FreeCAD, JSCAD, OCCT (caminho STEP) e Trimesh (caminho STL). O adaptador
nativo FreeCAD é um repositório separado, experimental e ainda não lançado.
Three.js, NumPy, SciPy, Manifold, FastAPI, React e OpenSpec formam a corrente
de ferramentas; seus nomes aparecem visualmente, sem enumeração falada.
A montagem não afirma que toda integração seja uma capacidade publicada
e estável. Código do framework: https://github.com/machinome/machinome/
A ferramenta de filmes em Python e algumas funções do viewer são
capacidades de desenvolvimento local, não promessas de pacotes publicados.

O logotipo Python, sem alterações, identifica a linguagem. É uma marca
da Python Software Foundation; a página oficial permite esse uso referencial
(https://www.python.org/community/logos/). Não há endosso implícito.

{{pictureCredits}}

## Antes da publicação

Substituir os endereços públicos pendentes somente após verificá-los.
Ouvir a narração e a mixagem finais. Confirmar a versão de lançamento
e as permissões de distribuição. A frase “tudo isso é código aberto”
expressa a comissão do vídeo, mas Videomaker ainda não registra uma
licença de distribuição escolhida; resolver essa questão antes de publicar
um filme que possa sugerir que toda a cadeia de produção é aberta.
O logotipo é uma marca, não uma concessão de licença de código aberto.
