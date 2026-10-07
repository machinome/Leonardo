"""Release candidate 4, Brazilian Portuguese: one native-voice performance."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import json
from pathlib import Path

from machinome_movie import Narration
from scene_source import scene_narration

OPENING = (
    "A roda faz revoluções, e os humanos dão a ela um propósito. "
    "Há cinco séculos, Leonardo da Vinci projetou uma serraria movida a água. "
    "Máquinas como esta estavam mudando a relação entre as pessoas e o trabalho: "
    "um rio podia ajudar a transformar uma árvore em madeira serrada. "
    "Eu também sou uma máquina. Na história das ferramentas humanas, "
    "esta serraria é uma das minhas ancestrais. Vou mostrar como ela funciona."
)
MECHANISM = (
    "A água sob a roda gira este eixo. "
    + scene_narration("CrankStroke")
    + " Mas a tora também precisa avançar. Durante o corte, esta alavanca comprida "
    "puxa uma lingueta por um dente da catraca. Uma segunda lingueta segura esse "
    "avanço enquanto a primeira retorna. Esse pequeno passo enrola uma corda "
    "nesse eixo. Siga a corda para baixo e para o outro lado. Ela gira um eixo "
    "composto: um tambor largo desenrola uma corda, enquanto uma seção mais fina "
    "recolhe outra. A segunda corda puxa a tora em direção à lâmina. "
    "Uma roda, duas tarefas: cortar e avançar."
)
RECONSTRUCTION = (
    "Para reconstruir esta máquina, me baseei em documentos históricos e fotos "
    "de museus, e usei a linguagem Python."
)
MACHINOME = (
    "From Machinome dot node dot assembly import... "
    "Em português: do módulo de montagem do Machinome, importe... "
    "Este é o Machinome, o framework CAD de código aberto para construir máquinas... "
    "The waterwheel drives the crankshaft. "
    "Em português: a rotação da roda-d'água aciona o virabrequim. "
    "Com o Machinome, máquinas podem ter código-fonte."
)
TESTING = (
    "O código-fonte também permite testar como as peças se encaixam. "
    "Este teste verifica se a lâmina não intersecta nenhuma das duas metades da tora. "
    "Testing steps. Em português, passos de teste. "
    "Esse decorador repete essas verificações em treze instantes de zero a quatro "
    "segundos: uma volta completa da roda. Cada amostra reposiciona a máquina "
    "e verifica a geometria. Isso verifica as posições amostradas, não todos "
    "os momentos entre elas."
)
FILM_SOURCE = (
    "O código-fonte deste vídeo também está em Python. Uma cena, uma câmera, "
    "uma voz. As palavras que eu digo dizem à câmera quando se mover."
)
THIS_SCENE = scene_narration("ThisScene")
OPEN_SOURCE = (
    "E a melhor parte: tudo isso é código aberto! "
    "O Machinome conecta tecnologias CAD que já existem: "
    "OpenSCAD, SolidPython, CadQuery, Build123d, FreeCAD, JSCAD, OCCT, Trimesh."
)
STREAM = "E, por baixo de tudo, uma corrente de ferramentas de código aberto..."
CLOSING = (
    "A roda faz revoluções, e os humanos constroem as suas. "
    "Eu sou o Machinome. Meu propósito é permitir que todas as máquinas sejam "
    "de código aberto. O que VOCÊ quer construir agora?"
)

lines = Narration("\n\n".join((
    OPENING, MECHANISM, RECONSTRUCTION, MACHINOME, TESTING, FILM_SOURCE,
    THIS_SCENE, OPEN_SOURCE, STREAM, CLOSING,
)))

AUDIO = {
    "provider": "elevenlabs",
    "model": "eleven_v3",
    "voice": "GDzHdQOi6jjf8zaXhCYD",
    "voiceLabel": "Raquel — Português (Brasil)",
    "outputFormat": "pcm_24000",
    "voiceSettings": {"stability": 0.5, "similarity_boost": 0.75},
    # Restore the delivery break normalized out by Narration.
    "replacements": {"aberto... A roda": "aberto...\n\nA roda"},
}

BEATS = (
    ("opening", "Abertura", "A roda faz revoluções, e os humanos dão"),
    ("ancestor", "Leonardo", "Há cinco séculos"),
    ("mechanism", "Como funciona", "Vou mostrar como ela funciona"),
    ("wheel", "Roda-d'água", "A água sob a roda"),
    ("crank", "Manivela", "Uma manivela"),
    ("rod", "Biela", "uma biela"),
    ("pawl", "Lingueta de avanço", "esta alavanca comprida puxa uma lingueta"),
    ("holding", "Lingueta de retenção", "Uma segunda lingueta"),
    ("rope", "Corda", "enrola uma corda nesse eixo"),
    ("shaft", "Eixo composto", "um eixo composto"),
    ("carriage", "Carro", "A segunda corda puxa a tora"),
    ("research", "Fontes históricas", "Para reconstruir esta máquina"),
    ("drawing", "Desenho", "documentos históricos"),
    ("museum", "Fotos de museus", "fotos de museus"),
    ("import", "Importação", "From Machinome dot node dot assembly import"),
    ("relation", "Relação em inglês", "The waterwheel drives the crankshaft"),
    ("translation", "Em português", "Em português: a rotação"),
    ("testing", "Teste de geometria", "O código-fonte também permite testar"),
    ("steps", "Passos de teste", "Testing steps"),
    ("film", "Código do vídeo", "O código-fonte deste vídeo"),
    ("mirror", "Esta exata cena", "E aqui está o código desta exata"),
    ("open", "Código aberto", "E a melhor parte: tudo isso é código aberto"),
    ("cad", "Tecnologias CAD", "O Machinome conecta tecnologias CAD que já existem"),
    ("openscad", "OpenSCAD", "OpenSCAD"),
    ("solidpython", "SolidPython", "SolidPython"),
    ("occt", "OCCT", "OCCT"),
    ("cadquery", "CadQuery", "CadQuery"),
    ("build123d", "Build123d", "Build123d"),
    ("freecad", "FreeCAD", "FreeCAD"),
    ("jscad", "JSCAD", "JSCAD"),
    ("trimesh", "Trimesh", "Trimesh"),
    ("stream", "Corrente de ferramentas", "E, por baixo de tudo"),
    ("return", "A roda retorna", "A roda faz revoluções, e os humanos constroem"),
    ("purpose", "Propósito", "Eu sou o Machinome"),
    ("question", "Convite", "O que VOCÊ quer construir agora"),
)


def document():
    return {
        "format": "machinome-release-narration/1",
        "audio": AUDIO,
        "chapters": [{"id": "continuous", "narration": lines.text}],
        "pronunciation": "../machinome-release-1/assets/pronunciation.json",
        "beats": [
            {"id": key, "label": label, "phrase": phrase}
            for key, label, phrase in BEATS
        ],
    }


if __name__ == "__main__":
    build = Path(__file__).resolve().parent / "_build"
    build.mkdir(exist_ok=True)
    (build / "narration-input.json").write_text(
        json.dumps(document(), indent=2) + "\n", encoding="utf-8"
    )
    (build / "narration.txt").write_text(lines.text + "\n", encoding="utf-8")
    print(f"One narration: {len(lines.text)} characters.")
