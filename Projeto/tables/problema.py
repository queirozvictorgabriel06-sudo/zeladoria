from database import get_connection


def tabela_problema():
    conexao = get_connection()
    cursor = conexao.cursor()
    sql = (
        "CREATE TABLE IF NOT EXISTS problema (" 
        "id SERIAL PRIMARY KEY, "
        "problema VARCHAR(50) NOT NULL "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()
    cursor.close()
    conexao.close()


def create_problema(problema):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "INSERT INTO problema "
            "(problema) "
            "VALUES "
            "(%s)"
        )
        cursor.execute(sql, (problema, ))
        conexao.commit()
        return {"problema": problema}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao colocar problema {e}')
    finally:
        cursor.close()
        conexao.close()


def read_problema():
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "SELECT * FROM problema "
        )
        cursor.execute(sql)
        resultados = cursor.fetchall()

        lista_problemas = []
        for problemas in resultados:
            id, problema = problemas
            lista_problemas.append({"id_problema": id, "problema": problema})

        return lista_problemas
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao ler problemas {e}')
    finally:
        cursor.close()
        conexao.close()


def update_problema(novo_problema, id_problema):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "UPDATE problema "
            "SET problema = %s "
            "WHERE id = %s "
        )
        cursor.execute(sql, (novo_problema, id_problema))
        conexao.commit()
        return {"novo_problema": novo_problema, "id_problema": id_problema}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar o problema {e}')
    finally:
        cursor.close()
        conexao.close()


def delete_problema(id_problema):
    conexao = get_connection()
    cursor = conexao.cursor()
    try:
        sql = (
            "DELETE FROM problema "
            "WHERE id = %s "
        )
        cursor.execute(sql, (id_problema, ))
        conexao.commit()
        return {"id_problema": id_problema, "status": "Deletado"}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao deletar o problema {e}')
    finally:
        cursor.close()
        conexao.close()

