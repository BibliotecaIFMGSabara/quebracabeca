# Relatório de melhorias

## Resultado geral

O projeto deixou de ser uma vitrine genérica de “jogos incríveis” e passou a funcionar como um catálogo educativo de jogos, brinquedos de habilidade e quebra-cabeças físicos.

## Melhorias técnicas

- Redução aproximada de **40 MB para 1,3 MB** no projeto descompactado.
- Conversão das imagens válidas de PNG para WebP, com dimensões adequadas à web.
- Remoção de arquivos de imagem corrompidos.
- Criação de ilustração SVG substituta para a Argola Prisioneira.
- Remoção das dependências de Bootstrap, Font Awesome e Google Fonts.
- O site publicado não depende de CDN ou biblioteca JavaScript externa.
- Cartões agora são links HTML reais, acessíveis por teclado, sem `onclick` duplicado.
- Busca textual e filtros por categoria com atualização acessível da contagem.
- HTML semântico, link “pular para o conteúdo”, foco visível e suporte a `prefers-reduced-motion`.
- Layout responsivo para celular, tablet e desktop.
- Folha de impressão para páginas de detalhes.
- Metadados Open Graph e dados estruturados JSON-LD.
- Página `404.html` própria para GitHub Pages.
- Base única de conteúdo em `data/jogos.json`.
- Templates em Jinja e gerador estático em `scripts/build.py`.
- Validador de títulos, IDs, links locais e imagens em `scripts/validate.py`.
- Workflow do GitHub Actions para gerar e validar o site a cada envio.

## Melhorias conceituais

- Nova ideia central: **“um acervo para pensar com as mãos”**.
- O site deixa claro que o jogo não ensina automaticamente; a mediação transforma tentativa em experiência.
- O erro é tratado como informação para a próxima tentativa, não como fracasso.
- Inclusão de perguntas de mediação em cada jogo.
- Inclusão de adaptações de participação e acessibilidade.
- Aviso explícito para não utilizar tempo de resolução como teste informal de inteligência.
- Distinção editorial entre:
  - regra conhecida;
  - prática por tentativas;
  - guia de exploração;
  - proposta de uso.
- Cuidado para não inventar origem, regra ou mecanismo quando o exemplar não tem identificação suficiente.

## Melhorias de conteúdo

- Os 15 jogos com páginas existentes agora aparecem na coleção principal.
- Foram incluídos na página inicial: Bilboquê, Dança das Cores e Hora do Rush.
- “Senhoritas Chinesas” foi apresentado pelo nome mais difundido, **Damas Chinesas**, mantendo o nome do acervo como alias.
- “Travas dos Heróis para Montar” foi normalizado como **Estrela de Madeira**, preservando o nome anterior como referência.
- As páginas de Tetris 3D foram corrigidas para descrever quebra-cabeças físicos de empacotamento e montagem, não o funcionamento de um videogame tridimensional.
- Histórias genéricas e afirmações difíceis de verificar foram substituídas por descrição do objeto, método de investigação e cuidados.
- Jogos com fontes institucionais ou de fabricante receberam seção de referências.
- Cada página agora contém:
  - objetivo;
  - participantes, tempo e dificuldade;
  - descrição do desafio;
  - sequência de experimentação;
  - possibilidades educativas;
  - perguntas de mediação;
  - adaptações de acessibilidade;
  - cuidados com o exemplar e com a informação;
  - referências, quando disponíveis.

## Manutenção

Para alterar textos ou acrescentar um jogo:

1. Edite `data/jogos.json`.
2. Execute `python scripts/build.py`.
3. Execute `python scripts/validate.py`.
4. Envie os arquivos ao repositório.

## Validação realizada

Os scripts de geração e validação foram executados com sucesso. Todos os arquivos locais referenciados existem, as imagens são válidas e cada página possui um único título principal.

## Pontos que ainda dependem de decisão humana

- Nome da instituição responsável, contatos, autoria e licença não foram acrescentados porque não constavam do projeto fornecido.
- Os quebra-cabeças sem manual precisam ser comparados com o exemplar físico antes de receber uma solução específica.
- Depois da publicação, é recomendável testar o domínio real em celular e computador e executar uma auditoria Lighthouse no endereço público.
