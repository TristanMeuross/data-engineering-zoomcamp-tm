import os
import argparse

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_file = 'output.parquet'

    os.system(f"wget {url} -O {parquet_file}")

    taxi_df = pd.read_parquet(parquet_file)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("Creating table...")
    taxi_df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    print("Finished creating table")

    print("Inserting data...")
    taxi_df.to_sql(name=f'{table_name}', con=engine, if_exists='append')
    print("Finished inserting data")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)