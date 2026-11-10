from  database import conexao,cursor

def tabela_categoria_problema():
    sql = (
        "CREATE TABLE IF NOT EXISTS categoria_problema ("
        "id SERIAL PRIMARY KEY, " 
        "id_problema INTEGER NOT NULL, "
        "gravidade INTEGER NOT NULL, "
        "FOREIGN KEY (id_problema) REFERENCES problema(id) "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()


def create_categoria_problema(id_problema, gravidade):
    try:
        sql = (
            "INSERT INTO categoria_problema "
            "(id_problema, gravidade) "
            "VALUES "
            "(%s, %s)"
        )
        cursor.execute(sql, (id_problema, gravidade))
        conexao.commit()
        return {"id_problema": id_problema, "gravidade": gravidade}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao criar dados {e}')
        return False
    finally:
        cursor.close()
        conexao.close()


def read_categoria_problema():
    try:
        sql =(
            "SELECT categoria_problema.id, problema.problema, categoria_problema.gravidade "
            "FROM categoria_problema "
            "JOIN problema ON categoria_problema.id_problema = problema.id "
        )
        cursor.execute(sql)
        resultados = cursor.fetchall()
        lista_categoria_problemas = []

        for categoria in resultados:
            id_categoria_problema, problema, gravidade = categoria
            lista_categoria_problemas.append({"id_categoria_problema": id_categoria_problema, "problema": problema, "gravidade":gravidade})
        return lista_categoria_problemas
    except Exception as e:
        conexao.rollback()
        print(F'Erro ao ler dados {e}')
    finally:
        cursor.close()
        conexao.close()


def update_categoria_problema(nova_gravidade, id_categoria):
    try:
        sql = (
            "UPDATE categoria_problema "
            "SET gravidade = %s "
            "WHERE id = %s "
        )
        cursor.execute(sql, (nova_gravidade, id_categoria))
        conexao.commit()
        return {"nova_gravidade": nova_gravidade, "id_categoria_problema": id_categoria}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar dados {e}')
    finally:
        cursor.close()
        conexao.close()


def delete_categoria_problema(id_categoria):
    try:
        sql = (
            "DELETE FROM categoria_problema "
            "WHERE id = %s "
        )
        cursor.execute(sql, (id_categoria, ))

        if cursor.rowcount == 0:
            conexao.rollback()
            return None

        conexao.commit()
        return {"id_categoria": id_categoria, "status": "Deletado"}
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao apagar dados {e}')
        return False
    finally:
        cursor.close()
        conexao.close()