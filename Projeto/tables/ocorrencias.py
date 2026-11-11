from database import get_connection


def tabela_ocorrencias():
    conexao = get_connection()
    cursor = conexao.cursor()
    sql = (
        "CREATE TABLE IF NOT EXISTS ocorrencias ("
        "id SERIAL PRIMARY KEY, "
        "id_categoria_p INTEGER NOT NULL, "
        "id_bairros INTEGER NOT NULL, "
        "ativo BOOLEAN DEFAULT TRUE, "
        "FOREIGN KEY (id_categoria_p) REFERENCES categoria_problema(id), " 
        "FOREIGN KEY (id_bairros) REFERENCES bairros(id) "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()
    cursor.close()
    conexao.close()


def create_ocorrencias(id_categoria, id_bairro):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "INSERT INTO ocorrencias "
            "(id_categoria_p, id_bairros) "
            "VALUES "
            "(%s, %s) "
        )
        cursor.execute(sql, (id_categoria, id_bairro))
        conexao.commit()
        return {"id_categoria": id_categoria, "id_bairro": id_bairro, "ativo": True}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao criar ocorrencias {e}')
        return False
    finally:
        cursor.close()
        conexao.close()


def read_ocorrencias():
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "SELECT "
            "ocorrencias.id, "
            "bairros.bairro, "
            "problema.problema, "
            "categoria_problema.gravidade, "
            "ocorrencias.ativo "
            "FROM ocorrencias "
            "JOIN categoria_problema ON ocorrencias.id_categoria_p = categoria_problema.id "
            "JOIN problema ON categoria_problema.id_problema = problema.id "
            "JOIN bairros ON ocorrencias.id_bairros = bairros.id"
        )
        cursor.execute(sql)
        resultados = cursor.fetchall()

        lista_ocorrencias = []
        for linha in resultados:
            id_ocorrencia, nome_bairro, nome_problema, gravidade, ativo = linha
            lista_ocorrencias.append({
                "id": id_ocorrencia,
                "bairro": nome_bairro,
                "problema": nome_problema,
                "gravidade": gravidade,
                "ativo": ativo
            })

        return lista_ocorrencias
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao ler ocorrências: {e}")
    finally:
        cursor.close()
        conexao.close()


def update_ocorrencias(id_ocorrencias):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "UPDATE ocorrencias "
            "SET ativo = False "
            "WHERE id = %s "
        )
        cursor.execute(sql, (id_ocorrencias, ))
        conexao.commit()
        return {"id_ocorrencia": id_ocorrencias, "ativo": False, "status": "Resolvida"}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar ocorrencias {e}')
    finally:
        cursor.close()
        conexao.close()


def delete_ocorrencias(id_ocorrencia):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "DELETE FROM ocorrencias "
            "WHERE id = %s "
        )
        cursor.execute(sql, (id_ocorrencia,))

        if cursor.rowcount == 0:
            conexao.rollback()
            return None

        conexao.commit()
        return {"id_ocorrencia": id_ocorrencia, "status": "Deletado"}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao deletar ocorrencia {e}')
        return False
    finally:
        cursor.close()
        conexao.close()
