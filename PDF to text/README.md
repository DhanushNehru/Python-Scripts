# PDF to Text Converter

Este projeto é uma ferramenta em Python para converter arquivos PDF em texto limpo e legível. Ele foi projetado para extrair texto de PDFs locais e remotos, realizar o pós-processamento do texto extraído para melhorar a legibilidade e salvar o conteúdo formatado em arquivos `.txt`. O projeto também inclui funcionalidades de download de PDFs a partir de URLs e limpeza de texto para evitar problemas com quebras de linha e espaçamento desorganizado.

---

## Funcionalidades
1. **Extração de Texto de PDFs Locais e Remotos**: 
   - Suporte para arquivos PDF armazenados localmente e para PDFs disponibilizados via URL.
2. **Limpeza e Formatação do Texto**:
   - Remoção de quebras de linha indesejadas e espaçamento excessivo.
   - Manutenção de parágrafos e estrutura original.
3. **Salvamento do Texto em Arquivos `.txt`**:
   - O texto extraído pode ser salvo em um arquivo `.txt` com o mesmo nome do PDF original.
4. **Criação Automática de Pastas de Saída**:
   - Organiza os textos gerados em uma pasta de saída (`output_texts`) para fácil navegação e uso futuro.

## Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- `requests`
- `PyPDF2`

Se ainda não as tiver, instale usando:

```bash
pip install requests PyPDF2
