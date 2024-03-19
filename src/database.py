from contextlib import contextmanager
import mysql.connector

# Configurações do banco de dados.
DB_CONFIG = {
    'host': "jarves.mysql.dbaas.com.br",
    'user': "jarves",
    'password': "Kawai312967@",
    'database': "jarves"
}


@contextmanager
def db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def db_cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def get_db_connection():
    """Estabelece e retorna a conexão com o banco de dados."""
    return mysql.connector.connect(**DB_CONFIG)


def execute_query(connection, query, data=None):
    """Executa uma query e retorna o cursor."""
    cursor = connection.cursor()
    cursor.execute(query, data)
    return cursor


def existRegistroPortugues(registro):
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                cursor = execute_query(connection, "SELECT COUNT(*) FROM registros WHERE registro = %s", (registro,))
                count = cursor.fetchone()[0]
                return count > 0
    except Exception as e:
        print(f"Erro ao verificar o registro no banco de dados: {e}")
        return False


def existRegistroIngles(registro):
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                cursor = execute_query(connection, "SELECT COUNT(*) FROM registros WHERE registro = %s AND ingles=1",
                                       (registro,))
                count = cursor.fetchone()[0]
                return count > 0
    except Exception as e:
        print(f"Erro ao verificar o registro no banco de dados: {e}")
        return False


def inserir_registro(registro, tipo, ingles, portugues, espanhol):
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                cursor = execute_query(connection, "SELECT registro FROM registros WHERE registro = %s", (registro,))
                existing_record = cursor.fetchone()
                if not existing_record:
                    logging.info(f'Adicionando a palavra - {registro}')
                    execute_query(connection,
                                  "INSERT INTO registros (registro, tipo, portugues, ingles, espanhol, processado, processVezes) "
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                  (registro, tipo, portugues, ingles, espanhol, 0, 0))
                connection.commit()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def inserirRegistroPortugues(registro, tipo, portugues, morf):
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                cursor = execute_query(connection, "SELECT registro FROM registros WHERE registro = %s", (registro,))
                existing_record = cursor.fetchone()
                if not existing_record:
                    logging.info(f'Adicionando a palavra - {registro}')
                    execute_query(connection,
                                  "INSERT INTO registros (registro, tipo, portugues, processado, morf) "
                                  "VALUES (%s, %s, %s, %s, %s)",
                                  (registro, tipo, portugues, 0, morf))
                connection.commit()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def inserirRegistroIngles(registro, tipo, ingles, morf):
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                cursor = execute_query(connection, "SELECT registro FROM registros WHERE registro = %s", (registro,))
                existing_record = cursor.fetchone()
                if not existing_record:
                    logging.info(f'Adicionando a palavra - {registro}')
                    execute_query(connection,
                                  "UPDATE registros SET ingles = %s WHERE registro = %s",
                                  (ingles, registro))
                connection.commit()
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")


def criar_tabela_registros():
    try:
        with db_connection() as connection:
            with db_cursor(connection) as cursor:
                execute_query(connection, """
                CREATE TABLE IF NOT EXISTS registros (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    registro VARCHAR(255) NOT NULL UNIQUE,
                    tipo VARCHAR(255),
                    ingles TINYINT(1) DEFAULT 0,
                    espanhol TINYINT(1) DEFAULT 0,
                    portugues TINYINT(1) DEFAULT 0,
                    processado TINYINT(1) DEFAULT 0,
                    processVezes INT DEFAULT 0 NOT NULL,
                    morfologia VARCHAR(255)
                )
                """)
    except mysql.connector.Error as e:
        print(f"Erro ao criar tabela de registros no banco de dados: {e}")


def palavra_presente_na_tabela(conexao, palavra):
    """Verifica se a palavra está presente na tabela de registros."""
    with db_connection() as connection:
        with db_cursor(connection) as cursor:
            consulta = "SELECT 1 FROM registros WHERE registro = %s"
            cursor.execute(consulta, (palavra,))
            return cursor.fetchone() is not None


def insert_metadata(column, collection_name, tipo_dado, data_ultima_utilizacao):
    """Insere metadados na tabela metadata."""
    with db_connection() as connection:
        with db_cursor(connection) as cursor:
            cursor.execute("""
                INSERT INTO metadata (column_name, collection_name, tipo_dado, data_ultima_utilizacao) 
                VALUES (%s, %s, %s, %s)
            """, (column, collection_name, tipo_dado, data_ultima_utilizacao))
            connection.commit()


def create_metadata_table_if_not_exists():
    """Cria a tabela metadata se ela não existir."""
    with db_connection() as connection:
        with db_cursor(connection) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    column_name VARCHAR(255),
                    collection_name VARCHAR(255),
                    tipo_dado VARCHAR(255),
                    data_ultima_utilizacao DATETIME
                )
            """)


def obter_resposta_padrao(pergunta):
    with db_connection() as connection:
        with db_cursor(connection) as cursor:
            cursor.execute(f"SELECT resposta FROM respostas_padrao WHERE pergunta = '{pergunta}'")
            result = cursor.fetchone()

            if result:
                return result[0]
            return None


def inserir_syn_ant(word, synonyms, antonyms):
    try:
        with db_connection() as connection:
            # Verifique se a palavra já existe na tabela
            with db_cursor(connection) as cursor:
                cursor.execute("SELECT word FROM syn_ant WHERE word = %s", (word,))
                existing_record = cursor.fetchone()

            # Se não existe, insira
            if not existing_record:
                synonyms_str = ",".join(synonyms)
                antonyms_str = ",".join(antonyms)

                with db_cursor(connection) as cursor:
                    cursor.execute("INSERT INTO syn_ant (word, synonyms, antonyms) VALUES (%s, %s, %s)",
                                   (word, synonyms_str, antonyms_str))
                    connection.commit()
                    print(f'Inserido {word} com sinônimos e antônimos.')
            else:
                print(f'{word} já está presente na base.')

    except Exception as e:
        print(f"Erro ao inserir sinônimos e antônimos no banco de dados: {e}")
