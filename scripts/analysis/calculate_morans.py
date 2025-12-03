#!/usr/bin/env python3
"""
Calcula Moran Global (qt_votos e votos_por_pop) por candidato
a partir da view eleicoes22.agg_eleicao_e_outras_bases_materialized e grava
em eleicoes22.calc_moran_dep_e_partido, sem recálculo para
candidatos já presentes na tabela.

Requisitos:
    pip install psycopg2-binary sqlalchemy geopandas libpysal esda
"""

import os
import sys
import logging

import numpy as np
import geopandas as gpd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import libpysal
from esda.moran import Moran
from tqdm import tqdm


USE_PARTY = True  # se True, calcula por partido em vez de por candidato

# ---------------------------------------------------------------------------
# Configuração básica
# ---------------------------------------------------------------------------

# Use variáveis de ambiente se quiser mudar facilmente
PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5434")  # você estava usando 5434 no QGIS
PGDATABASE = os.getenv("PGDATABASE", "gis")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "postgres")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)

# ---------------------------------------------------------------------------
# Conexão
# ---------------------------------------------------------------------------

def get_sqlalchemy_engine():
    # Ex: postgresql+psycopg2://user:pass@host:port/dbname
    if PGPASSWORD:
        conn_str = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
    else:
        conn_str = f"postgresql+psycopg2://{PGUSER}@{PGHOST}:{PGPORT}/{PGDATABASE}"
    return create_engine(conn_str)


def get_psycopg2_conn():
    return psycopg2.connect(
        host=PGHOST,
        port=PGPORT,
        dbname=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
    )

# ---------------------------------------------------------------------------
# Consultas auxiliares
# ---------------------------------------------------------------------------

def fetch_distinct_candidates(conn):
    """
    Retorna lista de (sq_candidato) distintos na view agregada.
    Se quiser nm_votavel também, basta incluir na query.
    """
    sql = """
        SELECT DISTINCT sq_candidato
        FROM eleicoes22.agg_eleicao_e_outras_bases_materialized
        WHERE sq_candidato IS NOT NULL
        ORDER BY sq_candidato
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [r[0] for r in rows]

def fetch_distinct_parties(conn):
    """
    Retorna lista de (sigla_partido) distintos na view agregada.
    Se quiser nm_votavel também, basta incluir na query.
    """
    sql = """
        SELECT DISTINCT sigla_partido
        FROM eleicoes22.agg_eleicao_partidos_e_outras_bases
        WHERE sigla_partido IS NOT NULL
        ORDER BY sigla_partido
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [r[0] for r in rows]

def item_already_processed(conn, sq_candidato):
    """
    Verifica se já existe linha na tabela de cálculo
    para esse sq_candidato (tipo=1 => candidato).
    """
    sql = """
        SELECT 1
        FROM eleicoes22.calc_moran_dep_e_partido
        WHERE sequencial_ou_sigla_partido = %s
        LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(sql, (str(sq_candidato),))
        return cur.fetchone() is not None


def load_candidate_geodata(engine, sq_candidato):
    """
    Carrega dados espaciais para um candidato específico
    a partir da view eleicoes22.agg_eleicao_e_outras_bases_materialized.
    """
    sql = """
        SELECT
            id_municipio,
            qt_votos,
            votos_por_pop,
            geom
        FROM eleicoes22.agg_eleicao_e_outras_bases_materialized
        WHERE sq_candidato = %(sq_candidato)s
          AND geom IS NOT NULL
    """
    gdf = gpd.read_postgis(
        sql,
        engine,
        params={"sq_candidato": sq_candidato},
        geom_col="geom",
    )
    return gdf


def load_party_geodata(engine, sigla_partido):
    sql = """
        SELECT
            id_municipio,
            qt_votos,
            votos_por_pop,
            geom
        FROM eleicoes22.agg_eleicao_partidos_e_outras_bases
        WHERE sigla_partido = %(sigla_partido)s
          AND geom IS NOT NULL
    """
    gdf = gpd.read_postgis(
        sql,
        engine,
        params={"sigla_partido": sigla_partido},
        geom_col="geom",
    )
    return gdf

# ---------------------------------------------------------------------------
# Cálculo do Moran para um candidato
# ---------------------------------------------------------------------------

def compute_moran_for_candidate(gdf, sq_candidato=None):
    """
    Recebe um GeoDataFrame com colunas:
        - qt_votos
        - votos_por_pop
        - geom (polígonos)

    Retorna:
        (moran_i_votos, moran_i_votos_por_pop, total_votos)
    ou None se não der para calcular (poucas observações ou variância zero).
    """
    if gdf is None or gdf.empty:
        return None

    if len(gdf) < 3:
        # Poucos municípios, não faz sentido estatístico
        return None

    # Vetores de atributos
    y_votes = gdf["qt_votos"].astype(float).values
    y_prop = gdf["votos_por_pop"].astype(float).values

    # Matriz de pesos (contiguidade de rainha)
    w = libpysal.weights.Queen.from_dataframe(gdf, silence_warnings=True, use_index=True)
    w.transform = "R"
    
    # islands = w.islands 

    # if islands:
    #     print(f"[ISLAND WARNING] Candidato {sq_candidato}:")
    #     print("  Municípios sem vizinhos (ilhas):")
    #     for idx in islands:
    #         row = gdf.iloc[idx]
    #         print(f"    index={idx}, id_municipio={row['id_municipio']}, qt_votos={row['qt_votos']}")
    #     print()


    # Se todos os valores forem (quase) iguais, Moran não é informativo
    if np.allclose(y_votes, y_votes[0]):
        moran_votes = None
    else:
        moran_votes = Moran(y_votes, w)

    if np.allclose(y_prop, y_prop[0]):
        moran_prop = None
    else:
        moran_prop = Moran(y_prop, w)

    total_votes = int(y_votes.sum())

    moran_i_votes = moran_votes.I if moran_votes is not None else 0
    moran_i_prop = moran_prop.I if moran_prop is not None else 0

    return moran_i_votes, moran_i_prop, total_votes


# ---------------------------------------------------------------------------
# Inserção na tabela de resultados
# ---------------------------------------------------------------------------

def insert_candidate_moran(conn, sq_candidato, moran_i_votes, moran_i_prop, total_votes, tipo=1):
    """
    Insere uma linha em eleicoes22.calc_moran_dep_e_partido
    para o candidato dado.

    - sequencial_ou_sigla_partido = sq_candidato::text
    - tipo = 1 (candidato)
    - indicador deixado como NULL por enquanto
    - bucket_moran e bucket_moran_proporcional preenchidos depois via UPDATE
    """
    sql = """
        INSERT INTO eleicoes22.calc_moran_dep_e_partido (
            sequencial_ou_sigla_partido,
            tipo,
            moran_i,
            bucket_moran,
            votos,
            moran_i_proporcional,
            bucket_moran_proporcional
        )
        VALUES (%s, %s, %s, NULL, %s, %s, NULL)
        ON CONFLICT (sequencial_ou_sigla_partido) DO NOTHING
    """
    with conn.cursor() as cur:
        cur.execute(
            sql,
            (
                str(sq_candidato),
                str(tipo),
                moran_i_votes,
                total_votes,
                moran_i_prop,
            ),
        )


# ---------------------------------------------------------------------------
# Cálculo dos buckets após inserir tudo
# ---------------------------------------------------------------------------

def update_buckets(conn):
    """
    Atualiza os buckets (inteiros) em função do valor de Moran.

    Regra exemplo:
        <= -0.5  -> -2 (muito negativo)
        (-0.5,-0.1] -> -1 (negativo)
        (-0.1,0.1)  -> 0  (próximo de zero)
        [0.1,0.5)   -> 1  (positivo)
        >= 0.5      -> 2  (muito positivo)
    Ajuste como quiser.
    """
    sql = """
        UPDATE eleicoes22.calc_moran_dep_e_partido
        SET
            bucket_moran = CASE
                WHEN moran_i IS NULL THEN NULL
                WHEN moran_i <= -0.5 THEN -2
                WHEN moran_i <= -0.1 THEN -1
                WHEN moran_i < 0.1 THEN 0
                WHEN moran_i < 0.5 THEN 1
                ELSE 2
            END,
            bucket_moran_proporcional = CASE
                WHEN moran_i_proporcional IS NULL THEN NULL
                WHEN moran_i_proporcional <= -0.5 THEN -2
                WHEN moran_i_proporcional <= -0.1 THEN -1
                WHEN moran_i_proporcional < 0.1 THEN 0
                WHEN moran_i_proporcional < 0.5 THEN 1
                ELSE 2
            END
    """
    with conn.cursor() as cur:
        cur.execute(sql)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    engine = get_sqlalchemy_engine()
    conn = get_psycopg2_conn()
    conn.autocommit = False

    try:
        logging.info("Buscando candidatos distintos na view...")
        if USE_PARTY:
            candidates = fetch_distinct_parties(conn)
        else:
            candidates = fetch_distinct_candidates(conn)
    

        logging.info("Total de candidatos encontrados: %d", len(candidates))

        processed = 0
        skipped = 0

        for i, sq_candidato in enumerate(tqdm(candidates, desc="Processando candidatos"), start=1):
            # Verifica se já existe na tabela de resultados
            if item_already_processed(conn, sq_candidato):
                skipped += 1
                continue

            # logging.info("(%d/%d) Carregando dados do candidato %s",
            #              i, len(candidates), sq_candidato)

            if USE_PARTY:
                gdf = load_party_geodata(engine, sq_candidato)
            else:
                gdf = load_candidate_geodata(engine, sq_candidato)

            result = compute_moran_for_candidate(gdf, sq_candidato=sq_candidato)
            if result is None:
                # logging.info("Candidato %s sem dados suficientes para Moran, pulando.",
                #              sq_candidato)
                skipped += 1
                continue

            moran_i_votes, moran_i_prop, total_votes = result

            # logging.info(
            #     "Candidato %s: Moran qt_votos = %s ; Moran votos_por_pop = %s ; votos totais = %d",
            #     sq_candidato,
            #     moran_i_votes,
            #     moran_i_prop,
            #     total_votes,
            # )

            tipo = 2 if USE_PARTY else 1

            insert_candidate_moran(conn, sq_candidato, moran_i_votes, moran_i_prop, total_votes, tipo=tipo)
            processed += 1

            # Commit periódico
            if processed % 50 == 0:
                conn.commit()

        # Commit final dos inserts
        conn.commit()
        logging.info("Inserções concluídas. Processados: %d, pulados: %d", processed, skipped)

        # Atualiza buckets
        logging.info("Atualizando buckets...")
        update_buckets(conn)
        conn.commit()
        logging.info("Buckets atualizados.")

    except Exception as e:
        logging.exception("Erro durante a execução")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()
        engine.dispose()


if __name__ == "__main__":
    main()
