"""A standalone Brazilian Portuguese mechanical short, spoken by Leo."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

from machinome_movie import Narration

lines = Narration(
    "A roda dá voltas. A engenhosidade humana dá a ela um propósito. "
    "Há cinco séculos, Leonardo da Vinci desenhou uma serraria movida "
    "a água. A força de um rio ajudava a transformar árvores em tábuas. "
    "Mas como uma única roda faz tudo isso? "
    "A água gira a roda, que movimenta este eixo. "
    "Uma manivela e uma biela transformam o giro no sobe e desce da serra. "
    "Mas a tora também precisa avançar. Durante o corte, esta alavanca "
    "puxa uma lingueta por um dente da catraca. Uma segunda lingueta "
    "segura o avanço enquanto a primeira volta. "
    "Cada passo enrola uma corda neste eixo. Siga a corda: "
    "para baixo, e para o outro lado. Ela gira um eixo composto. "
    "O tambor largo desenrola uma corda, enquanto a parte mais fina "
    "recolhe outra. A segunda corda puxa a tora em direção à lâmina. "
    "Uma roda, duas funções: cortar e avançar."
)

AUDIO = {
    "provider": "elevenlabs",
    "model": "eleven_v3",
    "voice": "EbiSUflQjzm4g7S895SC",
    "voiceLabel": "Leo Antonio — Português (Brasil)",
    "outputFormat": "pcm_24000",
    "voiceSettings": {"stability": 0.5, "similarity_boost": 0.75},
}
