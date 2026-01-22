# SECAD Tester 🧪

Este projeto é uma ferramenta de automação para testes e navegação no portal SECAD. Ele utiliza **Playwright** para automatizar interações no navegador, como login, seleção de programas/volumes e navegação em artigos.

## 🚀 Como Começar

### Pré-requisitos

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)

### 📦 Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd tester
    ```

2.  **Crie e ative um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instale os navegadores do Playwright:**
    ```bash
    playwright install chromium
    ```

## ⚙️ Configuração

Antes de rodar, você precisa configurar suas credenciais.

1.  Abra o arquivo `config.py`.
2.  Insira seu usuário e senha:
    ```python
    USERNAME = "seu-email@exemplo.com"
    PASSWORD = "sua-senha"
    ```
3.  Ajuste as configurações de execução se necessário (`HEADLESS` para ver o navegador ou não).

## 🛠️ Como Rodar

Para iniciar o script de automação, execute o comando:

```bash
python main.py
```

### O que o script faz:
1.  Realiza o login no portal.
2.  Lida com modais de "Primeiro Acesso".
3.  Permite selecionar interativamente o programa e o volume.
4.  Navega pelos artigos, realizando scroll e interagindo com elementos (botões, questões).

## 📁 Estrutura do Projeto

- `main.py`: Ponto de entrada do script.
- `config.py`: Configurações de acesso e execução.
- `selectors.py`: Seletores CSS utilizados para encontrar elementos na página.
- `utils.py`: Funções utilitárias (logger, cliques seguros).
- `.gitignore`: Arquivos e diretórios ignorados pelo Git.
