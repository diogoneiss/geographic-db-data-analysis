# Introspection of schema `eleicoes22`

- Generated at: 2025-10-30 22:29:13
- Database: gis @ localhost:5434
- Tables found: 16
- Views found: 3
- Materialized views found: 3
- Columns per object shown: up to 30
- Sample rows per object: 5 (random)

---

## Tables

### eleicoes22.br_bd_diretorios_brasil_distrito

- Estimated rows: 0
- Columns: 4 (showing first 4)
- Size (heap): 640 KB
- Size (indexes): 0 B
- Size (total): 640 KB

```sql
CREATE TABLE "eleicoes22"."br_bd_diretorios_brasil_distrito" (
  "id_distrito" integer,
  "nome" text,
  "id_municipio" text,
  "sigla_uf" text

);
```

**Sample (5 rows, first 4 columns):**

|   id_distrito | nome                 |   id_municipio | sigla_uf   |
|--------------:|:---------------------|---------------:|:-----------|
|     311000415 | Morro Vermelho       |        3110004 | MG         |
|     150530405 | Oriximiná            |        1505304 | PA         |
|     221040905 | São Miguel do Tapuio |        2210409 | PI         |
|     230240407 | Águas Belas          |        2302404 | CE         |
|     130380920 | São Felipe           |        1303809 | AM         |

### eleicoes22.br_bd_diretorios_brasil_municipio

- Estimated rows: 0
- Columns: 27 (showing first 27)
- Size (heap): 1.51 MB
- Size (indexes): 0 B
- Size (total): 1.51 MB

```sql
CREATE TABLE "eleicoes22"."br_bd_diretorios_brasil_municipio" (
  "id_municipio" text,
  "id_municipio_2" text,
  "id_municipio_tse" text,
  "id_municipio_rf" text,
  "id_municipio_bcb" text,
  "nome" text,
  "capital_uf" text,
  "id_comarca" text,
  "id_regiao_saude" text,
  "nome_regiao_saude" text,
  "id_regiao_imediata" text,
  "nome_regiao_imediata" text,
  "id_regiao_intermediaria" text,
  "nome_regiao_intermediaria" text,
  "id_microrregiao" text,
  "nome_microrregiao" text,
  "id_mesorregiao" text,
  "nome_mesorregiao" text,
  "id_regiao_metropolitana" text,
  "nome_regiao_metropolitana" text,
  "ddd" text,
  "id_uf" text,
  "sigla_uf" text,
  "nome_uf" text,
  "nome_regiao" text,
  "amazonia_legal" integer,
  "centroide" geometry

);
```

**Sample (5 rows, first 27 columns):**

|   id_municipio |   id_municipio_2 |   id_municipio_tse |   id_municipio_rf |   id_municipio_bcb | nome                 |   capital_uf |   id_comarca |   id_regiao_saude | nome_regiao_saude    |   id_regiao_imediata | nome_regiao_imediata   |   id_regiao_intermediaria | nome_regiao_intermediaria   |   id_microrregiao | nome_microrregiao    |   id_mesorregiao | nome_mesorregiao                | id_regiao_metropolitana   | nome_regiao_metropolitana        |   ddd |   id_uf | sigla_uf   | nome_uf           | nome_regiao   |   amazonia_legal | centroide                                  |
|---------------:|-----------------:|-------------------:|------------------:|-------------------:|:---------------------|-------------:|-------------:|------------------:|:---------------------|---------------------:|:-----------------------|--------------------------:|:----------------------------|------------------:|:---------------------|-----------------:|:--------------------------------|:--------------------------|:---------------------------------|------:|--------:|:-----------|:------------------|:--------------|-----------------:|:-------------------------------------------|
|        3539202 |           353920 |              68853 |              6885 |              29782 | Pirapozinho          |            0 |      3539202 |             35112 | Alta Sorocabana      |               350018 | Presidente Prudente    |                      3505 | Presidente Prudente         |             35036 | Presidente Prudente  |             3508 | Presidente Prudente             |                           |                                  |    18 |      35 | SP         | São Paulo         | Sudeste       |                0 | POINT(-51.6197485091438 -22.4796493116021) |
|        2915700 |           291570 |              36153 |              3615 |              13688 | Itamari              |            0 |      2915700 |             29015 | Jequié               |               290014 | Ipiaú                  |                      2904 | Vitória da Conquista        |             29031 | Ilhéus-Itabuna       |             2907 | Sul Baiano                      |                           |                                  |    73 |      29 | BA         | Bahia             | Nordeste      |                0 | POINT(-39.6592456554453 -13.7679458866116) |
|        3118304 |           311830 |              43656 |              4365 |               8882 | Conselheiro Lafaiete |            0 |      3118304 |             31079 | Conselheiro Lafaiete |               310038 | Conselheiro Lafaiete   |                      3107 | Barbacena                   |             31034 | Conselheiro Lafaiete |             3107 | Metropolitana de Belo Horizonte |                           |                                  |    31 |      31 | MG         | Minas Gerais      | Sudeste       |                0 | POINT(-43.7886821392692 -20.6660145792377) |
|        4314175 |           431417 |              89567 |              1156 |              57864 | Pedras Altas         |            0 |      4314506 |             43021 | Região 21 - Sul      |               430010 | Bagé                   |                      4302 | Pelotas                     |             43032 | Serras de Sudeste    |             4307 | Sudeste Rio-grandense           |                           |                                  |    53 |      43 | RS         | Rio Grande do Sul | Sul           |                0 | POINT(-53.691108537891 -31.8391932900592)  |
|        4103453 |           410345 |              79855 |              7985 |              41179 | Cafelândia           |            0 |      4106308 |             41010 | 10ª RS Cascavel      |               410006 | Cascavel               |                      4103 | Cascavel                    |             41023 | Cascavel             |             4106 | Oeste Paranaense                | 6101                      | Região Metropolitana de Cascavel |    45 |      41 | PR         | Paraná            | Sul           |                0 | POINT(-53.3639284459892 -24.6924406884538) |

### eleicoes22.br_bd_diretorios_brasil_setor_censitario

- Estimated rows: 452340
- Columns: 22 (showing first 22)
- Size (heap): 105.35 MB
- Size (indexes): 0 B
- Size (total): 105.35 MB

```sql
CREATE TABLE "eleicoes22"."br_bd_diretorios_brasil_setor_censitario" (
  "id_setor_censitario" text,
  "id_regiao" integer,
  "nome_regiao" text,
  "id_uf" integer,
  "nome_uf" text,
  "id_municipio" text,
  "nome_municipio" text,
  "id_distrito" integer,
  "nome_distrito" text,
  "id_subdistrito" double precision,
  "nome_subdistrito" text,
  "id_microrregiao" integer,
  "nome_microrregiao" text,
  "id_mesorregiao" integer,
  "nome_mesorregiao" text,
  "id_regiao_imediata" integer,
  "nome_regiao_imediata" text,
  "id_regiao_intermediaria" integer,
  "nome_regiao_intermediaria" text,
  "id_concentracao_urbana" integer,
  "nome_concentracao_urbana" text,
  "area_km2" text

);
```

**Sample (5 rows, first 22 columns):**

| id_setor_censitario   |   id_regiao | nome_regiao   |   id_uf | nome_uf    |   id_municipio | nome_municipio   |   id_distrito | nome_distrito   |   id_subdistrito | nome_subdistrito   |   id_microrregiao | nome_microrregiao   |   id_mesorregiao | nome_mesorregiao        |   id_regiao_imediata | nome_regiao_imediata   |   id_regiao_intermediaria | nome_regiao_intermediaria   | id_concentracao_urbana   | nome_concentracao_urbana   |   area_km2 |
|:----------------------|------------:|:--------------|--------:|:-----------|---------------:|:-----------------|--------------:|:----------------|-----------------:|:-------------------|------------------:|:--------------------|-----------------:|:------------------------|---------------------:|:-----------------------|--------------------------:|:----------------------------|:-------------------------|:---------------------------|-----------:|
| 354890610000014P      |           3 | Sudeste       |      35 | São Paulo  |        3548906 | São Carlos       |     354890610 | Água Vermelha   |      35489061000 |                    |             35025 | São Carlos          |             3505 | Araraquara              |               350037 | São Carlos             |                      3509 | Araraquara                  | 3548906                  | São Carlos/SP              |   0.927579 |
| 260960005000238P      |           2 | Nordeste      |      26 | Pernambuco |        2609600 | Olinda           |     260960005 | Olinda          |      26096000500 |                    |             26017 | Recife              |             2605 | Metropolitana de Recife |               260001 | Recife                 |                      2601 | Recife                      | 2611606                  | Recife/PE                  |   0.152541 |
| 290405005000046P      |           2 | Nordeste      |      29 | Bahia      |        2904050 | Bonito           |     290405005 | Bonito          |      29040500500 |                    |             29023 | Seabra              |             2906 | Centro Sul Baiano       |               290020 | Irecê                  |                      2907 | Irecê                       |                          |                            |   0.485039 |
| 350950205001980P      |           3 | Sudeste       |      35 | São Paulo  |        3509502 | Campinas         |     350950205 | Campinas        |      35095020500 |                    |             35032 | Campinas            |             3507 | Campinas                |               350038 | Campinas               |                      3510 | Campinas                    | 3509502                  | Campinas/SP                |   0.037166 |
| 140023305000015P      |           1 | Norte         |      14 | Roraima    |        1400233 | Caroebe          |     140023305 | Caroebe         |      14002330500 |                    |             14004 | Sudeste de Roraima  |             1402 | Sul de Roraima          |               140003 | Rorainópolis           |                      1402 | Rorainópolis - Caracaraí    |                          |                            | 464.135    |

### eleicoes22.br_geobr_mapas_limite_vizinhanca

- Estimated rows: 0
- Columns: 12 (showing first 12)
- Size (heap): 11.19 MB
- Size (indexes): 0 B
- Size (total): 11.19 MB

```sql
CREATE TABLE "eleicoes22"."br_geobr_mapas_limite_vizinhanca" (
  "id_uf" integer,
  "sigla_uf" text,
  "id_municipio" text,
  "nome_municipio" text,
  "id_distrito" integer,
  "nome_distrito" text,
  "id_subdistrito" double precision,
  "nome_subdistrito" text,
  "id_vizinhanca" double precision,
  "nome_vizinhanca" text,
  "referencia_geometria" text,
  "geometria" geometry

);
```

**Sample (5 rows, first 12 columns):**

|   id_uf | sigla_uf   |   id_municipio | nome_municipio     |   id_distrito | nome_distrito      |   id_subdistrito | nome_subdistrito   |   id_vizinhanca | nome_vizinhanca      | referencia_geometria   | geometria                                                                                                                |
|--------:|:-----------|---------------:|:-------------------|--------------:|:-------------------|-----------------:|:-------------------|----------------:|:---------------------|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------|
|      35 | SP         |        3548807 | São Caetano Do Sul |     354880705 | São Caetano Do Sul |      35488070500 |                    |    354880705007 | Mauá                 | neighborhood           | POLYGON((-46.567647 -23.64946,-46.568753 -23.647525,-46.568716 -23.639452,-46.57346 -23.639489,-46.574224 -23.640827,-4… |
|      42 | SC         |        4217907 | Tangará            |     421790705 | Tangará            |      42179070500 |                    |    421790705005 | Bela Vista           | neighborhood           | POLYGON((-51.24115156 -27.10124375,-51.24157567 -27.10100767,-51.23393755 -27.09929662,-51.23768304 -27.09087439,-51.24… |
|      42 | SC         |        4219309 | Videira            |     421930905 | Videira            |      42193090500 |                    |    421930905025 | Amarante             | neighborhood           | POLYGON((-51.1817491 -27.00679116,-51.18090653 -27.00618986,-51.18036627 -27.00556914,-51.18012105 -27.00501355,-51.179… |
|      32 | ES         |        3200607 | Aracruz            |     320060720 | Santa Cruz         |      32006072000 |                    |    320060720041 | Putiri               | neighborhood           | POLYGON((-40.10247842 -19.90278317,-40.10267227 -19.90324632,-40.10310116 -19.90550347,-40.10159283 -19.90576297,-40.10… |
|      43 | RS         |        4300406 | Alegrete           |     430040605 | Alegrete           |      43004060509 | Zona Sul           |    430040605013 | Porto Dos Aguateiros | neighborhood           | POLYGON((-55.7928268 -29.78963627,-55.79449693 -29.79012165,-55.79521877 -29.79049009,-55.79565905 -29.79095883,-55.796… |

### eleicoes22.br_geobr_mapas_municipio

- Estimated rows: 0
- Columns: 3 (showing first 3)
- Size (heap): 24.32 MB
- Size (indexes): 0 B
- Size (total): 24.32 MB

```sql
CREATE TABLE "eleicoes22"."br_geobr_mapas_municipio" (
  "id_municipio" text,
  "sigla_uf" text,
  "geometria" geometry

);
```

**Sample (5 rows, first 3 columns):**

|   id_municipio | sigla_uf   | geometria                                                                                                                |
|---------------:|:-----------|:-------------------------------------------------------------------------------------------------------------------------|
|        3157252 | MG         | POLYGON((-42.062588 -19.898056996,-42.070976 -19.886247996,-42.074017 -19.884883996,-42.094304 -19.895745996,-42.094463… |
|        3528403 | SP         | POLYGON((-47.288635809 -23.428730835,-47.29191281 -23.428531213,-47.294316113 -23.426512079,-47.298100636 -23.417426051… |
|        1711506 | TO         | POLYGON((-48.716626023 -12.401907894,-48.715154608 -12.397699428,-48.718013899 -12.397556123,-48.722601638 -12.40004537… |
|        4309159 | RS         | POLYGON((-52.599802136 -29.215921363,-52.603600981 -29.216181158,-52.604670612 -29.218762297,-52.609173037 -29.22229925… |
|        3141306 | MG         | POLYGON((-46.518423 -19.857662996,-46.522127 -19.859373996,-46.529612 -19.858102996,-46.541455 -19.868962996,-46.544907… |

### eleicoes22.br_geobr_mapas_regiao

- Estimated rows: 0
- Columns: 3 (showing first 3)
- Size (heap): 1.05 MB
- Size (indexes): 0 B
- Size (total): 1.05 MB

```sql
CREATE TABLE "eleicoes22"."br_geobr_mapas_regiao" (
  "id_regiao" integer,
  "nome_regiao" text,
  "geometria" geometry

);
```

**Sample (5 rows, first 3 columns):**

|   id_regiao | nome_regiao   | geometria                                                                                                                |
|------------:|:--------------|:-------------------------------------------------------------------------------------------------------------------------|
|           3 | Sudeste       | MULTIPOLYGON(((-45.33357188 -23.72257747,-45.34147357 -23.72778946,-45.34336595 -23.73663474,-45.34938978 -23.74253986,… |
|           5 | Centro Oeste  | POLYGON((-57.82871857 -20.93387894,-57.82489328 -20.93393294,-57.81978126 -20.93799556,-57.81881782 -20.94841223,-57.82… |
|           4 | Sul           | MULTIPOLYGON(((-48.52416256 -26.38646081,-48.52495919 -26.38494125,-48.52565627 -26.38645014,-48.52525249 -26.38747651,… |
|           2 | Nordeste      | MULTIPOLYGON(((-45.08845774 -1.43330349000001,-45.08602042 -1.42624844,-45.08785384 -1.42242009000001,-45.09217705 -1.4… |
|           1 | Norte         | MULTIPOLYGON(((-47.83476484 -0.659027890000008,-47.83585055 -0.655482390000006,-47.83817114 -0.657019659999999,-47.8365… |

### eleicoes22.br_geobr_mapas_regiao_imediata

- Estimated rows: 0
- Columns: 4 (showing first 4)
- Size (heap): 8.26 MB
- Size (indexes): 0 B
- Size (total): 8.26 MB

```sql
CREATE TABLE "eleicoes22"."br_geobr_mapas_regiao_imediata" (
  "id_uf" text,
  "sigla_uf" text,
  "id_regiao_imediata" text,
  "geometria" geometry

);
```

**Sample (5 rows, first 4 columns):**

|   id_uf | sigla_uf   |   id_regiao_imediata | geometria                                                                                                                |
|--------:|:-----------|---------------------:|:-------------------------------------------------------------------------------------------------------------------------|
|      29 | BA         |               290015 | POLYGON((-40.048035285 -14.950523859,-40.0497592789999 -14.953144328,-40.053071835 -14.964710683,-40.052181775 -14.9683… |
|      15 | PA         |               150013 | POLYGON((-50.9248995629999 -5.14917483799998,-50.927234577 -5.15145175199999,-51.5004565869999 -5.15015504299991,-52.05… |
|      31 | MG         |               310037 | POLYGON((-43.2966469999999 -20.851748997,-43.302694 -20.8538479969999,-43.3099939999999 -20.852380997,-43.3149789999999… |
|      51 | MT         |               510005 | POLYGON((-58.8799098749999 -12.210766487,-58.885899205 -12.213586637,-58.89284525 -12.21191204,-58.897052169 -12.215361… |
|      23 | CE         |               230015 | POLYGON((-40.686310821 -3.08035338599992,-40.7510415169999 -3.05078058,-40.7275832759999 -3.13009068,-40.715314443 -3.1… |

### eleicoes22.br_geobr_mapas_regiao_intermediaria

- Estimated rows: 0
- Columns: 4 (showing first 4)
- Size (heap): 4.7 MB
- Size (indexes): 0 B
- Size (total): 4.7 MB

```sql
CREATE TABLE "eleicoes22"."br_geobr_mapas_regiao_intermediaria" (
  "id_uf" text,
  "sigla_uf" text,
  "id_regiao_intermediaria" text,
  "geometria" geometry

);
```

**Sample (5 rows, first 4 columns):**

|   id_uf | sigla_uf   |   id_regiao_intermediaria | geometria                                                                                                                |
|--------:|:-----------|--------------------------:|:-------------------------------------------------------------------------------------------------------------------------|
|      22 | PI         |                      2201 | POLYGON((-42.685751478 -3.807246073,-42.698788194 -3.83216397900001,-42.7092762 -3.85681554400001,-42.716475803 -3.8686… |
|      13 | AM         |                      1302 | POLYGON((-69.894026118 -4.00067752600001,-69.935166628 -4.216471203,-69.943555884 -4.21659269299999,-69.951244053 -4.22… |
|      31 | MG         |                      3102 | POLYGON((-45.621422026 -15.016922521,-45.624618848 -15.021368493,-45.629398309 -15.020677772,-45.634758774 -15.02367943… |
|      42 | SC         |                      4205 | POLYGON((-51.407906808 -26.95449727,-51.401650444 -26.952516135,-51.400345982 -26.954484117,-51.401567374 -26.95756492,… |
|      51 | MT         |                      5103 | POLYGON((-61.541565754 -10.008658477,-61.546041804 -10.013139241,-61.545470147 -10.018848218,-61.551931194 -10.02913879… |

### eleicoes22.br_ibge_censo_2022_municipio

- Estimated rows: 5570
- Columns: 13 (showing first 13)
- Size (heap): 520 KB
- Size (indexes): 0 B
- Size (total): 520 KB

```sql
CREATE TABLE "eleicoes22"."br_ibge_censo_2022_municipio" (
  "id_municipio" text,
  "sigla_uf" text,
  "domicilios" integer,
  "populacao" integer,
  "area" integer,
  "taxa_alfabetizacao" double precision,
  "idade_mediana" text,
  "razao_sexo" text,
  "indice_envelhecimento" text,
  "populacao_indigena" text,
  "populacao_indigena_terra_indigena" text,
  "populacao_quilombola" text,
  "populacao_quilombola_territorio_quilombola" text

);
```

**Sample (5 rows, first 13 columns):**

|   id_municipio | sigla_uf   |   domicilios |   populacao |   area |   taxa_alfabetizacao |   idade_mediana |   razao_sexo |   indice_envelhecimento |   populacao_indigena |   populacao_indigena_terra_indigena |   populacao_quilombola |   populacao_quilombola_territorio_quilombola |
|---------------:|:-----------|-------------:|------------:|-------:|---------------------:|----------------:|-------------:|------------------------:|---------------------:|------------------------------------:|-----------------------:|---------------------------------------------:|
|        4218202 | SC         |        16734 |       46043 |    128 |              0.98571 |              36 |        95.75 |                   63.21 |                   20 |                                   0 |                      0 |                                            0 |
|        2110658 | MA         |         2249 |        7990 |    961 |              0.79364 |              28 |       102.07 |                   30.98 |                   16 |                                   0 |                    180 |                                            0 |
|        5219100 | GO         |         2252 |        6149 |    141 |              0.89609 |              35 |        96.96 |                   55.78 |                    6 |                                   0 |                      0 |                                            0 |
|        3103751 | MG         |         2878 |        8467 |    294 |              0.94713 |              33 |        99.69 |                   41.9  |                    0 |                                   0 |                      0 |                                            0 |
|        1504703 | PA         |        25016 |       83890 |   9094 |              0.87528 |              26 |       109.12 |                   19.43 |                  258 |                                 179 |                   6244 |                                         3406 |

### eleicoes22.br_ibge_censo_2022_populacao_idade_sexo

- Estimated rows: 2495360
- Columns: 7 (showing first 7)
- Size (heap): 221.89 MB
- Size (indexes): 0 B
- Size (total): 221.89 MB

```sql
CREATE TABLE "eleicoes22"."br_ibge_censo_2022_populacao_idade_sexo" (
  "id_municipio" text,
  "forma_declaracao_idade" text,
  "sexo" text,
  "idade" text,
  "idade_anos" text,
  "grupo_idade" text,
  "populacao" text

);
```

**Sample (5 rows, first 7 columns):**

|   id_municipio | forma_declaracao_idade   | sexo     | idade   |   idade_anos | grupo_idade   | populacao   |
|---------------:|:-------------------------|:---------|:--------|-------------:|:--------------|:------------|
|        2102374 | Data de nascimento       | Homens   | 2 meses |     0.166667 | 0 a 4 anos    | 3           |
|        3530508 | Data de nascimento       | Mulheres | 26 anos |    26        | 25 a 29 anos  | 409         |
|        4315552 | Idade presumida          | Homens   | 97 anos |    97        | 95 a 99 anos  |             |
|        3136108 | Idade presumida          | Mulheres | 69 anos |    69        | 65 a 69 anos  | 1           |
|        3126950 | Data de nascimento       | Homens   | 92 anos |    92        | 90 a 94 anos  |             |

### eleicoes22.br_ibge_censo_2022_setor_censitario_sc

- Estimated rows: 16736
- Columns: 1423 (showing first 30)
- Size (heap): 178.48 MB
- Size (indexes): 0 B
- Size (total): 178.48 MB

```sql
CREATE TABLE "eleicoes22"."br_ibge_censo_2022_setor_censitario_sc" (
  "id_uf" integer,
  "id_municipio" text,
  "id_setor_censitario" double precision,
  "area" double precision,
  "geometria" geometry,
  "pessoas" integer,
  "domicilios" integer,
  "domicilios_particulares" integer,
  "domicilios_coletivos" integer,
  "media_moradores_domicilios" double precision,
  "porcentagem_domicilios_imputados" double precision,
  "domicilios_particulares_ocupados" integer,
  "v00001" integer,
  "v00002" integer,
  "v00003" integer,
  "v00004" integer,
  "v00005" integer,
  "v00006" integer,
  "v00007" integer,
  "v00008" integer,
  "v00009" integer,
  "v00010" integer,
  "v00011" integer,
  "v00012" integer,
  "v00013" integer,
  "v00014" integer,
  "v00015" integer,
  "v00016" integer,
  "v00017" integer,
  "v00018" integer

);

-- NOTE: Column list truncated to first 30 columns.
```

**Sample (5 rows, first 30 columns):**

|   id_uf |   id_municipio |   id_setor_censitario |       area | geometria                                                                                                                |   pessoas |   domicilios |   domicilios_particulares |   domicilios_coletivos |   media_moradores_domicilios |   porcentagem_domicilios_imputados |   domicilios_particulares_ocupados | v00001   | v00002   | v00003   | v00004   | v00005   | v00006   | v00007   | v00008   | v00009   | v00010   | v00011   | v00012   | v00013   | v00014   | v00015   | v00016   | v00017   | v00018   |
|--------:|---------------:|----------------------:|-----------:|:-------------------------------------------------------------------------------------------------------------------------|----------:|-------------:|--------------------------:|-----------------------:|-----------------------------:|-----------------------------------:|-----------------------------------:|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|
|      42 |        4211900 |       421190005000150 | 0.0795889  | POLYGON((-48.6461801 -27.6289854,-48.6502154 -27.6288264999999,-48.6501905 -27.6290415,-48.6501926 -27.6292498999999,-4… |       889 |          350 |                       350 |                      0 |                          2.7 |                             0.0153 |                                326 | 326      | 0        | 0        | 326      | 889      | 0        | 0        | 103      | 0        | 0        | 426      | 0        | 0        | 463      | 0        | 0        | 56       | 97       |
|      42 |        4205456 |       420545605000087 | 1.21908    | POLYGON((-49.434557 -28.7344259999999,-49.4345427 -28.7347244,-49.4344983999999 -28.7347232,-49.4182403 -28.73392549999… |       120 |           58 |                        58 |                      0 |                          2.4 |                             0      |                                 50 | 50       | 0        | 0        | 50       | 120      | 0        | 0        | 18       | 0        | 0        | 60       | 0        | 0        | 60       | 0        | 0        | 14       | 17       |
|      42 |        4208401 |       420840105000037 | 0.40218    | POLYGON((-53.7309701 -27.1863753,-53.7309513 -27.1864065999999,-53.730742 -27.1867571999999,-53.7300640999999 -27.18638… |       650 |          234 |                       234 |                      0 |                          3   |                             0      |                                218 | 216      |          | 0        | 216      | 647      | 3        | 0        | 99       | 0        | 0        | 331      |          | 0        | 316      |          | 0        | 36       | 64       |
|      42 |        4201406 |       420140605000156 | 0.00537789 | POLYGON((-49.5339729999999 -28.9715677,-49.5346984999999 -28.9709336999999,-49.5350994 -28.9712522999999,-49.5343655 -2… |       289 |            1 |                         0 |                      1 |                          0   |                             0      |                                  0 |          |          |          |          |          |          |          |          |          |          |          |          |          |          |          |          |          |          |
|      42 |        4203204 |       420320410000008 | 0.105923   | POLYGON((-48.6564567 -27.0018216999999,-48.6567856 -27.0013602999999,-48.6569267 -27.0011615999999,-48.6571443999999 -2… |      1018 |          488 |                       488 |                      0 |                          2.7 |                             0.0162 |                                371 | 371      | 0        | 0        | 371      | 1018     | 0        | 0        | 128      | 0        | 0        | 523      | 0        | 0        | 495      | 0        | 0        | 71       | 108      |

### eleicoes22.br_inep_indicador_nivel_socioeconomico_municipio

- Estimated rows: 169302
- Columns: 15 (showing first 15)
- Size (heap): 18.7 MB
- Size (indexes): 0 B
- Size (total): 18.7 MB

```sql
CREATE TABLE "eleicoes22"."br_inep_indicador_nivel_socioeconomico_municipio" (
  "id_municipio" text,
  "ano" integer,
  "sigla_uf" text,
  "rede" text,
  "tipo_localizacao" text,
  "quantidade_alunos_inse" integer,
  "inse" double precision,
  "percentual_nivel" double precision,
  "percentual_nivel_2" double precision,
  "percentual_nivel_3" double precision,
  "percentual_nivel_4" double precision,
  "percentual_nivel_5" double precision,
  "percentual_nivel_6" double precision,
  "percentual_nivel_7" double precision,
  "percentual_nivel_8" double precision

);
```

**Sample (5 rows, first 15 columns):**

|   id_municipio |   ano | sigla_uf   |   rede |   tipo_localizacao |   quantidade_alunos_inse |   inse |   percentual_nivel |   percentual_nivel_2 |   percentual_nivel_3 |   percentual_nivel_4 |   percentual_nivel_5 |   percentual_nivel_6 |   percentual_nivel_7 |   percentual_nivel_8 |
|---------------:|------:|:-----------|-------:|-------------------:|-------------------------:|-------:|-------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
|        2209906 |  2019 | PI         |      2 |                  1 |                      107 | 3.9676 |              11.31 |                37.21 |                26.18 |                15.83 |                 7.59 |                 1    |                 0.87 |                 0    |
|        3100104 |  2021 | MG         |      0 |                  2 |                        8 | 4.7    |               0    |                12.5  |                12.5  |                50    |                25    |                 0    |                 0    |                 0    |
|        2933109 |  2021 | BA         |      3 |                  1 |                      108 | 4.38   |               1.66 |                32.03 |                19.12 |                28.05 |                10.08 |                 6.74 |                 2.32 |                 0    |
|        4108205 |  2021 | PR         |      2 |                  1 |                      128 | 5.51   |               0    |                 0.74 |                 6.53 |                11.25 |                28.74 |                33.03 |                18.98 |                 0.73 |
|        2604205 |  2021 | PE         |      5 |                  0 |                      833 | 4.4    |               3.64 |                25.75 |                27.53 |                22.99 |                11.45 |                 5.8  |                 2.85 |                 0    |

### eleicoes22.br_ms_sim_municipio_causa_idade_sexo_raca

- Estimated rows: 40004
- Columns: 13 (showing first 13)
- Size (heap): 9.27 MB
- Size (indexes): 0 B
- Size (total): 9.27 MB

```sql
CREATE TABLE "eleicoes22"."br_ms_sim_municipio_causa_idade_sexo_raca" (
  "ano" integer,
  "sigla_uf" text,
  "sigla_uf_nome" text,
  "id_municipio" text,
  "id_municipio_nome" text,
  "causa_basica" text,
  "causa_basica_descricao_subcategoria" text,
  "causa_basica_descricao_categoria" text,
  "causa_basica_descricao_capitulo" text,
  "idade" integer,
  "sexo" text,
  "raca_cor" text,
  "numero_obitos" text

);
```

**Sample (5 rows, first 13 columns):**

|   ano | sigla_uf   | sigla_uf_nome   |   id_municipio | id_municipio_nome   | causa_basica   | causa_basica_descricao_subcategoria                                                                                      | causa_basica_descricao_categoria                                                                          | causa_basica_descricao_capitulo               |   idade | sexo      | raca_cor   |   numero_obitos |
|------:|:-----------|:----------------|---------------:|:--------------------|:---------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------|:----------------------------------------------|--------:|:----------|:-----------|----------------:|
|  2019 | SC         | Santa Catarina  |        4219705 | Xaxim               | C760           | Neoplasia maligna da cabeça, face e pescoço                                                                              | Neoplasia maligna de outras localizações e de localizações mal definidas                                  | Neoplasmas (tumores)                          |      60 | Masculino | Branca     |               1 |
|  2019 | SC         | Santa Catarina  |        4211058 | Monte Carlo         | J159           | Pneumonia bacteriana não especificada                                                                                    | Pneumonia bacteriana não classificada em outra parte                                                      | Doenças do aparelho respiratório              |      79 | Feminino  | Branca     |               1 |
|  2019 | SC         | Santa Catarina  |        4214805 | Rio do Sul          | I219           | Infarto agudo do miocárdio não especificado                                                                              | Infarto agudo do miocárdio                                                                                | Doenças do aparelho circulatório              |      81 | Feminino  | Branca     |               1 |
|  2019 | SC         | Santa Catarina  |        4202404 | Blumenau            | I698           | Seqüelas de outras doenças cerebrovasculares e das não especificadas                                                     | Seqüelas de doenças cerebrovasculares                                                                     | Doenças do aparelho circulatório              |      56 | Feminino  | Branca     |               1 |
|  2019 | SC         | Santa Catarina  |        4215505 | Santa Cecília       | V446           | Ocupante de um automóvel [carro] traumatizado em colisão com um veículo de transporte pesado ou um ônibus - passageiro … | Ocupante de um automóvel [carro] traumatizado em colisão com um veículo de transporte pesado ou um ônibus | Causas externas de morbidade e de mortalidade |      57 | Feminino  | Branca     |               1 |

### eleicoes22.br_tse_eleicoes_resultados_candidato_municipio_sc

- Estimated rows: 263435
- Columns: 16 (showing first 16)
- Size (heap): 41.8 MB
- Size (indexes): 0 B
- Size (total): 41.8 MB

```sql
CREATE TABLE "eleicoes22"."br_tse_eleicoes_resultados_candidato_municipio_sc" (
  "ano" integer,
  "turno" integer,
  "id_eleicao" integer,
  "tipo_eleicao" text,
  "data_eleicao" text,
  "sigla_uf" text,
  "id_municipio" text,
  "id_municipio_tse" text,
  "cargo" text,
  "numero_partido" integer,
  "sigla_partido" text,
  "titulo_eleitoral_candidato" text,
  "sequencial_candidato" text,
  "numero_candidato" text,
  "resultado" text,
  "votos" integer

);
```

**Sample (5 rows, first 16 columns):**

|   ano |   turno |   id_eleicao | tipo_eleicao      | data_eleicao   | sigla_uf   |   id_municipio |   id_municipio_tse | cargo            |   numero_partido | sigla_partido   |   titulo_eleitoral_candidato |   sequencial_candidato |   numero_candidato | resultado   |   votos |
|------:|--------:|-------------:|:------------------|:---------------|:-----------|---------------:|-------------------:|:-----------------|-----------------:|:----------------|-----------------------------:|-----------------------:|-------------------:|:------------|--------:|
|  2022 |       1 |          546 | eleicao ordinaria | 2022-10-02     | SC         |        4218400 |              83615 | senador          |               14 | PTB             |                 023539820981 |           240001644895 |                142 | nao eleito  |    1458 |
|  2022 |       1 |          546 | eleicao ordinaria | 2022-10-02     | SC         |        4215075 |              80560 | deputado federal |               40 | PSB             |                 035319590930 |           240001647248 |               4078 | nao eleito  |       0 |
|  2022 |       1 |          546 | eleicao ordinaria | 2022-10-02     | SC         |        4210506 |              82058 | deputado federal |               15 | MDB             |                 005506780965 |           240001602678 |               1555 | suplente    |      13 |
|  2022 |       1 |          546 | eleicao ordinaria | 2022-10-02     | SC         |        4206504 |              81272 | deputado federal |               18 | REDE            |                 174375210124 |           240001610083 |               1800 | nao eleito  |       1 |
|  2022 |       1 |          546 | eleicao ordinaria | 2022-10-02     | SC         |        4213401 |              82635 | deputado federal |               70 | AVANTE          |                 036358830957 |           240001602982 |               7077 | nao eleito  |       3 |

### eleicoes22.votacao_partido_munzona_2022_sc

- Estimated rows: 0
- Columns: 38 (showing first 30)
- Size (heap): 8.23 MB
- Size (indexes): 0 B
- Size (total): 8.23 MB

```sql
CREATE TABLE "eleicoes22"."votacao_partido_munzona_2022_sc" (
  "dt_geracao" text,
  "hh_geracao" text,
  "ano_eleicao" integer,
  "cd_tipo_eleicao" integer,
  "nm_tipo_eleicao" text,
  "nr_turno" integer,
  "cd_eleicao" integer,
  "ds_eleicao" text,
  "dt_eleicao" text,
  "tp_abrangencia" text,
  "sg_uf" text,
  "sg_ue" text,
  "nm_ue" text,
  "cd_municipio" integer,
  "nm_municipio" text,
  "nr_zona" integer,
  "cd_cargo" integer,
  "ds_cargo" text,
  "tp_agremiacao" text,
  "nr_partido" integer,
  "sg_partido" text,
  "nm_partido" text,
  "nr_federacao" text,
  "nm_federacao" text,
  "sg_federacao" text,
  "ds_composicao_federacao" text,
  "sq_coligacao" text,
  "nm_coligacao" text,
  "ds_composicao_coligacao" text,
  "st_voto_em_transito" text

);

-- NOTE: Column list truncated to first 30 columns.
```

**Sample (5 rows, first 30 columns):**

| dt_geracao   | hh_geracao   |   ano_eleicao |   cd_tipo_eleicao | nm_tipo_eleicao   |   nr_turno |   cd_eleicao | ds_eleicao                     | dt_eleicao   | tp_abrangencia   | sg_uf   | sg_ue   | nm_ue          |   cd_municipio | nm_municipio   |   nr_zona |   cd_cargo | ds_cargo          | tp_agremiacao   |   nr_partido | sg_partido   | nm_partido                     |   nr_federacao | nm_federacao        | sg_federacao   | ds_composicao_federacao   |   sq_coligacao | nm_coligacao    | ds_composicao_coligacao        | st_voto_em_transito   |
|:-------------|:-------------|--------------:|------------------:|:------------------|-----------:|-------------:|:-------------------------------|:-------------|:-----------------|:--------|:--------|:---------------|---------------:|:---------------|----------:|-----------:|:------------------|:----------------|-------------:|:-------------|:-------------------------------|---------------:|:--------------------|:---------------|:--------------------------|---------------:|:----------------|:-------------------------------|:----------------------|
| 19/10/2025   | 03:30:43     |          2022 |                 2 | Eleição Ordinária |          2 |          547 | Eleições Gerais Estaduais 2022 | 30/10/2022   | E                | SC      | SC      | SANTA CATARINA |          83356 | SÃO LUDGERO    |        44 |          3 | Governador        | Partido isolado |           22 | PL           | Partido Liberal                |             -1 | #NULO#              | #NULO#         | #NULO#                    |   240001681558 | PARTIDO ISOLADO | PL                             | N                     |
| 19/10/2025   | 03:30:43     |          2022 |                 2 | Eleição Ordinária |          1 |          546 | Eleições Gerais Estaduais 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          83674 | TUBARÃO        |        99 |          6 | Deputado Federal  | Federação       |           18 | REDE         | Rede Sustentabilidade          |              3 | Federação PSOL REDE | PSOL/REDE      | PSOL / REDE               |   240001681489 | FEDERAÇÃO       | Federação PSOL REDE(PSOL/REDE) | N                     |
| 19/10/2025   | 03:30:43     |          2022 |                 2 | Eleição Ordinária |          1 |          546 | Eleições Gerais Estaduais 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          81639 | ITAPEMA        |        91 |          7 | Deputado Estadual | Federação       |           50 | PSOL         | Partido Socialismo e Liberdade |              3 | Federação PSOL REDE | PSOL/REDE      | PSOL / REDE               |   240001681488 | FEDERAÇÃO       | Federação PSOL REDE(PSOL/REDE) | N                     |
| 19/10/2025   | 03:30:43     |          2022 |                 2 | Eleição Ordinária |          1 |          546 | Eleições Gerais Estaduais 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          80233 | ANTÔNIO CARLOS |         2 |          6 | Deputado Federal  | Partido isolado |           19 | PODE         | Podemos                        |             -1 | #NULO#              | #NULO#         | #NULO#                    |   240001681541 | PARTIDO ISOLADO | PODE                           | N                     |
| 19/10/2025   | 03:30:43     |          2022 |                 2 | Eleição Ordinária |          1 |          546 | Eleições Gerais Estaduais 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          80918 | CUNHA PORÃ     |        83 |          7 | Deputado Estadual | Partido isolado |           30 | NOVO         | Partido Novo                   |             -1 | #NULO#              | #NULO#         | #NULO#                    |   240001680942 | PARTIDO ISOLADO | NOVO                           | N                     |

### eleicoes22.votacao_secao_2022_sc

- Estimated rows: 2144634
- Columns: 26 (showing first 26)
- Size (heap): 678.59 MB
- Size (indexes): 0 B
- Size (total): 678.59 MB

```sql
CREATE TABLE "eleicoes22"."votacao_secao_2022_sc" (
  "dt_geracao" text,
  "hh_geracao" text,
  "ano_eleicao" integer,
  "cd_tipo_eleicao" integer,
  "nm_tipo_eleicao" text,
  "nr_turno" integer,
  "cd_eleicao" integer,
  "ds_eleicao" text,
  "dt_eleicao" text,
  "tp_abrangencia" text,
  "sg_uf" text,
  "sg_ue" text,
  "nm_ue" text,
  "cd_municipio" text,
  "nm_municipio" text,
  "nr_zona" text,
  "nr_secao" text,
  "cd_cargo" text,
  "ds_cargo" text,
  "nr_votavel" text,
  "nm_votavel" text,
  "qt_votos" text,
  "nr_local_votacao" text,
  "sq_candidato" text,
  "nm_local_votacao" text,
  "ds_local_votacao_endereco" text

);
```

**Sample (5 rows, first 26 columns):**

| dt_geracao   | hh_geracao   |   ano_eleicao |   cd_tipo_eleicao | nm_tipo_eleicao   |   nr_turno |   cd_eleicao | ds_eleicao                     | dt_eleicao   | tp_abrangencia   | sg_uf   | sg_ue   | nm_ue          |   cd_municipio | nm_municipio   |   nr_zona |   nr_secao |   cd_cargo | ds_cargo          |   nr_votavel | nm_votavel                     |   qt_votos |   nr_local_votacao |   sq_candidato | nm_local_votacao                   | ds_local_votacao_endereco            |
|:-------------|:-------------|--------------:|------------------:|:------------------|-----------:|-------------:|:-------------------------------|:-------------|:-----------------|:--------|:--------|:---------------|---------------:|:---------------|----------:|-----------:|-----------:|:------------------|-------------:|:-------------------------------|-----------:|-------------------:|---------------:|:-----------------------------------|:-------------------------------------|
| 01/11/2022   | 16:05:25     |          2022 |                 2 | ELEIÇÃO ORDINÁRIA |          1 |          546 | ELEIÇÕES GERAIS ESTADUAIS 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          83674 | TUBARÃO        |        99 |        135 |          7 | DEPUTADO ESTADUAL |        44117 | MARIA CRISTINA CORREA CLEMENTE |          3 |               1015 |   240001616209 | E.E.B. HENRIQUE FONTES             | RUA DUQUE DE CAXIAS, 700             |
| 01/11/2022   | 16:05:25     |          2022 |                 2 | ELEIÇÃO ORDINÁRIA |          1 |          546 | ELEIÇÕES GERAIS ESTADUAIS 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          80284 | SERRA ALTA     |        83 |         93 |          7 | DEPUTADO ESTADUAL |        19369 | CAMILO NAZARENO PAGANI MARTINS |         11 |               1023 |   240001610835 | ESCOLA DE EDUCAÇÃO BÁSICA LA SALLE | RUA ALMIRANTE BARROSO, N. 571        |
| 01/11/2022   | 16:05:25     |          2022 |                 2 | ELEIÇÃO ORDINÁRIA |          1 |          546 | ELEIÇÕES GERAIS ESTADUAIS 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          81515 | IPUMIRIM       |        90 |         64 |          3 | GOVERNADOR        |           95 | VOTO BRANCO                    |         16 |               1228 |             -1 | ESCOLA DE LINHA SÃO RAFAEL         | ESTRADA GERAL, S/N                   |
| 01/11/2022   | 16:05:25     |          2022 |                 2 | ELEIÇÃO ORDINÁRIA |          1 |          546 | ELEIÇÕES GERAIS ESTADUAIS 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          81590 | ITAIÓPOLIS     |        38 |        103 |          7 | DEPUTADO ESTADUAL |        15655 | FERNANDO KRELLING              |         12 |               1040 |   240001605919 | EEB SÃO JOÃO BATISTA               | RUA ANITA RUTHES ANDRZEJEWSKI, N. 48 |
| 01/11/2022   | 16:05:25     |          2022 |                 2 | ELEIÇÃO ORDINÁRIA |          1 |          546 | ELEIÇÕES GERAIS ESTADUAIS 2022 | 02/10/2022   | E                | SC      | SC      | SANTA CATARINA |          82678 | PORTO UNIÃO    |        25 |        154 |          3 | GOVERNADOR        |           10 | CARLOS MOISÉS DA SILVA         |         71 |               1104 |   240001610772 | ESCOLA BASICA ANTONIO GONZAGA      | RUA FRANCISCO DE SOUZA BACELAR, 742  |

---

## Views

### eleicoes22.vw_eleicao_votacao_por_secoes

- Columns: 12 (showing first 12)

```sql
CREATE VIEW "eleicoes22"."vw_eleicao_votacao_por_secoes" AS
 SELECT m.id_municipio,
    v.cd_municipio,
    v.nm_municipio,
    v.nr_zona,
    v.nr_secao,
    v.cd_cargo,
    v.ds_cargo,
    v.nr_votavel,
    v.nm_votavel,
    v.qt_votos,
    v.nr_local_votacao,
    v.sq_candidato
   FROM eleicoes22.votacao_secao_2022_sc v
     JOIN eleicoes22.br_bd_diretorios_brasil_municipio m ON v.cd_municipio = m.id_municipio_tse
  WHERE v.cd_cargo = '7'::text;;
```

**Sample (5 rows, first 12 columns):**

|   id_municipio |   cd_municipio | nm_municipio       |   nr_zona |   nr_secao |   cd_cargo | ds_cargo          |   nr_votavel | nm_votavel                    |   qt_votos |   nr_local_votacao |   sq_candidato |
|---------------:|---------------:|:-------------------|----------:|-----------:|-----------:|:------------------|-------------:|:------------------------------|-----------:|-------------------:|---------------:|
|        4207304 |          81434 | IMBITUBA           |        73 |        164 |          7 | DEPUTADO ESTADUAL |        50420 | ZELIZE FERNANDA SCHENEKEMBERG |          1 |               1112 |   240001610067 |
|        4209102 |          81795 | JOINVILLE          |        76 |        765 |          7 | DEPUTADO ESTADUAL |        12444 | LUIZ FERNANDO ALONSO DE CYSNE |          4 |               1031 |   240001644406 |
|        4212809 |          82511 | BALNEÁRIO PIÇARRAS |        68 |        131 |          7 | DEPUTADO ESTADUAL |           96 | VOTO NULO                     |         11 |               1015 |             -1 |
|        4202404 |          80470 | BLUMENAU           |        88 |        207 |          7 | DEPUTADO ESTADUAL |        11677 | ALMIR VIEIRA                  |         11 |               1066 |   240001644761 |
|        4204558 |          83950 | CORREIA PINTO      |        93 |         75 |          7 | DEPUTADO ESTADUAL |        22444 | CARLOS HUMBERTO METZNER SILVA |          2 |               1074 |   240001614337 |

### eleicoes22.vw_indicador_nivel_socioeconomico_municipio_agregado

- Columns: 17 (showing first 17)

```sql
CREATE VIEW "eleicoes22"."vw_indicador_nivel_socioeconomico_municipio_agregado" AS
 SELECT id_municipio,
    nome,
    quantidade_alunos_inse,
    rede,
    desc_rede,
    tipo_localizacao,
    desc_tipo_localizacao,
    inse,
    percentual_nivel,
    percentual_nivel_2,
    percentual_nivel_3,
    percentual_nivel_4,
    percentual_nivel_5,
    percentual_nivel_6,
    percentual_nivel_7,
    percentual_nivel_8,
    sigla_uf
   FROM eleicoes22.vw_indicador_nivel_socioeconomico_municipio_raw
  WHERE rede = '0'::text AND tipo_localizacao = '0'::text;;
```

**Sample (5 rows, first 17 columns):**

|   id_municipio | nome                       |   quantidade_alunos_inse |   rede | desc_rede                                      |   tipo_localizacao | desc_tipo_localizacao   |   inse |   percentual_nivel |   percentual_nivel_2 |   percentual_nivel_3 |   percentual_nivel_4 |   percentual_nivel_5 |   percentual_nivel_6 |   percentual_nivel_7 |   percentual_nivel_8 | sigla_uf   |
|---------------:|:---------------------------|-------------------------:|-------:|:-----------------------------------------------|-------------------:|:------------------------|-------:|-------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|:-----------|
|        4200903 | Angelina                   |                      145 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  0 | Total (Urbana e Rural)  |   5.68 |               0    |                 1.65 |                 3.83 |                11.38 |                24.5  |                25.01 |                28.67 |                 4.97 | SC         |
|        4204608 | Criciúma                   |                     4918 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  0 | Total (Urbana e Rural)  |   5.97 |               0.06 |                 0.75 |                 2.71 |                 7.34 |                17.55 |                23.47 |                36.11 |                12.01 | SC         |
|        4201257 | Apiúna                     |                      244 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  0 | Total (Urbana e Rural)  |   5.49 |               0.35 |                 1.15 |                 5.72 |                12.28 |                31.79 |                28.66 |                18.02 |                 2.03 | SC         |
|        4213906 | Presidente Castello Branco |                       50 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  0 | Total (Urbana e Rural)  |   5.49 |               0    |                 0    |                 1.75 |                14.68 |                36.82 |                32.81 |                13.93 |                 0    | SC         |
|        4207684 | Ipuaçu                     |                      100 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  0 | Total (Urbana e Rural)  |   5.36 |               0    |                 2.28 |                11.72 |                11.04 |                35.15 |                23.87 |                15.67 |                 0.28 | SC         |

### eleicoes22.vw_indicador_nivel_socioeconomico_municipio_segmentado

- Columns: 17 (showing first 17)

```sql
CREATE VIEW "eleicoes22"."vw_indicador_nivel_socioeconomico_municipio_segmentado" AS
 SELECT id_municipio,
    nome,
    quantidade_alunos_inse,
    rede,
    desc_rede,
    tipo_localizacao,
    desc_tipo_localizacao,
    inse,
    percentual_nivel,
    percentual_nivel_2,
    percentual_nivel_3,
    percentual_nivel_4,
    percentual_nivel_5,
    percentual_nivel_6,
    percentual_nivel_7,
    percentual_nivel_8,
    sigla_uf
   FROM eleicoes22.vw_indicador_nivel_socioeconomico_municipio_raw
  WHERE NOT desc_rede ~~* 'total%'::text AND NOT tipo_localizacao = '0'::text;;
```

**Sample (5 rows, first 17 columns):**

|   id_municipio | nome               |   quantidade_alunos_inse |   rede | desc_rede   |   tipo_localizacao | desc_tipo_localizacao   |   inse | percentual_nivel   | percentual_nivel_2   | percentual_nivel_3   | percentual_nivel_4   | percentual_nivel_5   | percentual_nivel_6   | percentual_nivel_7   | percentual_nivel_8   | sigla_uf   |
|---------------:|:-------------------|-------------------------:|-------:|:------------|-------------------:|:------------------------|-------:|:-------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:-----------|
|        4209201 | Lacerdópolis       |                       23 |      3 | Municipal   |                  1 | Urbana                  |   5.46 | 0                  | 4.36                 | 4.33                 | 8.7                  | 39.15                | 21.73                | 17.39                | 4.33                 | SC         |
|        4212809 | Balneário Piçarras |                        0 |      1 | Federal     |                  1 | Urbana                  |   0    |                    |                      |                      |                      |                      |                      |                      |                      | SC         |
|        4207650 | Iporã do Oeste     |                       41 |      2 | Estadual    |                  2 | Rural                   |   5.45 | 0                  | 2.48                 | 2.27                 | 24.41                | 23.67                | 32.35                | 7.67                 | 7.14                 | SC         |
|        4205159 | Doutor Pedrinho    |                        0 |      1 | Federal     |                  1 | Urbana                  |   0    |                    |                      |                      |                      |                      |                      |                      |                      | SC         |
|        4205209 | Erval Velho        |                       86 |      2 | Estadual    |                  1 | Urbana                  |   5.51 | 0                  | 0                    | 7.91                 | 15.24                | 28.88                | 18.53                | 29.44                | 0                    | SC         |

---

## Materialized Views

### eleicoes22.vw_diretorio_municipio_e_geom

- Estimated rows: 5570
- Columns: 0 (showing first 23)
- Size (heap): 25.55 MB
- Size (indexes): 0 B
- Size (total): 25.55 MB

```sql
CREATE MATERIALIZED VIEW "eleicoes22"."vw_diretorio_municipio_e_geom" AS
 SELECT dbm.id_municipio,
    dbm.nome,
    dbm.sigla_uf,
    dbm.capital_uf,
    dbm.id_comarca,
    dbm.id_regiao_saude,
    dbm.nome_regiao_saude,
    dbm.id_regiao_imediata,
    dbm.nome_regiao_imediata,
    dbm.id_regiao_intermediaria,
    dbm.nome_regiao_intermediaria,
    dbm.id_microrregiao,
    dbm.nome_microrregiao,
    dbm.id_mesorregiao,
    dbm.nome_mesorregiao,
    dbm.id_regiao_metropolitana,
    dbm.nome_regiao_metropolitana,
    dbm.ddd,
    dbm.amazonia_legal,
    dbm.id_municipio_tse,
    dbm.id_municipio_rf,
    dbm.id_municipio_bcb,
    br_geobr_mapas_municipio.geometria
   FROM eleicoes22.br_geobr_mapas_municipio
     JOIN eleicoes22.br_bd_diretorios_brasil_municipio dbm ON br_geobr_mapas_municipio.id_municipio = dbm.id_municipio;;
```

**Sample (5 rows, first 23 columns):**

|   id_municipio | nome              | sigla_uf   |   capital_uf |   id_comarca |   id_regiao_saude | nome_regiao_saude                       |   id_regiao_imediata | nome_regiao_imediata         |   id_regiao_intermediaria | nome_regiao_intermediaria   |   id_microrregiao | nome_microrregiao   |   id_mesorregiao | nome_mesorregiao              | id_regiao_metropolitana   | nome_regiao_metropolitana            |   ddd |   amazonia_legal |   id_municipio_tse |   id_municipio_rf |   id_municipio_bcb | geometria                                                                                                                |
|---------------:|:------------------|:-----------|-------------:|-------------:|------------------:|:----------------------------------------|---------------------:|:-----------------------------|--------------------------:|:----------------------------|------------------:|:--------------------|-----------------:|:------------------------------|:--------------------------|:-------------------------------------|------:|-----------------:|-------------------:|------------------:|-------------------:|:-------------------------------------------------------------------------------------------------------------------------|
|        2905503 | Caldeirão Grande  | BA         |            0 |      2905503 |             29014 | Jacobina                                |               290030 | Jacobina                     |                      2910 | Feira de Santana            |             29010 | Jacobina            |             2903 | Centro Norte Baiano           |                           |                                      |    74 |                0 |              34096 |              3409 |               1023 | POLYGON((-40.231592542 -10.925447785,-40.247687914 -10.910568158,-40.250179465 -10.913698988,-40.28308464 -10.934985143… |
|        4211892 | Painel            | SC         |            0 |      4209300 |             42013 | Serra Catarinense                       |               420005 | Lages                        |                      4203 | Lages                       |             42010 | Campos de Lages     |             4203 | Serrana                       | 6601                      | Região Metropolitana de Lages        |    49 |                0 |              81264 |               930 |              54348 | POLYGON((-50.003666256 -27.796283702,-50.005497328 -27.797924385,-50.006072659 -27.801584449,-50.010610806 -27.80249998… |
|        4304689 | Capela de Santana | RS         |            0 |      4314803 |             43008 | Região 08 - Vale do Caí e Metropolitana |               430002 | Novo Hamburgo - São Leopoldo |                      4301 | Porto Alegre                |             43023 | Montenegro          |             4305 | Metropolitana de Porto Alegre | 7401                      | Região Metropolitana de Porto Alegre |    51 |                0 |              84891 |              8443 |              45247 | POLYGON((-51.338139751 -29.634241105,-51.349053424 -29.638818268,-51.350839242 -29.6409259,-51.352307409 -29.638523338,… |
|        4322806 | Veranópolis       | RS         |            0 |      4322806 |             43025 | Região 25 - Vinhedos e Basalto          |               430037 | Bento Gonçalves              |                      4307 | Caxias do Sul               |             43016 | Caxias do Sul       |             4302 | Nordeste Rio-grandense        |                           |                                      |    54 |                0 |              89591 |              8959 |               2613 | POLYGON((-51.533020691 -28.887220927,-51.534247715 -28.878862922,-51.559457436 -28.879809361,-51.559410131 -28.89182513… |
|        3134301 | Itumirim          | MG         |            0 |      3134301 |             31004 | Lavras                                  |               310043 | Lavras                       |                      3108 | Varginha                    |             31057 | Lavras              |             3111 | Campo das Vertentes           |                           |                                      |    35 |                0 |              46850 |              4685 |              35965 | POLYGON((-44.863395 -21.166666996,-44.86671 -21.170993996,-44.86608 -21.171991996,-44.862997 -21.170815996,-44.867658 -… |

### eleicoes22.vw_eleicao_votacao_agg_por_municipio

- Estimated rows: 59179
- Columns: 0 (showing first 7)
- Size (heap): 7.04 MB
- Size (indexes): 0 B
- Size (total): 7.04 MB

```sql
CREATE MATERIALIZED VIEW "eleicoes22"."vw_eleicao_votacao_agg_por_municipio" AS
 WITH base AS (
         SELECT v.id_municipio,
            v.cd_municipio,
            v.nm_municipio,
            v.nr_zona,
            v.nr_secao,
            v.cd_cargo,
            v.ds_cargo,
            v.nr_votavel,
            v.nm_votavel,
            v.sq_candidato,
            v.qt_votos::integer AS qt_votos
           FROM eleicoes22.vw_eleicao_votacao_por_secoes v
        )
 SELECT id_municipio,
    nm_municipio,
    sum(qt_votos) AS qt_votos,
    nr_votavel,
    nm_votavel,
    sq_candidato,
    ds_cargo
   FROM base
  GROUP BY id_municipio, nm_municipio, ds_cargo, nr_votavel, nm_votavel, sq_candidato
  ORDER BY id_municipio, nm_municipio, (sum(qt_votos)) DESC, nm_votavel;;
```

**Sample (5 rows, first 7 columns):**

|   id_municipio | nm_municipio   |   qt_votos |   nr_votavel | nm_votavel                   |   sq_candidato | ds_cargo          |
|---------------:|:---------------|-----------:|-------------:|:-----------------------------|---------------:|:------------------|
|        4217402 | SCHROEDER      |          3 |        30999 | ORIDES DOS SANTOS NETO       |   240001597556 | DEPUTADO ESTADUAL |
|        4211751 | OTACÍLIO COSTA |          1 |        13333 | LINO FERNANDO BRAGANÇA PERES |   240001679656 | DEPUTADO ESTADUAL |
|        4202404 | BLUMENAU       |          5 |        10111 | VALDENIR DA SILVA            |   240001610206 | DEPUTADO ESTADUAL |
|        4206405 | GUARACIABA     |          4 |        19111 | THIAGO DA SILVA MORASTONI    |   240001610826 | DEPUTADO ESTADUAL |
|        4204251 | COCAL DO SUL   |          9 |        13131 | MATHEUS ROETGER MADEIRA      |   240001679631 | DEPUTADO ESTADUAL |

### eleicoes22.vw_indicador_nivel_socioeconomico_municipio_raw

- Estimated rows: 5310
- Columns: 0 (showing first 17)
- Size (heap): 880 KB
- Size (indexes): 0 B
- Size (total): 880 KB

```sql
CREATE MATERIALIZED VIEW "eleicoes22"."vw_indicador_nivel_socioeconomico_municipio_raw" AS
 WITH rede_dict AS (
         SELECT t.cod_rede,
            t.ano,
            t.desc_rede
           FROM ( VALUES (0,2021,'Total (Federal, Estadual, Municipal e Privada)'::text), (1,2021,'Federal'::text), (2,2021,'Estadual'::text), (3,2021,'Municipal'::text), (4,2021,'Privada'::text), (5,2021,'Total (Estadual e Municipal)'::text), (6,2021,'Total (Federal, Estadual e Municipal)'::text)) t(cod_rede, ano, desc_rede)
        ), tipo_loc_dict AS (
         SELECT t.cod_tipo_localizacao,
            t.ano,
            t.desc_tipo_localizacao
           FROM ( VALUES (0,2021,'Total (Urbana e Rural)'::text), (1,2021,'Urbana'::text), (2,2021,'Rural'::text)) t(cod_tipo_localizacao, ano, desc_tipo_localizacao)
        )
 SELECT b.id_municipio,
    m.nome,
    b.quantidade_alunos_inse,
    b.rede,
    r.desc_rede,
    b.tipo_localizacao,
    tl.desc_tipo_localizacao,
    b.inse,
    b.percentual_nivel,
    b.percentual_nivel_2,
    b.percentual_nivel_3,
    b.percentual_nivel_4,
    b.percentual_nivel_5,
    b.percentual_nivel_6,
    b.percentual_nivel_7,
    b.percentual_nivel_8,
    m.sigla_uf
   FROM eleicoes22.br_inep_indicador_nivel_socioeconomico_municipio b
     LEFT JOIN rede_dict r ON r.ano = b.ano AND r.cod_rede = NULLIF(b.rede, ''::text)::integer
     LEFT JOIN tipo_loc_dict tl ON tl.ano = b.ano AND tl.cod_tipo_localizacao = NULLIF(b.tipo_localizacao, ''::text)::integer
     LEFT JOIN eleicoes22.br_bd_diretorios_brasil_municipio m ON b.id_municipio = m.id_municipio
  WHERE b.sigla_uf = 'SC'::text AND b.ano = 2021
  ORDER BY b.id_municipio, b.sigla_uf, b.rede, b.tipo_localizacao;;
```

**Sample (5 rows, first 17 columns):**

|   id_municipio | nome                   |   quantidade_alunos_inse |   rede | desc_rede                                      |   tipo_localizacao | desc_tipo_localizacao   |   inse | percentual_nivel   | percentual_nivel_2   | percentual_nivel_3   | percentual_nivel_4   | percentual_nivel_5   | percentual_nivel_6   | percentual_nivel_7   | percentual_nivel_8   | sigla_uf   |
|---------------:|:-----------------------|-------------------------:|-------:|:-----------------------------------------------|-------------------:|:------------------------|-------:|:-------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:---------------------|:-----------|
|        4211405 | Nova Erechim           |                        0 |      5 | Total (Estadual e Municipal)                   |                  2 | Rural                   |   0    |                    |                      |                      |                      |                      |                      |                      |                      | SC         |
|        4217253 | São Pedro de Alcântara |                        0 |      5 | Total (Estadual e Municipal)                   |                  2 | Rural                   |   0    |                    |                      |                      |                      |                      |                      |                      |                      | SC         |
|        4204905 | Descanso               |                        0 |      1 | Federal                                        |                  0 | Total (Urbana e Rural)  |   0    |                    |                      |                      |                      |                      |                      |                      |                      | SC         |
|        4218756 | Tunápolis              |                       11 |      0 | Total (Federal, Estadual, Municipal e Privada) |                  2 | Rural                   |   5.69 | 0                  | 0                    | 0                    | 27.27                | 18.18                | 18.18                | 27.27                | 9.09                 | SC         |
|        4215059 | Rio Rufino             |                       17 |      5 | Total (Estadual e Municipal)                   |                  2 | Rural                   |   5.01 | 0                  | 6.8                  | 17.01                | 20.41                | 43.54                | 0                    | 12.24                | 0                    | SC         |

---
