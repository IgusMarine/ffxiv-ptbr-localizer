# FFXIV PT-BR Localizer

Plugin [Dalamud](https://github.com/goatcorp/Dalamud) que traduz a interface e os textos de **Final Fantasy XIV** para **português brasileiro (PT-BR)**.

> ⚠️ **Projeto de fã, não-oficial e sem afiliação com a Square Enix.** Em desenvolvimento — a tradução melhora continuamente (o plugin se atualiza sozinho). Use por sua conta e risco.

## Como instalar (in-game, via Dalamud)

1. No jogo, abra as configurações do Dalamud: digite **`/xlsettings`**.
2. Aba **Experimental** → seção **Custom Plugin Repositories**.
3. Cole esta URL no campo e clique no **`+`**, depois **salve** (ícone de disquete):

   ```
   https://raw.githubusercontent.com/IgusMarine/ffxiv-ptbr-localizer/main/pluginmaster.json
   ```

4. Abra o instalador de plugins: **`/xlplugins`** → procure **FFXIV PT-BR Localizer** → **Install**.

Pronto! As atualizações de código chegam automaticamente pelo Dalamud, e o **texto traduzido se atualiza sozinho** (baixado de um CDN) conforme os revisores melhoram a tradução — sem precisar reinstalar.

## Como funciona

- O plugin troca, em tempo real, o texto em inglês na tela pela tradução PT-BR.
- A base de traduções (`ffxiv_translations.bin`) é baixada/atualizada de um CDN público; o plugin valida a integridade (SHA-256) antes de aplicar e mantém uma cópia embutida como fallback offline.

## Contribuir com a tradução

A revisão é colaborativa. Quer ajudar a melhorar os textos? Fale com a comunidade PT-BR do projeto.

## Créditos

Feito pela comunidade de tradução PT-BR de FFXIV. Final Fantasy XIV © SQUARE ENIX.
