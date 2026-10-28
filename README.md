# Acervo de Jogos e Quebra-Cabeças

Site estático e acessível para apresentar jogos de estratégia, brinquedos de habilidade e quebra-cabeças de lógica e montagem.

## Estrutura

- `data/jogos.json`: fonte única dos textos, metadados e referências;
- `templates/`: modelos da página inicial e das páginas de detalhes;
- `scripts/build.py`: gera o HTML estático;
- `scripts/validate.py`: verifica títulos, links locais, IDs e imagens;
- `css/site.css`: estilos compartilhados;
- `js/site.js`: busca, filtros e compartilhamento;
- `images/`: imagens locais; são aceitos WebP, PNG, JPG/JPEG, SVG, GIF e BMP. Se o arquivo mantiver o mesmo nome-base, o gerador encontra a nova extensão automaticamente.

## Editar conteúdo

1. Altere `data/jogos.json`.
2. Execute `python scripts/build.py`.
3. Execute `python scripts/validate.py`.
4. Publique os arquivos gerados no GitHub Pages. No ramo `main`, o GitHub Actions também reconstrói e grava automaticamente as páginas geradas quando os dados mudam.

Dependências para geração e validação:

```bash
pip install beautifulsoup4 jinja2 pillow
```

O site publicado não depende de bibliotecas externas, CDNs, frameworks ou fontes remotas.

## Princípio editorial

As páginas distinguem regras conhecidas, guias de exploração e propostas de uso. Quando o exemplar não possui identificação ou manual suficiente, o texto evita atribuir origem, regra ou solução sem confirmação.
