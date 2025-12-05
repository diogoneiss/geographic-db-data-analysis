# Dados Eleitorais Espacializados - Santa Catarina (2022)

## Introdução

Este repositório contém os artefatos desenvolvidos para o Trabalho Prático da disciplina de Banco de Dados Geográficos (BDGEO). O objetivo do projeto é realizar a aquisição, tratamento, armazenamento e análise espacial de dados eleitorais referentes às eleições de 2022 para o cargo de Deputado Estadual em Santa Catarina.

O projeto integra dados eleitorais do TSE com dados censitários, indicadores socioeconômicos e dados de mortalidade, permitindo análises de correlação espacial e visualizações geográficas em diferentes níveis de agregação (município, região imediata e região intermediária).

## Estrutura de Diretórios

A estrutura do projeto está organizada da seguinte forma:

*   **`data_sources/`**: Contém os arquivos de dados brutos utilizados no projeto, não colocados no git. Outras pastas foaram omitidas.
    *   `br_bd_diretorios_*`: Dados administrativos e códigos de municípios/regiões (Base dos Dados).
    *   `br_geobr_mapas_*`: Arquivos de geometria espacial (municípios, regiões imediatas/intermediárias).
    *   `br_inep_indicador_*`: Indicadores socioeconômicos (INSE).
    *   `consulta_cand_2022/`: Dados dos candidatos (TSE).
    *   `votacao_secao_2022_SC/`: Dados brutos de votação por seção eleitoral.
    *   `df_espectro_politico.csv`: Classificação de espectro político.
*   **`database_dump/`**: Backups e dumps do banco de dados PostgreSQL/PostGIS contendo as tabelas processadas e espacializadas.
*   **`output/`**: Relatórios gerados em formatos LaTeX, HTML e RMarkdown (`eleicoes22_introspection`, `eleicoes22_stats`).
*   **`qgis/`**: Projetos do QGIS (`.qgz`) e templates de layout (`.qpt`) utilizados para a geração dos mapas e visualizações.
*   **`resultados/`**: Resultados parciais e finais das análises.
*   **`scripts/`**: Scripts utilizados para engenharia de dados, introspecção do banco e análises.
    *   `analysis/`: Scripts de análise de dados.
    *   `database_introspection/`: Scripts para verificar a estrutura e qualidade dos dados no banco.
*   **`visualizacao/`**: Imagens e mapas gerados, organizados por tema (agregados, partidos, socioeconômico, etc.).

## Fontes de Dados Utilizadas

As seguintes fontes de dados foram integradas neste projeto:

1.  **Dados Eleitorais (TSE)**:
    *   Resultados das eleições de 2022 (Votação por seção eleitoral).
    *   Perfil do eleitorado.
    *   Fonte: [Tribunal Superior Eleitoral (TSE)](https://dadosabertos.tse.jus.br/)

2.  **Dados Administrativos e Geográficos**:
    *   Diretórios Brasileiros (códigos IBGE, TSE, etc.).
    *   Malhas geográficas (Municípios, Regiões Imediatas e Intermediárias) via pacote `geobr`.
    *   Fonte: [Base dos Dados](https://basedosdados.org/) e IBGE.

3.  **Indicadores Socioeconômicos**:
    *   Indicador de Nível Socioeconômico (INSE) do município.
    *   Indicadores municipais gerais.
    *   Fonte: Base dos Dados (INEP/IBGE).

4.  **Dados Extras (Saúde)**:
    *   Sistema de Informações sobre Mortalidade (SIM).
    *   Utilizado para análises de correlação com dados de saúde pública.
    *   Fonte: DATASUS (via Base dos Dados).

## Tecnologias Utilizadas

*   **Banco de Dados**: PostgreSQL com extensão PostGIS.
*   **Análise e Processamento**: Python, SQL.
*   **Visualização Espacial**: QGIS.
*   **Documentação**: LaTeX/RMarkdown.

---
*Autor: Diogo Neiss*
