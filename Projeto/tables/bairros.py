from database import get_connection


def tabela_bairro():
    conexao = get_connection()
    cursor = conexao.cursor()
    sql = (
        "CREATE TABLE IF NOT EXISTS bairros (" 
        "id SERIAL PRIMARY KEY, " 
        "bairro VARCHAR(100) NOT NULL " 
        ")"
    )
    cursor.execute(sql)
    conexao.commit()
    cursor.close()
    conexao.close()


def create_bairro(bairro):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "INSERT INTO bairros "
            "(bairro) "
            "VALUES "
            "(%s)"
        )
        cursor.execute(sql, (bairro, ))
        conexao.commit()
        return {"bairro": bairro}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao criar bairro {e}')
    finally:
        cursor.close()
        conexao.close()


def read_bairro():
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "SELECT * FROM bairros "
        )
        cursor.execute(sql)
        resultados = cursor.fetchall()

        lista_bairro = []
        for bairros in resultados:
            id, bairro = bairros
            lista_bairro.append({"id": id, "bairro": bairro})

        return lista_bairro
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao ler bairros {e}")
    finally:
        cursor.close()
        conexao.close()


def update_bairro(novo_bairro, id_bairro):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "UPDATE bairros "
            "SET bairro = %s "
            "WHERE id = %s "
        )
        cursor.execute(sql, (novo_bairro, id_bairro))
        conexao.commit()
        return {"novo_bairro": novo_bairro, "id": id_bairro}
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao atualizar {e}")
    finally:
        cursor.close()
        conexao.close()


def delete_bairro(id_bairro):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "DELETE FROM bairros "
            "WHERE id = %s "
        )
        cursor.execute(sql, (id_bairro, ))
        conexao.commit()
        return {"id_bairro": id_bairro, "status": "Deletado"}
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao excluir bairro {e}")
    finally:
        cursor.close()
        conexao.close()
