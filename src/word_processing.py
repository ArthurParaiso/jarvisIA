import logging
import os
from datetime import datetime

import mysql.connector
import pandas as pd
from pymongo import MongoClient

from src.database import insert_metadata, create_metadata_table_if_not_exists


class DataProcessor:
    def __init__(self, csv_folder, mongo_db, mysql_db):
        self.csv_folder = csv_folder
        self.mongo_db = mongo_db
        self.mysql_db = mysql_db
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console_handler)

    def connect_to_mysql(self):
        return mysql.connector.connect(
            host=self.mysql_db['host'],
            user=self.mysql_db['user'],
            password=self.mysql_db['password'],
            database=self.mysql_db['database']
        )

    def preprocess_csv(self, csv_file):
        logging.info(f"Preprocessing file: {csv_file}")

        df = pd.read_csv(csv_file)

        if df.isnull().values.any():
            logging.warning("Identified missing data. Filling with mean values.")
            numeric_cols = df.select_dtypes(include=[float, int]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        return df

    def save_to_mongodb(self, df, collection_name):
        client = MongoClient('mongodb://localhost:27017/')
        db = client[self.mongo_db['name']]

        if collection_name not in db.list_collection_names():
            collection = db[collection_name]
            data_to_insert = df.iloc[1:].to_dict(orient='records')
            collection.insert_many(data_to_insert)
            logging.info(f"Data inserted into MongoDB collection: {collection_name}")
        else:
            logging.info(f"Collection {collection_name} already exists in MongoDB. Skipping insertion.")

    def process_csv_and_save(self, csv_file):
        df = self.preprocess_csv(csv_file)
        collection_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Obter tipos de dados da segunda linha
        tipos_de_dados = df.iloc[0].tolist()
        tipo_dado = ', '.join(map(str, tipos_de_dados))

        # Registrar a data atual
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_to_mongodb(df, collection_name)

        mysql_conn = self.connect_to_mysql()
        cursor = mysql_conn.cursor()

        create_metadata_table_if_not_exists()

        for column in df.columns:
            insert_metadata(column, collection_name, tipo_dado, data_atual)

        mysql_conn.commit()
        mysql_conn.close()
        logging.info(f"Metadata inserted into MySQL for file: {csv_file}")


if __name__ == "__main__":
    csv_folder_path = "E:\\OneDrive\\Projeto\\Dataset\\DatasetZip\\"
    mongo_db_config = {
        'name': 'jarves'
    }
    mysql_db_config = {
        'host': 'jarves.mysql.dbaas.com.br',
        'user': 'jarves',
        'password': 'Kawai312967@',
        'database': 'jarves'
    }

    processor = DataProcessor(csv_folder_path, mongo_db_config, mysql_db_config)

    for root, dirs, files in os.walk(csv_folder_path):
        for file in files:
            if file.endswith(".csv"):
                csv_file = os.path.join(root, file)
                processor.process_csv_and_save(csv_file)
