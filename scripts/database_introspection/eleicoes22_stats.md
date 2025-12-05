# Statistical profile for `eleicoes22`

- Generated at: 2025-10-30 22:17:39
- Database: gis @ localhost:5434
- Tables discovered: 12
- Tables profiled: up to 30 (cap)
- Ignored tables: br_bd_diretorios_brasil_setor_censitario, br_geobr_mapas_limite_vizinhanca, br_ibge_censo_2022_setor_censitario_sc, ignore_detalhe_votacao_munzona_2022_sc, ignore_detalhe_votacao_secao_2022_sc, ignore_eleitorado_local_votacao, ignore_perfil_eleitor_secao_2022_sc, votacao_partido_munzona_2022_sc
- Columns per table considered: up to 30 (geometry/geography skipped; id_* and *_id skipped)
- Outliers = Tukey fences (Q1−1.5·IQR, Q3+1.5·IQR)
- Fast mode: False (limit=13)
- SHOW_SQL: False
- SHOW_HIST: True (bins=10, max columns=10)
- Numeric low-cardinality heuristic: distinct ≤ 20 or distinct/non_null ≤ 1.00%

## Table of Contents

<!-- toc -->
<!--stop reading eleicoes22_stats.md: probably a binary file-->
<!-- tocstop -->

---

## 1. br_bd_diretorios_brasil_distrito

_Skipped ID-like columns (id_*, *_id):_ `id_distrito, id_municipio`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| nome | 10283 | 0 | 0 | 8890 |
| sigla_uf | 10283 | 0 | 0 | 27 |

**Top-5 values for `nome`**

| value         |   cnt |
|:--------------|------:|
| São José      |    17 |
| Santo Antônio |    14 |
| Bela Vista    |    12 |
| São Pedro     |    11 |
| Boa Esperança |    10 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |  1633 |
| RS      |  1231 |
| SP      |  1036 |
| BA      |   844 |
| CE      |   839 |

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.007272 |
| numeric_aggregates | 0 |
| categoricals_total | 0.11286 |
| histograms_total | 0 |
| table_total | 0.131692 |

---

## 2. br_bd_diretorios_brasil_municipio

_Skipped ID-like columns (id_*, *_id):_ `id_municipio, id_municipio_2, id_municipio_tse, id_municipio_rf, id_municipio_bcb, id_comarca, id_regiao_saude, id_regiao_imediata, id_regiao_intermediaria, id_microrregiao, id_mesorregiao, id_regiao_metropolitana, id_uf`

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazonia_legal | 5571 | 0 | 0 | 2 | 0.13875426314844733 | 0.3456899153961231 | 0 | 0 | 0 | 0 | 1 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| amazonia_legal | 0 | 0 | 773 | 0.009171 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| nome | 5571 | 0 | 0 | 5298 |
| capital_uf | 5570 | 1 | 0.018 | 2 |
| nome_regiao_saude | 5570 | 1 | 0.018 | 440 |
| nome_regiao_imediata | 5571 | 0 | 0 | 508 |
| nome_regiao_intermediaria | 5571 | 0 | 0 | 133 |
| nome_microrregiao | 5570 | 1 | 0.018 | 554 |
| nome_mesorregiao | 5570 | 1 | 0.018 | 137 |
| nome_regiao_metropolitana | 1432 | 4139 | 74.2955 | 86 |
| ddd | 5570 | 1 | 0.018 | 67 |
| sigla_uf | 5571 | 0 | 0 | 27 |
| nome_uf | 5571 | 0 | 0 | 27 |
| nome_regiao | 5571 | 0 | 0 | 5 |

**Top-5 values for `nome`**

| value        |   cnt |
|:-------------|------:|
| Bom Jesus    |     5 |
| São Domingos |     5 |
| Bonito       |     4 |
| Planalto     |     4 |
| Santa Helena |     4 |

**Top-5 values for `capital_uf`**

| value   |   cnt |
|:--------|------:|
| 0       |  5543 |
| 1       |    27 |
|         |     1 |

**Top-5 values for `nome_regiao_saude`**

| value                               |   cnt |
|:------------------------------------|------:|
| Central                             |    58 |
| Sul                                 |    44 |
| Vale do Rio Guaribas                |    42 |
| 6ª Região de Saúde - Pau dos Ferros |    37 |
| Norte                               |    35 |

**Top-5 values for `nome_regiao_imediata`**

| value                 |   cnt |
|:----------------------|------:|
| Campina Grande        |    47 |
| São Paulo             |    39 |
| São José do Rio Preto |    36 |
| Pau dos Ferros        |    34 |
| Pouso Alegre          |    34 |

**Top-5 values for `nome_regiao_intermediaria`**

| value        |   cnt |
|:-------------|------:|
| Juíz de Fora |   146 |
| Passo Fundo  |   144 |
| Maringá      |   115 |
| Chapecó      |   109 |
| Cascavel     |   100 |

**Top-5 values for `nome_microrregiao`**

| value              |   cnt |
|:-------------------|------:|
| Ilhéus-Itabuna     |    41 |
| Alto Médio Canindé |    39 |
| Chapecó            |    38 |
| Juiz de Fora       |    33 |
| Lajeado-Estrela    |    31 |

**Top-5 values for `nome_mesorregiao`**

| value                  |   cnt |
|:-----------------------|------:|
| Noroeste Rio-grandense |   216 |
| Sul/Sudoeste de Minas  |   146 |
| Zona da Mata           |   142 |
| Centro Sul Baiano      |   118 |
| Oeste Catarinense      |   118 |

**Top-5 values for `nome_regiao_metropolitana`**

| value                                                   |   cnt |
|:--------------------------------------------------------|------:|
|                                                         |  4139 |
| Região Metropolitana do Extremo Oeste                   |    49 |
| Região Metropolitana do Contestado                      |    45 |
| Região Metropolitana do Vale do Paraíba e Litoral Norte |    39 |
| Região Metropolitana de São Paulo                       |    38 |

**Top-5 values for `ddd`**

|   value |   cnt |
|--------:|------:|
|      83 |   223 |
|      33 |   176 |
|      84 |   167 |
|      55 |   160 |
|      35 |   159 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |   853 |
| SP      |   645 |
| RS      |   497 |
| BA      |   417 |
| PR      |   399 |

**Top-5 values for `nome_uf`**

| value             |   cnt |
|:------------------|------:|
| Minas Gerais      |   853 |
| São Paulo         |   645 |
| Rio Grande do Sul |   497 |
| Bahia             |   417 |
| Paraná            |   399 |

**Top-5 values for `nome_regiao`**

| value        |   cnt |
|:-------------|------:|
| Nordeste     |  1794 |
| Sudeste      |  1668 |
| Sul          |  1191 |
| Centro-Oeste |   468 |
| Norte        |   450 |

### Histograms

#### Equal-frequency bins (NTILE)

**amazonia_legal** (bins=10, time 0.007777s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 558 |
| 2 | 0 | 0 | 557 |
| 3 | 0 | 0 | 557 |
| 4 | 0 | 0 | 557 |
| 5 | 0 | 0 | 557 |
| 6 | 0 | 0 | 557 |
| 7 | 0 | 0 | 557 |
| 8 | 0 | 0 | 557 |
| 9 | 0 | 1 | 557 |
| 10 | 1 | 1 | 557 |

#### Fixed-width bins (width_bucket)

**amazonia_legal** (categorical-like, top-10) — time 0.003844s

```


████████████████████████████████████████████████████████████████     4.80K    0
██████████                                                          773.00    1
```


`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001813 |
| numeric_aggregates | 0.038854 |
| categoricals_total | 0.11415 |
| histograms_total | 0.01162 |
| table_total | 0.184582 |

---

## 3. br_geobr_mapas_municipio

_Skipped ID-like columns (id_*, *_id):_ `id_municipio`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 5570 | 0 | 0 | 27 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |   853 |
| SP      |   645 |
| RS      |   497 |
| BA      |   417 |
| PR      |   399 |

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001133 |
| numeric_aggregates | 0 |
| categoricals_total | 0.266204 |
| histograms_total | 0 |
| table_total | 0.268154 |

---

## 4. br_geobr_mapas_regiao

_Skipped ID-like columns (id_*, *_id):_ `id_regiao`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| nome_regiao | 5 | 0 | 0 | 5 |

**Top-5 values for `nome_regiao`** — _All non-null values are distinct; omitting list._

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001466 |
| numeric_aggregates | 0 |
| categoricals_total | 0.007637 |
| histograms_total | 0 |
| table_total | 0.009286 |

---

## 5. br_geobr_mapas_regiao_imediata

_Skipped ID-like columns (id_*, *_id):_ `id_uf, id_regiao_imediata`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 510 | 0 | 0 | 27 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |    70 |
| SP      |    53 |
| RS      |    43 |
| BA      |    34 |
| PR      |    29 |

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001124 |
| numeric_aggregates | 0 |
| categoricals_total | 0.010039 |
| histograms_total | 0 |
| table_total | 0.011934 |

---

## 6. br_geobr_mapas_regiao_intermediaria

_Skipped ID-like columns (id_*, *_id):_ `id_uf, id_regiao_intermediaria`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 135 | 0 | 0 | 27 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |    13 |
| SP      |    11 |
| BA      |    10 |
| RS      |    10 |
| PA      |     7 |

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001373 |
| numeric_aggregates | 0 |
| categoricals_total | 0.006665 |
| histograms_total | 0 |
| table_total | 0.008816 |

---

## 7. br_ibge_censo_2022_municipio

_Skipped ID-like columns (id_*, *_id):_ `id_municipio`

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| domicilios | 5570 | 0 | 0 | 4366 | 13008.324596050268 | 77531.26351125 | 322 | 1876 | 3883 | 8375 | 4307665 |
| populacao | 5570 | 0 | 0 | 5042 | 36280.614003590665 | 205463.59934643 | 829 | 5201 | 11021 | 24297 | 11395157 |
| area | 5570 | 0 | 0 | 2063 | 1525.553500897666 | 5604.915413634342 | 4 | 205 | 418 | 1027 | 159533 |
| taxa_alfabetizacao | 5570 | 0 | 0 | 4903 | 0.8819973141831238 | 0.07560106979192845 | 0.63186 | 0.82041 | 0.9062 | 0.94437 | 0.99096 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| domicilios | -7872.5 | 18123.5 | 618 | 0.004085 |
| populacao | -23443 | 52941 | 606 | 0.00362 |
| area | -1028 | 2260 | 665 | 0.003353 |
| taxa_alfabetizacao | 0.6344699999999999 | 1.1303100000000001 | 1 | 0.003566 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 5570 | 0 | 0 | 27 |
| idade_mediana | 5570 | 0 | 0 | 38 |
| razao_sexo | 5570 | 0 | 0 | 1973 |
| indice_envelhecimento | 5570 | 0 | 0 | 4192 |
| populacao_indigena | 5570 | 0 | 0 | 786 |
| populacao_indigena_terra_indigena | 5570 | 0 | 0 | 350 |
| populacao_quilombola | 5570 | 0 | 0 | 833 |
| populacao_quilombola_territorio_quilombola | 5570 | 0 | 0 | 254 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      |   853 |
| SP      |   645 |
| RS      |   497 |
| BA      |   417 |
| PR      |   399 |

**Top-5 values for `idade_mediana`**

|   value |   cnt |
|--------:|------:|
|      36 |   568 |
|      35 |   565 |
|      37 |   485 |
|      34 |   470 |
|      38 |   458 |

**Top-5 values for `razao_sexo`**

|   value |   cnt |
|--------:|------:|
|  100    |    15 |
|   98.58 |    12 |
|  100.55 |    11 |
|   98.88 |    11 |
|  101.09 |    10 |

**Top-5 values for `indice_envelhecimento`**

|   value |   cnt |
|--------:|------:|
|   36.71 |     5 |
|   43.68 |     5 |
|   48.38 |     5 |
|   50.68 |     5 |
|   58.94 |     5 |

**Top-5 values for `populacao_indigena`**

|   value |   cnt |
|--------:|------:|
|       0 |   770 |
|       1 |   454 |
|       2 |   344 |
|       3 |   281 |
|       4 |   218 |

**Top-5 values for `populacao_indigena_terra_indigena`**

|   value |   cnt |
|--------:|------:|
|       0 |  5187 |
|     102 |     3 |
|     306 |     3 |
|      66 |     3 |
|      79 |     3 |

**Top-5 values for `populacao_quilombola`**

|   value |   cnt |
|--------:|------:|
|       0 |  3908 |
|       1 |    59 |
|       3 |    35 |
|       4 |    35 |
|       2 |    34 |

**Top-5 values for `populacao_quilombola_territorio_quilombola`**

|   value |   cnt |
|--------:|------:|
|       0 |  5272 |
|      56 |     4 |
|     153 |     3 |
|      43 |     3 |
|      82 |     3 |

### Histograms

#### Equal-frequency bins (NTILE)

**domicilios** (bins=10, time 0.005331s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 322 | 1142 | 557 |
| 2 | 1142 | 1618 | 557 |
| 3 | 1619 | 2194 | 557 |
| 4 | 2195 | 2928 | 557 |
| 5 | 2929 | 3883 | 557 |
| 6 | 3884 | 5135 | 557 |
| 7 | 5135 | 7046 | 557 |
| 8 | 7048 | 10383 | 557 |
| 9 | 10419 | 20079 | 557 |
| 10 | 20188 | 4307665 | 557 |

**populacao** (bins=10, time 0.004989s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 829 | 3115 | 557 |
| 2 | 3116 | 4444 | 557 |
| 3 | 4446 | 6108 | 557 |
| 4 | 6110 | 8280 | 557 |
| 5 | 8281 | 11021 | 557 |
| 6 | 11021 | 14669 | 557 |
| 7 | 14683 | 20339 | 557 |
| 8 | 20350 | 30524 | 557 |
| 9 | 30545 | 58608 | 557 |
| 10 | 58883 | 11395157 | 557 |

**area** (bins=10, time 0.005002s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 4 | 114 | 557 |
| 2 | 114 | 175 | 557 |
| 3 | 175 | 236 | 557 |
| 4 | 237 | 314 | 557 |
| 5 | 314 | 418 | 557 |
| 6 | 418 | 576 | 557 |
| 7 | 576 | 827 | 557 |
| 8 | 828 | 1320 | 557 |
| 9 | 1327 | 2730 | 557 |
| 10 | 2736 | 159533 | 557 |

**taxa_alfabetizacao** (bins=10, time 0.005046s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0.63186 | 0.76847 | 557 |
| 2 | 0.76852 | 0.80309 | 557 |
| 3 | 0.80316 | 0.83917 | 557 |
| 4 | 0.83924 | 0.87908 | 557 |
| 5 | 0.87908 | 0.9062 | 557 |
| 6 | 0.90621 | 0.92375 | 557 |
| 7 | 0.92376 | 0.93817 | 557 |
| 8 | 0.93821 | 0.95133 | 557 |
| 9 | 0.95134 | 0.96499 | 557 |
| 10 | 0.96509 | 0.99096 | 557 |

#### Fixed-width bins (width_bucket)

**domicilios** (bins=10, time 0.005117s)

```


██████████████████████████████████████████████████    5.56K    [322,431056.3)       
                                                       7.00    [431056.3,861790.6)  
                                                       3.00    [861790.6,1292524.9) 
                                                       1.00    [2153993.5,2584727.8)
```

**populacao** (bins=10, time 0.003806s)

```


██████████████████████████████████████████████████    5.56K    [829,1140261.8)               
                                                       7.00    [1140261.8,2279694.6)         
                                                       4.00    [2279694.6,3419127.4000000004)
                                                       1.00    [5697993,6837425.800000001)   
```

**area** (bins=10, time 0.003719s)

```


██████████████████████████████████████████████████    5.50K    [4,15956.9)        
                                                      45.00    [15956.9,31909.8)  
                                                      11.00    [31909.8,47862.7)  
                                                       7.00    [47862.7,63815.6)  
                                                       5.00    [63815.6,79768.5)  
                                                       2.00    [79768.5,95721.4)  
                                                       2.00    [95721.4,111674.3) 
                                                       1.00    [111674.3,127627.2)
```

**taxa_alfabetizacao** (bins=10, time 0.004114s)

```


                                                        9.00    [0.63186,0.66777)
█                                                      51.00    [0.66777,0.70368)
██████                                                182.00    [0.70368,0.73959)
███████████████                                       426.00    [0.73959,0.7755) 
████████████████████                                  583.00    [0.7755,0.81141) 
██████████████████                                    536.00    [0.81141,0.84732)
██████████████████                                    514.00    [0.84732,0.88323)
███████████████████████████████                       897.00    [0.88323,0.91914)
██████████████████████████████████████████████████     1.42K    [0.91914,0.95505)
█████████████████████████████████                     954.00    [0.95505,0.99096)
```

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.002339 |
| numeric_aggregates | 0.026653 |
| categoricals_total | 0.071861 |
| histograms_total | 0.037124 |
| table_total | 0.161947 |

---

## 8. br_ibge_censo_2022_populacao_idade_sexo

_Skipped ID-like columns (id_*, *_id):_ `id_municipio`

_No numeric columns considered._

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| forma_declaracao_idade | 2495360 | 0 | 0 | 2 |
| sexo | 2495360 | 0 | 0 | 2 |
| idade | 2495360 | 0 | 0 | 112 |
| idade_anos | 2473080 | 22280 | 0.8929 | 110 |
| grupo_idade | 2495360 | 0 | 0 | 21 |
| populacao | 2145409 | 349951 | 14.0241 | 7138 |

**Top-5 values for `forma_declaracao_idade`**

| value              |     cnt |
|:-------------------|--------:|
| Data de nascimento | 1247680 |
| Idade presumida    | 1247680 |

**Top-5 values for `sexo`**

| value    |     cnt |
|:---------|--------:|
| Homens   | 1247680 |
| Mulheres | 1247680 |

**Top-5 values for `idade`**

| value            |   cnt |
|:-----------------|------:|
| 100 anos ou mais | 22280 |
| 10 anos          | 22280 |
| 10 meses         | 22280 |
| 11 anos          | 22280 |
| 11 meses         | 22280 |

**Top-5 values for `idade_anos`**

|     value |   cnt |
|----------:|------:|
| 0         | 44560 |
| 0.0833333 | 22280 |
| 0.166667  | 22280 |
| 0.25      | 22280 |
| 0.333333  | 22280 |

**Top-5 values for `grupo_idade`**

| value        |    cnt |
|:-------------|-------:|
| 0 a 4 anos   | 334200 |
| 10 a 14 anos | 111400 |
| 15 a 19 anos | 111400 |
| 20 a 24 anos | 111400 |
| 25 a 29 anos | 111400 |

**Top-5 values for `populacao`**

| value   |    cnt |
|:--------|-------:|
|         | 349951 |
| 1       | 200876 |
| 2       | 143214 |
| 3       | 109540 |
| 4       |  88098 |

`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.0015 |
| numeric_aggregates | 0 |
| categoricals_total | 14.917443 |
| histograms_total | 0 |
| table_total | 14.926777 |

---

## 9. br_inep_indicador_nivel_socioeconomico_municipio

_Skipped ID-like columns (id_*, *_id):_ `id_municipio`

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ano | 169302 | 0 | 0 | 2 | 2020.174185774533 | 0.9847128088688143 | 2019 | 2019 | 2021 | 2021 | 2021 |
| quantidade_alunos_inse | 169302 | 0 | 0 | 4650 | 487.15104369706205 | 3101.040113940636 | 0 | 34 | 130 | 350 | 277258 |
| inse | 169302 | 0 | 0 | 15451 | 3.9059215827337637 | 1.8530333096252394 | 0 | 4.03 | 4.5 | 5.0977 | 6.72 |
| percentual_nivel | 139922 | 29380 | 17.3536 | 2264 | 2.6762339017452437 | 4.139241555982628 | 0 | 0 | 0.86 | 3.95 | 90.57 |
| percentual_nivel_2 | 139922 | 29380 | 17.3536 | 6176 | 19.746737968295655 | 16.069044740636862 | 0 | 5.38 | 15.39 | 32.62 | 100 |
| percentual_nivel_3 | 139922 | 29380 | 17.3536 | 3839 | 18.334851631623348 | 8.200165265921726 | 0 | 11.88 | 19.14 | 24.46 | 77.78 |
| percentual_nivel_4 | 139922 | 29380 | 17.3536 | 3757 | 20.374357213305323 | 6.649782475702133 | 0 | 16.36 | 20.56 | 24.32 | 100 |
| percentual_nivel_5 | 139922 | 29380 | 17.3536 | 3960 | 18.150717828505023 | 8.86271426129045 | 0 | 10.77 | 18.34 | 25.1 | 80 |
| percentual_nivel_6 | 139922 | 29380 | 17.3536 | 3680 | 12.100730978688338 | 9.02447319028809 | 0 | 4.34 | 10 | 19.1 | 83.33 |
| percentual_nivel_7 | 139922 | 29380 | 17.3536 | 3614 | 7.8908980717829555 | 8.067784532604648 | 0 | 1.59 | 4.95 | 12.49 | 81.82 |
| percentual_nivel_8 | 139922 | 29380 | 17.3536 | 950 | 0.7254100141507444 | 1.3351002786369457 | 0 | 0 | 0.17 | 1.02 | 43.75 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| ano | 2016 | 2024 | 0 | 0.037322 |
| quantidade_alunos_inse | -440 | 824 | 17494 | 0.039679 |
| inse | 2.428450000000001 | 6.699249999999999 | 29382 | 0.030733 |
| percentual_nivel | -5.925000000000001 | 9.875 | 8144 | 0.031317 |
| percentual_nivel_2 | -35.48 | 73.47999999999999 | 86 | 0.031825 |
| percentual_nivel_3 | -6.99 | 43.33 | 412 | 0.03549 |
| percentual_nivel_4 | 4.419999999999998 | 36.260000000000005 | 3518 | 0.035169 |
| percentual_nivel_5 | -10.725000000000005 | 46.595000000000006 | 347 | 0.033323 |
| percentual_nivel_6 | -17.8 | 41.24 | 373 | 0.031264 |
| percentual_nivel_7 | -14.760000000000002 | 28.840000000000003 | 3077 | 0.031641 |
| percentual_nivel_8 | -1.53 | 2.55 | 9165 | 0.03364 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 169302 | 0 | 0 | 27 |
| rede | 169302 | 0 | 0 | 6 |
| tipo_localizacao | 169302 | 0 | 0 | 3 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| MG      | 24702 |
| SP      | 18810 |
| RS      | 14747 |
| BA      | 13220 |
| PR      | 11994 |

**Top-5 values for `rede`**

|   value |   cnt |
|--------:|------:|
|       0 | 30944 |
|       6 | 30944 |
|       5 | 30934 |
|       3 | 30255 |
|       2 | 28953 |

**Top-5 values for `tipo_localizacao`**

|   value |   cnt |
|--------:|------:|
|       0 | 61063 |
|       1 | 60887 |
|       2 | 47352 |

### Histograms

#### Equal-frequency bins (NTILE)

**ano** (bins=10, time 0.125934s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 2019 | 2019 | 16931 |
| 2 | 2019 | 2019 | 16931 |
| 3 | 2019 | 2019 | 16930 |
| 4 | 2019 | 2019 | 16930 |
| 5 | 2019 | 2021 | 16930 |
| 6 | 2021 | 2021 | 16930 |
| 7 | 2021 | 2021 | 16930 |
| 8 | 2021 | 2021 | 16930 |
| 9 | 2021 | 2021 | 16930 |
| 10 | 2021 | 2021 | 16930 |

**quantidade_alunos_inse** (bins=10, time 0.127030s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 16931 |
| 2 | 0 | 16 | 16931 |
| 3 | 16 | 51 | 16930 |
| 4 | 51 | 87 | 16930 |
| 5 | 87 | 130 | 16930 |
| 6 | 130 | 189 | 16930 |
| 7 | 189 | 280 | 16930 |
| 8 | 280 | 445 | 16930 |
| 9 | 445 | 847 | 16930 |
| 10 | 847 | 277258 | 16930 |

**inse** (bins=10, time 0.139612s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 16931 |
| 2 | 0 | 3.84 | 16931 |
| 3 | 3.84 | 4.1447 | 16930 |
| 4 | 4.1447 | 4.3182 | 16930 |
| 5 | 4.3182 | 4.5 | 16930 |
| 6 | 4.5 | 4.78 | 16930 |
| 7 | 4.78 | 5.01 | 16930 |
| 8 | 5.01 | 5.1803 | 16930 |
| 9 | 5.1803 | 5.36 | 16930 |
| 10 | 5.36 | 6.72 | 16930 |

**percentual_nivel_2** (bins=10, time 0.195734s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 2.25 | 13993 |
| 2 | 2.25 | 4.28 | 13993 |
| 3 | 4.28 | 6.61 | 13992 |
| 4 | 6.61 | 9.93 | 13992 |
| 5 | 9.93 | 15.39 | 13992 |
| 6 | 15.39 | 23.02 | 13992 |
| 7 | 23.03 | 29.58 | 13992 |
| 8 | 29.58 | 35.6 | 13992 |
| 9 | 35.6 | 42.91 | 13992 |
| 10 | 42.91 | 100 | 13992 |

**percentual_nivel_3** (bins=10, time 0.254229s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 7.27 | 13993 |
| 2 | 7.27 | 10.38 | 13993 |
| 3 | 10.38 | 13.4 | 13992 |
| 4 | 13.4 | 16.34 | 13992 |
| 5 | 16.34 | 19.14 | 13992 |
| 6 | 19.14 | 21.51 | 13992 |
| 7 | 21.51 | 23.5 | 13992 |
| 8 | 23.5 | 25.42 | 13992 |
| 9 | 25.42 | 27.9 | 13992 |
| 10 | 27.9 | 77.78 | 13992 |

**percentual_nivel_4** (bins=10, time 0.338769s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 12.06 | 13993 |
| 2 | 12.06 | 15.26 | 13993 |
| 3 | 15.26 | 17.36 | 13992 |
| 4 | 17.36 | 19.03 | 13992 |
| 5 | 19.03 | 20.56 | 13992 |
| 6 | 20.56 | 22.02 | 13992 |
| 7 | 22.02 | 23.5 | 13992 |
| 8 | 23.5 | 25.21 | 13992 |
| 9 | 25.21 | 27.89 | 13992 |
| 10 | 27.89 | 100 | 13992 |

**percentual_nivel_5** (bins=10, time 0.306584s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 6.67 | 13993 |
| 2 | 6.67 | 9.52 | 13993 |
| 3 | 9.52 | 12.07 | 13992 |
| 4 | 12.07 | 14.94 | 13992 |
| 5 | 14.94 | 18.34 | 13992 |
| 6 | 18.34 | 21.61 | 13992 |
| 7 | 21.61 | 24.08 | 13992 |
| 8 | 24.08 | 26.15 | 13992 |
| 9 | 26.15 | 28.73 | 13992 |
| 10 | 28.73 | 80 | 13992 |

**percentual_nivel_6** (bins=10, time 0.148945s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 2.1 | 13993 |
| 2 | 2.1 | 3.63 | 13993 |
| 3 | 3.63 | 5.11 | 13992 |
| 4 | 5.11 | 7.05 | 13992 |
| 5 | 7.05 | 10 | 13992 |
| 6 | 10 | 13.91 | 13992 |
| 7 | 13.91 | 17.37 | 13992 |
| 8 | 17.37 | 20.78 | 13992 |
| 9 | 20.78 | 24.76 | 13992 |
| 10 | 24.76 | 83.33 | 13992 |

**percentual_nivel_7** (bins=10, time 0.141078s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0.24 | 13993 |
| 2 | 0.24 | 1.22 | 13993 |
| 3 | 1.22 | 1.99 | 13992 |
| 4 | 1.99 | 3.02 | 13992 |
| 5 | 3.02 | 4.95 | 13992 |
| 6 | 4.95 | 7.86 | 13992 |
| 7 | 7.86 | 10.89 | 13992 |
| 8 | 10.89 | 14.29 | 13992 |
| 9 | 14.29 | 19.03 | 13992 |
| 10 | 19.03 | 81.82 | 13992 |

**percentual_nivel_8** (bins=10, time 0.141854s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 13993 |
| 2 | 0 | 0 | 13993 |
| 3 | 0 | 0 | 13992 |
| 4 | 0 | 0 | 13992 |
| 5 | 0 | 0.17 | 13992 |
| 6 | 0.17 | 0.44 | 13992 |
| 7 | 0.44 | 0.8 | 13992 |
| 8 | 0.8 | 1.27 | 13992 |
| 9 | 1.27 | 2.06 | 13992 |
| 10 | 2.06 | 43.75 | 13992 |

#### Fixed-width bins (width_bucket)

**quantidade_alunos_inse** (bins=10, time 0.061959s)

```


██████████████████████████████████████████████████    169.13K    [0,27725.8)                  
                                                        92.00    [27725.8,55451.6)            
                                                        48.00    [55451.6,83177.4)            
                                                        12.00    [83177.4,110903.2)           
                                                         2.00    [138629,166354.8)            
                                                         2.00    [194080.6,221806.4)          
                                                         6.00    [221806.4,249532.19999999998)
                                                         2.00    [249532.19999999998,277258)  
```

**inse** (bins=10, time 0.060834s)

```


█████████████████████████                             29.38K    [0,0.6719999999999999)                 
                                                        4.00    [2.016,2.6879999999999997)             
                                                      146.00    [2.6879999999999997,3.3599999999999994)
███████████                                           12.93K    [3.3599999999999994,4.032)             
████████████████████████████████████████████████      54.94K    [4.032,4.704)                          
██████████████████████████████████████████████████    56.53K    [4.704,5.3759999999999994)             
█████████████                                         15.26K    [5.3759999999999994,6.047999999999999) 
                                                      110.00    [6.047999999999999,6.719999999999999)  
```

**percentual_nivel_2** (bins=10, time 0.065003s)

```


█████████████████████████████████████████████████████████    56.18K    [0,10)  
██████████████████████                                       22.12K    [10,20) 
████████████████████                                         20.62K    [20,30) 
██████████████████████                                       22.07K    [30,40) 
█████████████                                                13.18K    [40,50) 
████                                                          4.68K    [50,60) 
                                                             913.00    [60,70) 
                                                             129.00    [70,80) 
                                                              31.00    [80,90) 
                                                               6.00    [90,100)
```

**percentual_nivel_3** (bins=10, time 0.052624s)

```


██████████████████                                    16.04K    [0,7.7780000000000005)                 
████████████████████████████████████████              36.23K    [7.7780000000000005,15.556000000000001)
██████████████████████████████████████████████████    44.49K    [15.556000000000001,23.334000000000003)
██████████████████████████████████████████            37.76K    [23.334000000000003,31.112000000000002)
█████                                                  4.48K    [31.112000000000002,38.89)             
                                                      709.00    [38.89,46.668000000000006)             
                                                      143.00    [46.668000000000006,54.446000000000005)
                                                       50.00    [54.446000000000005,62.224000000000004)
                                                       19.00    [62.224000000000004,70.00200000000001) 
```

**percentual_nivel_4** (bins=10, time 0.051644s)

```


███████                                                        8.18K    [0,10) 
████████████████████████████████████████████████              56.39K    [10,20)
██████████████████████████████████████████████████████████    67.28K    [20,30)
██████                                                         6.99K    [30,40)
                                                              818.00    [40,50)
                                                              227.00    [50,60)
                                                               39.00    [60,70)
                                                                2.00    [70,80)
```

**percentual_nivel_5** (bins=10, time 0.051619s)

```


████████████████████████████                                  19.81K    [0,8)  
██████████████████████████████████████████████████████████    40.67K    [8,16) 
████████████████████████████████████████████████████          36.87K    [16,24)
████████████████████████████████████████████████████          36.47K    [24,32)
███████                                                        5.05K    [32,40)
█                                                             747.00    [40,48)
                                                              235.00    [48,56)
                                                               46.00    [56,64)
                                                               18.00    [64,72)
                                                                4.00    [72,80)
```

**percentual_nivel_6** (bins=10, time 0.049840s)

```


██████████████████████████████████████████████████    62.87K    [0,8.333)                  
█████████████████████████                             32.05K    [8.333,16.666)             
█████████████████████████                             31.70K    [16.666,24.999000000000002)
█████████                                             11.56K    [24.999000000000002,33.332)
█                                                      1.37K    [33.332,41.665)            
                                                      257.00    [41.665,49.998000000000005)
                                                       91.00    [49.998000000000005,58.331)
                                                        7.00    [58.331,66.664)            
                                                        2.00    [66.664,74.997)            
                                                        5.00    [74.997,83.33)             
```

**percentual_nivel_7** (bins=10, time 0.059460s)

```


██████████████████████████████████████████████████    85.54K    [0,8.181999999999999)                  
███████████████████                                   33.41K    [8.181999999999999,16.363999999999997) 
████████                                              14.95K    [16.363999999999997,24.545999999999996)
██                                                     4.24K    [24.545999999999996,32.727999999999994)
                                                       1.31K    [32.727999999999994,40.91)             
                                                      338.00    [40.91,49.09199999999999)              
                                                       89.00    [49.09199999999999,57.27399999999999)  
                                                       18.00    [57.27399999999999,65.45599999999999)  
                                                        4.00    [65.45599999999999,73.63799999999999)  
```

**percentual_nivel_8** (bins=10, time 0.073616s)

```


██████████████████████████████████████████████████    137.01K    [0,4.375)     
                                                        2.43K    [4.375,8.75)  
                                                       335.00    [8.75,13.125) 
                                                        99.00    [13.125,17.5) 
                                                        31.00    [17.5,21.875) 
                                                         9.00    [21.875,26.25)
                                                         4.00    [26.25,30.625)
                                                         3.00    [30.625,35)   
                                                         1.00    [35,39.375)   
```

**ano** (categorical-like, top-10) — time 0.035547s

```


█████████████████████████████████████████████████████████████    99.40K    2021
██████████████████████████████████████████                       69.91K    2019
```


`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001938 |
| numeric_aggregates | 0.898394 |
| categoricals_total | 0.192106 |
| histograms_total | 2.481915 |
| table_total | 3.962629 |

---

## 10. br_ms_sim_municipio_causa_idade_sexo_raca

_Skipped ID-like columns (id_*, *_id):_ `id_municipio, id_municipio_nome`

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ano | 40027 | 0 | 0 | 1 | 2019 | 0 | 2019 | 2019 | 2019 | 2019 | 2019 |
| idade | 39936 | 91 | 0.2273 | 112 | 66.18622295673077 | 20.642260442176145 | 0 | 56 | 70 | 81 | 112 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| ano | 2019 | 2019 | 0 | 0.010278 |
| idade | 18.5 | 118.5 | 1367 | 0.010286 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| sigla_uf | 40027 | 0 | 0 | 1 |
| sigla_uf_nome | 40027 | 0 | 0 | 1 |
| causa_basica | 40027 | 0 | 0 | 2142 |
| causa_basica_descricao_subcategoria | 40027 | 0 | 0 | 2138 |
| causa_basica_descricao_categoria | 40027 | 0 | 0 | 835 |
| causa_basica_descricao_capitulo | 40027 | 0 | 0 | 19 |
| sexo | 40027 | 0 | 0 | 3 |
| raca_cor | 39673 | 354 | 0.8844 | 5 |
| numero_obitos | 40027 | 0 | 0 | 8 |

**Top-5 values for `sigla_uf`**

| value   |   cnt |
|:--------|------:|
| SC      | 40027 |

**Top-5 values for `sigla_uf_nome`**

| value          |   cnt |
|:---------------|------:|
| Santa Catarina | 40027 |

**Top-5 values for `causa_basica`**

| value   |   cnt |
|:--------|------:|
| I219    |  2170 |
| C349    |  1127 |
| J189    |  1071 |
| I64     |  1014 |
| J449    |   768 |

**Top-5 values for `causa_basica_descricao_subcategoria`**

| value                                                                      |   cnt |
|:---------------------------------------------------------------------------|------:|
| Infarto agudo do miocárdio não especificado                                |  2170 |
| Neoplasia maligna dos brônquios ou pulmões, não especificado               |  1127 |
| Pneumonia não especificada                                                 |  1071 |
| Acidente vascular cerebral, não especificado como hemorrágico ou isquêmico |  1014 |
| Doença pulmonar obstrutiva crônica não especificada                        |   768 |

**Top-5 values for `causa_basica_descricao_categoria`**

| value                                          |   cnt |
|:-----------------------------------------------|------:|
| Infarto agudo do miocárdio                     |  2236 |
| Outras doenças pulmonares obstrutivas crônicas |  1715 |
| Pneumonia por microorganismo não especificada  |  1374 |
| Diabetes mellitus não especificado             |  1218 |
| Neoplasia maligna dos brônquios e dos pulmões  |  1217 |

**Top-5 values for `causa_basica_descricao_capitulo`**

| value                                          |   cnt |
|:-----------------------------------------------|------:|
| Doenças do aparelho circulatório               | 10562 |
| Neoplasmas (tumores)                           |  8841 |
| Doenças do aparelho respiratório               |  4875 |
| Causas externas de morbidade e de mortalidade  |  4246 |
| Doenças endócrinas, nutricionais e metabólicas |  2353 |

**Top-5 values for `sexo`**

| value                                           |   cnt |
|:------------------------------------------------|------:|
| Masculino                                       | 22208 |
| Feminino                                        | 17812 |
| Código não encontrado nos dicionários oficiais. |     7 |

**Top-5 values for `raca_cor`**

| value    |   cnt |
|:---------|------:|
| Branca   | 35826 |
| Parda    |  2411 |
| Preta    |  1297 |
|          |   354 |
| Indígena |    73 |

**Top-5 values for `numero_obitos`**

|   value |   cnt |
|--------:|------:|
|       1 | 38236 |
|       2 |  1477 |
|       3 |   224 |
|       4 |    64 |
|       5 |    18 |

### Histograms

#### Equal-frequency bins (NTILE)

**ano** (bins=10, time 0.011945s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 2019 | 2019 | 4003 |
| 2 | 2019 | 2019 | 4003 |
| 3 | 2019 | 2019 | 4003 |
| 4 | 2019 | 2019 | 4003 |
| 5 | 2019 | 2019 | 4003 |
| 6 | 2019 | 2019 | 4003 |
| 7 | 2019 | 2019 | 4003 |
| 8 | 2019 | 2019 | 4002 |
| 9 | 2019 | 2019 | 4002 |
| 10 | 2019 | 2019 | 4002 |

**idade** (bins=10, time 0.014390s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 38 | 3994 |
| 2 | 38 | 52 | 3994 |
| 3 | 52 | 60 | 3994 |
| 4 | 60 | 65 | 3994 |
| 5 | 65 | 70 | 3994 |
| 6 | 70 | 75 | 3994 |
| 7 | 75 | 79 | 3993 |
| 8 | 79 | 83 | 3993 |
| 9 | 83 | 88 | 3993 |
| 10 | 88 | 112 | 3993 |

#### Fixed-width bins (width_bucket)

**ano** (categorical-like, top-10) — time 0.007492s

```


█████████████████████████████████████████████████████████████    40.03K    2019
```

**idade** (categorical-like, top-10) — time 0.009261s

```


███████████████████████████████████████████████████████████████    946.00    80
█████████████████████████████████████████████████████████████      923.00    79
█████████████████████████████████████████████████████████████      921.00    83
████████████████████████████████████████████████████████████       912.00    76
████████████████████████████████████████████████████████████       912.00    81
███████████████████████████████████████████████████████████        900.00    82
███████████████████████████████████████████████████████████        895.00    72
██████████████████████████████████████████████████████████         884.00    73
██████████████████████████████████████████████████████████         884.00    77
██████████████████████████████████████████████████████████         879.00    71
```


`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001405 |
| numeric_aggregates | 0.067043 |
| categoricals_total | 0.246783 |
| histograms_total | 0.043088 |
| table_total | 0.389544 |

---

## 11. br_tse_eleicoes_resultados_candidato_municipio_sc

_Skipped ID-like columns (id_*, *_id):_ `id_eleicao, id_municipio, id_municipio_tse`

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ano | 263435 | 0 | 0 | 1 | 2022 | 0 | 2022 | 2022 | 2022 | 2022 | 2022 |
| turno | 263435 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| numero_partido | 263435 | 0 | 0 | 28 | 31.669652855543113 | 20.417357183229562 | 10 | 14 | 22 | 45 | 90 |
| votos | 263435 | 0 | 0 | 2833 | 58.48613889574278 | 918.50554596069 | 0 | 0 | 0 | 2 | 151072 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| ano | 2022 | 2022 | 0 | 0.142715 |
| turno | 1 | 1 | 0 | 0.111915 |
| numero_partido | -32.5 | 91.5 | 0 | 0.095538 |
| votos | -3 | 5 | 45485 | 0.090953 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| tipo_eleicao | 263435 | 0 | 0 | 1 |
| data_eleicao | 263435 | 0 | 0 | 1 |
| sigla_uf | 263435 | 0 | 0 | 1 |
| cargo | 263435 | 0 | 0 | 4 |
| sigla_partido | 263435 | 0 | 0 | 28 |
| titulo_eleitoral_candidato | 262550 | 885 | 0.3359 | 890 |
| sequencial_candidato | 263435 | 0 | 0 | 893 |
| numero_candidato | 263435 | 0 | 0 | 893 |
| resultado | 263435 | 0 | 0 | 6 |

**Top-5 values for `tipo_eleicao`**

| value             |    cnt |
|:------------------|-------:|
| eleicao ordinaria | 263435 |

**Top-5 values for `data_eleicao`**

| value      |    cnt |
|:-----------|-------:|
| 2022-10-02 | 263435 |

**Top-5 values for `sigla_uf`**

| value   |    cnt |
|:--------|-------:|
| SC      | 263435 |

**Top-5 values for `cargo`**

| value             |    cnt |
|:------------------|-------:|
| deputado estadual | 171690 |
| deputado federal  |  86140 |
| governador        |   2950 |
| senador           |   2655 |

**Top-5 values for `sigla_partido`**

| value    |   cnt |
|:---------|------:|
| PL       | 16815 |
| PATRIOTA | 16520 |
| UNIÃO    | 16520 |
| PTB      | 15340 |
| PDT      | 14750 |

**Top-5 values for `titulo_eleitoral_candidato`**

| value        |   cnt |
|:-------------|------:|
|              |   885 |
| 000000160973 |   295 |
| 000162180930 |   295 |
| 000235200922 |   295 |
| 000287572810 |   295 |

**Top-5 values for `sequencial_candidato`**

|        value |   cnt |
|-------------:|------:|
| 240001597409 |   295 |
| 240001597410 |   295 |
| 240001597411 |   295 |
| 240001597412 |   295 |
| 240001597453 |   295 |

**Top-5 values for `numero_candidato`**

|   value |   cnt |
|--------:|------:|
|      10 |   295 |
|    1000 |   295 |
|   10000 |   295 |
|   10010 |   295 |
|   10019 |   295 |

**Top-5 values for `resultado`**

| value            |    cnt |
|:-----------------|-------:|
| suplente         | 133045 |
| nao eleito       | 112985 |
| eleito por qp    |  11210 |
| eleito por media |   5310 |
| 2º turno         |    590 |

### Histograms

#### Equal-frequency bins (NTILE)

**ano** (bins=10, time 0.291709s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 2022 | 2022 | 26344 |
| 2 | 2022 | 2022 | 26344 |
| 3 | 2022 | 2022 | 26344 |
| 4 | 2022 | 2022 | 26344 |
| 5 | 2022 | 2022 | 26344 |
| 6 | 2022 | 2022 | 26343 |
| 7 | 2022 | 2022 | 26343 |
| 8 | 2022 | 2022 | 26343 |
| 9 | 2022 | 2022 | 26343 |
| 10 | 2022 | 2022 | 26343 |

**turno** (bins=10, time 0.329269s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 26344 |
| 2 | 1 | 1 | 26344 |
| 3 | 1 | 1 | 26344 |
| 4 | 1 | 1 | 26344 |
| 5 | 1 | 1 | 26344 |
| 6 | 1 | 1 | 26343 |
| 7 | 1 | 1 | 26343 |
| 8 | 1 | 1 | 26343 |
| 9 | 1 | 1 | 26343 |
| 10 | 1 | 1 | 26343 |

**numero_partido** (bins=10, time 0.320289s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 10 | 11 | 26344 |
| 2 | 11 | 13 | 26344 |
| 3 | 13 | 15 | 26344 |
| 4 | 15 | 20 | 26344 |
| 5 | 20 | 22 | 26344 |
| 6 | 22 | 30 | 26343 |
| 7 | 30 | 44 | 26343 |
| 8 | 44 | 50 | 26343 |
| 9 | 50 | 55 | 26343 |
| 10 | 55 | 90 | 26343 |

**votos** (bins=10, time 0.303800s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 26344 |
| 2 | 0 | 0 | 26344 |
| 3 | 0 | 0 | 26344 |
| 4 | 0 | 0 | 26344 |
| 5 | 0 | 0 | 26344 |
| 6 | 0 | 0 | 26343 |
| 7 | 0 | 1 | 26343 |
| 8 | 1 | 4 | 26343 |
| 9 | 4 | 21 | 26343 |
| 10 | 21 | 151072 | 26343 |

#### Fixed-width bins (width_bucket)

**votos** (bins=10, time 0.118818s)

```


██████████████████████████████████████████████████    263.30K    [0,15107.2)                           
                                                        91.00    [15107.2,30214.4)                     
                                                        28.00    [30214.4,45321.600000000006)          
                                                         9.00    [45321.600000000006,60428.8)          
                                                         2.00    [60428.8,75536)                       
                                                         3.00    [75536,90643.20000000001)             
                                                         2.00    [90643.20000000001,105750.40000000001)
                                                         1.00    [105750.40000000001,120857.6)         
```

**ano** (categorical-like, top-10) — time 0.049227s

```


████████████████████████████████████████████████████████████    263.44K    2022
```

**turno** (categorical-like, top-10) — time 0.049318s

```


███████████████████████████████████████████████████████████████    263.44K    1
```

**numero_partido** (categorical-like, top-10) — time 0.046060s

```


███████████████████████████████████████████████████████████████    16.82K    22
█████████████████████████████████████████████████████████████      16.52K    44
█████████████████████████████████████████████████████████████      16.52K    51
█████████████████████████████████████████████████████████          15.34K    14
███████████████████████████████████████████████████████            14.75K    12
██████████████████████████████████████████████████████             14.46K    11
██████████████████████████████████████████████████████             14.46K    13
██████████████████████████████████████████████████████             14.46K    15
██████████████████████████████████████████████████                 13.57K    10
██████████████████████████████████████████████████                 13.57K    30
```


`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.002156 |
| numeric_aggregates | 1.891564 |
| categoricals_total | 2.69304 |
| histograms_total | 1.508489 |
| table_total | 6.549566 |

---

## 12. votacao_secao_2022_sc

### Numeric columns

| column | non_null | nulls | nulls_% | distinct | mean | stddev | min | p25 | median | p75 | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ano_eleicao | 2178931 | 0 | 0 | 1 | 2022 | 0 | 2022 | 2022 | 2022 | 2022 | 2022 |
| cd_tipo_eleicao | 2178931 | 0 | 0 | 1 | 2 | 0 | 2 | 2 | 2 | 2 | 2 |
| nr_turno | 2178931 | 0 | 0 | 2 | 1.0297141121035958 | 0.16979747832488767 | 1 | 1 | 1 | 1 | 2 |
| cd_eleicao | 2178931 | 0 | 0 | 2 | 546.0297141121036 | 0.16979747832488767 | 546 | 546 | 546 | 546 | 547 |

#### Outliers (Tukey fences)

| column | low | high | outliers | time (s) |
| --- | --- | --- | --- | --- |
| ano_eleicao | 2022 | 2022 | 0 | 2.287289 |
| cd_tipo_eleicao | 2 | 2 | 0 | 2.376043 |
| nr_turno | 1 | 1 | 64745 | 2.453041 |
| cd_eleicao | 546 | 546 | 64745 | 2.325061 |

### Categorical columns

| column | non_null | nulls | nulls_% | distinct |
| --- | --- | --- | --- | --- |
| dt_geracao | 2178931 | 0 | 0 | 1 |
| hh_geracao | 2178931 | 0 | 0 | 1 |
| nm_tipo_eleicao | 2178931 | 0 | 0 | 1 |
| ds_eleicao | 2178931 | 0 | 0 | 1 |
| dt_eleicao | 2178931 | 0 | 0 | 2 |
| tp_abrangencia | 2178931 | 0 | 0 | 1 |
| sg_uf | 2178931 | 0 | 0 | 1 |
| sg_ue | 2178931 | 0 | 0 | 1 |
| nm_ue | 2178931 | 0 | 0 | 1 |
| cd_municipio | 2178931 | 0 | 0 | 295 |
| nm_municipio | 2178931 | 0 | 0 | 295 |
| nr_zona | 2178931 | 0 | 0 | 99 |
| nr_secao | 2178931 | 0 | 0 | 800 |
| cd_cargo | 2178931 | 0 | 0 | 4 |
| ds_cargo | 2178931 | 0 | 0 | 4 |
| nr_votavel | 2178931 | 0 | 0 | 938 |
| nm_votavel | 2178931 | 0 | 0 | 946 |
| qt_votos | 2178931 | 0 | 0 | 310 |
| nr_local_votacao | 2178931 | 0 | 0 | 147 |
| sq_candidato | 2178931 | 0 | 0 | 920 |
| nm_local_votacao | 2178931 | 0 | 0 | 3427 |
| ds_local_votacao_endereco | 2178931 | 0 | 0 | 2574 |

**Top-5 values for `dt_geracao`**

| value      |     cnt |
|:-----------|--------:|
| 01/11/2022 | 2178931 |

**Top-5 values for `hh_geracao`**

| value    |     cnt |
|:---------|--------:|
| 16:05:25 | 2178931 |

**Top-5 values for `nm_tipo_eleicao`**

| value             |     cnt |
|:------------------|--------:|
| ELEIÇÃO ORDINÁRIA | 2178931 |

**Top-5 values for `ds_eleicao`**

| value                          |     cnt |
|:-------------------------------|--------:|
| ELEIÇÕES GERAIS ESTADUAIS 2022 | 2178931 |

**Top-5 values for `dt_eleicao`**

| value      |     cnt |
|:-----------|--------:|
| 02/10/2022 | 2114186 |
| 30/10/2022 |   64745 |

**Top-5 values for `tp_abrangencia`**

| value   |     cnt |
|:--------|--------:|
| E       | 2178931 |

**Top-5 values for `sg_uf`**

| value   |     cnt |
|:--------|--------:|
| SC      | 2178931 |

**Top-5 values for `sg_ue`**

| value   |     cnt |
|:--------|--------:|
| SC      | 2178931 |

**Top-5 values for `nm_ue`**

| value          |     cnt |
|:---------------|--------:|
| SANTA CATARINA | 2178931 |

**Top-5 values for `cd_municipio`**

|   value |    cnt |
|--------:|-------:|
|   81051 | 197561 |
|   81795 | 185253 |
|   80470 | 102890 |
|   83275 |  94689 |
|   81612 |  66257 |

**Top-5 values for `nm_municipio`**

| value         |    cnt |
|:--------------|-------:|
| FLORIANÓPOLIS | 197561 |
| JOINVILLE     | 185253 |
| BLUMENAU      | 102890 |
| SÃO JOSÉ      |  94689 |
| ITAJAÍ        |  66257 |

**Top-5 values for `nr_zona`**

|   value |   cnt |
|--------:|------:|
|      12 | 71796 |
|      13 | 64277 |
|      24 | 63703 |
|     100 | 61488 |
|       3 | 59609 |

**Top-5 values for `nr_secao`**

|   value |   cnt |
|--------:|------:|
|       1 |  9495 |
|       3 |  9443 |
|       2 |  9428 |
|      23 |  9311 |
|      22 |  9233 |

**Top-5 values for `cd_cargo`**

|   value |    cnt |
|--------:|-------:|
|       7 | 970447 |
|       6 | 837896 |
|       3 | 210711 |
|       5 | 159877 |

**Top-5 values for `ds_cargo`**

| value             |    cnt |
|:------------------|-------:|
| DEPUTADO ESTADUAL | 970447 |
| DEPUTADO FEDERAL  | 837896 |
| GOVERNADOR        | 210711 |
| SENADOR           | 159877 |

**Top-5 values for `nr_votavel`**

|   value |   cnt |
|--------:|------:|
|      95 | 81045 |
|      96 | 80634 |
|      22 | 61224 |
|      13 | 60257 |
|      11 | 27016 |

**Top-5 values for `nm_votavel`**

| value                     |   cnt |
|:--------------------------|------:|
| VOTO BRANCO               | 81045 |
| VOTO NULO                 | 80634 |
| DÉCIO NERY DE LIMA        | 32482 |
| JORGINHO DOS SANTOS MELLO | 32480 |
| Partido Liberal           | 28744 |

**Top-5 values for `qt_votos`**

|   value |    cnt |
|--------:|-------:|
|       1 | 857924 |
|       2 | 304671 |
|       3 | 161211 |
|       4 | 105286 |
|       5 |  76304 |

**Top-5 values for `nr_local_votacao`**

|   value |    cnt |
|--------:|-------:|
|    1015 | 261194 |
|    1023 | 124867 |
|    1040 |  94270 |
|    1031 |  83609 |
|    1066 |  66083 |

**Top-5 values for `sq_candidato`**

|        value |    cnt |
|-------------:|-------:|
|           -3 | 197855 |
|           -1 | 161679 |
| 240001647445 |  32482 |
| 240001611127 |  32480 |
| 240001610772 |  16236 |

**Top-5 values for `nm_local_votacao`**

| value                                                |   cnt |
|:-----------------------------------------------------|------:|
| COLÉGIO MUNICIPAL MARIA LUIZA DE MELO                |  6465 |
| ASSOCIAÇÃO FRANCISCANA DE ENSINO SENHOR BOM JESUS    |  5957 |
| ESCOLA DE EDUCAÇÃO BÁSICA ENGENHEIRO ANNES GUALBERTO |  5213 |
| UNIVALI - UNIVERSIDADE DO VALE DO ITAJAI - CAMPUS II |  5204 |
| UNIVALI - UNIVERSIDADE DO VALE DO ITAJAÍ             |  5090 |

**Top-5 values for `ds_local_votacao_endereco`**

| value                                 |   cnt |
|:--------------------------------------|------:|
| ESTRADA GERAL, S/N                    | 75935 |
| RUA GERAL, S/N                        |  6671 |
| RUA JOSÉ FERMINO NOVAES - FUNDOS, S/N |  6465 |
| QUINTA AVENIDA, 1100                  |  5204 |
| RUA 1500, N. 640                      |  5057 |

### Histograms

#### Equal-frequency bins (NTILE)

**ano_eleicao** (bins=10, time 3.157308s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 2022 | 2022 | 217894 |
| 2 | 2022 | 2022 | 217893 |
| 3 | 2022 | 2022 | 217893 |
| 4 | 2022 | 2022 | 217893 |
| 5 | 2022 | 2022 | 217893 |
| 6 | 2022 | 2022 | 217893 |
| 7 | 2022 | 2022 | 217893 |
| 8 | 2022 | 2022 | 217893 |
| 9 | 2022 | 2022 | 217893 |
| 10 | 2022 | 2022 | 217893 |

**cd_tipo_eleicao** (bins=10, time 3.083541s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 217894 |
| 2 | 2 | 2 | 217893 |
| 3 | 2 | 2 | 217893 |
| 4 | 2 | 2 | 217893 |
| 5 | 2 | 2 | 217893 |
| 6 | 2 | 2 | 217893 |
| 7 | 2 | 2 | 217893 |
| 8 | 2 | 2 | 217893 |
| 9 | 2 | 2 | 217893 |
| 10 | 2 | 2 | 217893 |

**nr_turno** (bins=10, time 3.272510s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 217894 |
| 2 | 1 | 1 | 217893 |
| 3 | 1 | 1 | 217893 |
| 4 | 1 | 1 | 217893 |
| 5 | 1 | 1 | 217893 |
| 6 | 1 | 1 | 217893 |
| 7 | 1 | 1 | 217893 |
| 8 | 1 | 1 | 217893 |
| 9 | 1 | 1 | 217893 |
| 10 | 1 | 2 | 217893 |

**cd_eleicao** (bins=10, time 3.739534s)

| bin | lo | hi | count |
| --- | --- | --- | --- |
| 1 | 546 | 546 | 217894 |
| 2 | 546 | 546 | 217893 |
| 3 | 546 | 546 | 217893 |
| 4 | 546 | 546 | 217893 |
| 5 | 546 | 546 | 217893 |
| 6 | 546 | 546 | 217893 |
| 7 | 546 | 546 | 217893 |
| 8 | 546 | 546 | 217893 |
| 9 | 546 | 546 | 217893 |
| 10 | 546 | 547 | 217893 |

#### Fixed-width bins (width_bucket)

**ano_eleicao** (categorical-like, top-10) — time 1.251336s

```


██████████████████████████████████████████████████████████████    2.18M    2022
```

**cd_tipo_eleicao** (categorical-like, top-10) — time 1.255620s

```


█████████████████████████████████████████████████████████████████    2.18M    2
```

**nr_turno** (categorical-like, top-10) — time 1.511971s

```


████████████████████████████████████████████████████████████████     2.11M    1
█                                                                   64.75K    2
```

**cd_eleicao** (categorical-like, top-10) — time 1.266559s

```


██████████████████████████████████████████████████████████████     2.11M    546
█                                                                 64.75K    547
```


`Execution timings`

| step | time (s) |
| --- | --- |
| split_columns | 0.001835 |
| numeric_aggregates | 15.758996 |
| categoricals_total | 99.21526 |
| histograms_total | 18.53838 |
| table_total | 142.980521 |

---

