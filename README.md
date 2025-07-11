# Centro de Performance Pessoal (Projeto N=1)

**Lema:** *Deixar de ser um recetor passivo de dados e passar a ser o cientista ativo da minha própria saúde.*

## 1. Visão do Projeto
Este projeto é um sistema de análise de dados de saúde e performance pessoal. O objetivo é integrar dados de múltiplas fontes (Garmin, nutrição, etc.) para criar scores personalizados de **Recuperação** e **Esforço**, fornecendo insights acionáveis para otimizar o treino, o descanso e o bem-estar geral.

## 2. Estado Atual
**Fase 1: Coletor de Dados Robusto (MVP) - ✅ CONCLUÍDO**
Nesta fase, construímos a fundação do projeto. O sistema atual é capaz de:
- Autenticar de forma segura e automática na API da Garmin usando um token persistente.
- Recolher dados diários via GraphQL para métricas chave como Sono, VFC, Passos e Stress.
- Processar ("parsing") das respostas JSON complexas para extrair os valores importantes.
- Apresentar um relatório diário resumido no terminal.
- Suportar um modo de depuração (`--full`) para visualização dos dados brutos.

## 3. Tech Stack
- **Linguagem:** Python
- **Comunicação com API:** `garth` (para autenticação OAuth1 e pedidos GraphQL)
- **Análise de Dados (Futuro):** `pandas`
- **Interface Web (Futuro):** `Streamlit`
- **Controlo de Versão:** `Git` & `GitHub`

## 4. Como Instalar e Configurar
1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/PTEduardoCosta/Performance_N1.git](https://github.com/PTEduardoCosta/Performance_N1.git)
    cd Performance_N1
    ```
2.  **Criar e Ativar o Ambiente Virtual:**
    ```bash
    # Criar o ambiente
    python -m venv venv
    
    # Ativar o ambiente (Windows PowerShell)
    .\venv\Scripts\activate
    ```
3.  **Instalar as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Primeira Execução (Login Interativo):**
    Na primeira vez que executar o script, ele não encontrará uma sessão guardada e irá pedir as suas credenciais Garmin para criar o token de autenticação.
    ```bash
    python main.py
    ```
    Siga as instruções no terminal para introduzir o seu email, password e código MFA. O token será guardado para todas as execuções futuras.

## 5. Como Usar
-   **Execução Simples (Relatório Resumido):**
    Use o script `run.bat` (duplo clique) ou execute no terminal:
    ```bash
    python main.py
    ```
-   **Execução Completa (Resumo + Dados JSON):**
    Para fins de depuração ou análise profunda, use o argumento `--full`:
    ```bash
    python main.py --full
    ```
## 6. Próximos Passos (Roadmap v1.1)
- [ ] Implementar as fórmulas para `calculate_recovery_score()` e `calculate_effort_score()` no `analysis.py`.
- [ ] Guardar os scores diários e dados chave num ficheiro CSV para análise histórica. 
