# Ficha de Personagem de D&D 5.5E

Este projeto foi desenvolvido por [João Pedro Lopes Lenharo](https://github.com/joaoLopesLenharo/-sheetsD-D) e é uma aplicação Python que permite criar, editar e gerenciar fichas de personagens de Dungeons & Dragons (D&D) 5.5E. A ferramenta foi projetada para facilitar o trabalho de jogadores e mestres, fornecendo uma interface intuitiva e poderosa para organizar todos os detalhes do seu personagem.

## Funcionalidades

- **Interface amigável:** Interface gráfica para edição de atributos, habilidades, magias, inventário e mais.
- **Exportação e Importação:** Salve suas fichas em arquivos JSON ou exporte-as para PDF.
- **Gerenciamento de magias e habilidades:** Adicione, edite e visualize magias, talentos e outros aspectos únicos do personagem.
- **Personalização:** Adicione recursos personalizados e anotações específicas para cada personagem.
- **Organização de dados:** Visualize e gerencie informações detalhadas do background, alinhamento e histórico do personagem com praticidade.
- **Responsividade:** Design interativo e dinâmico com fácil navegação.

## Requisitos

- Python 3.7 ou superior.
- Bibliotecas Python adicionais:
  - `tkinter` (incluso no Python padrão)
  - `Pillow` (para manipulação de imagens)
  - `reportlab` (para exportação de PDFs)

## Instalação

1. **Clone este repositório:**

    ```bash
    git clone https://github.com/joaoLopesLenharo/-sheetsD-D.git
    cd -sheetsD-D
    ```

2. **Crie um ambiente virtual (opcional):**

    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/MacOS
    venv\Scripts\activate   # Windows
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o programa:**

    ```bash
    python Ficha.py
    ```

5. **(Opcional) Gere um executável standalone:**

    Execute o script `build_exe.py` para criar um executável na pasta `dist`:

    ```bash
    python build_exe.py
    ```

## Uso

1. **Janela principal:**
   - A janela principal contém seções para informações básicas, atributos, magias, inventário e outros aspectos essenciais do personagem.

2. **Menus:**
   - **Salvar/Carregar:** Salve fichas no formato JSON ou carregue arquivos existentes.
   - **Exportar para PDF:** Gere um PDF formatado com todos os detalhes da ficha.
   - **Background e personalização:** Acesse ferramentas para detalhar a história e características únicas do personagem.

3. **Outras telas:**
   - Acesse funcionalidades adicionais, como gerenciamento de magias, talentos e habilidades, por meio dos botões disponíveis.

## Estrutura do Projeto

- **`Ficha.py`**: Arquivo principal com a implementação da interface e lógica do programa.
- **`build_exe.py`**: Script para criação de executáveis standalone (usando `pyinstaller`).
- **Dependências:**
  - `tkinter`: Criação da interface gráfica.
  - `Pillow`: Manipulação de imagens (ex.: foto do personagem).
  - `reportlab`: Geração de PDFs.

## Exemplos de Uso

- **Criação de Personagens:**
  Crie fichas detalhadas, incluindo atributos, histórico e alinhamento do personagem.
- **Organização para Mestres:**
  Gerencie múltiplos personagens e exporte dados para consulta rápida durante as sessões.
- **Personalização Avançada:**
  Adicione recursos e notas específicas para adaptar a ficha às necessidades da campanha.

### Módulos

- **Magias:** Adicione, edite e filtre magias por nível e descrição. Registre detalhes como tempo de conjuração, componentes e duração.
- **Talentos e Habilidades:** Gerencie as características e habilidades únicas do personagem.
- **Inventário:** Adicione itens, rastreie bônus, descreva equipamentos e calcule efeitos de atributos.

## Exportação e Importação

- **JSON:** Salve ou carregue fichas de personagem em um formato editável.
- **PDF:** Exporte sua ficha como um PDF formatado e pronto para impressão.

## Contribuindo

1. Faça um fork do repositório.
2. Crie uma nova branch para suas alterações:

    ```bash
    git checkout -b minha-feature
    ```

3. Commit suas alterações:

    ```bash
    git commit -m "Descrição da minha feature"
    ```

4. Faça um push para sua branch:

    ```bash
    git push origin minha-feature
    ```

5. Abra um pull request no repositório original.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo LICENSE para mais informações.

## Autor

Desenvolvido por [João Pedro Lopes Lenharo](https://github.com/joaoLopesLenharo/-sheetsD-D). Sinta-se à vontade para contribuir, reportar problemas ou sugerir melhorias!

## Agradecimentos

Agradecimentos especiais à comunidade Python pelo suporte e ferramentas que tornaram este projeto possível.