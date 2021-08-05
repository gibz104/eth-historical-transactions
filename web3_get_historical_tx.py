import sys
import json
import sqlite3
import getopt
import pandas as pd
from web3 import Web3


provider = Web3.WebsocketProvider('ws://127.0.0.1:8546')
w3 = Web3(provider)


class DBController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.db_cursor = self.conn.cursor()

    def write_data(self, df, table, index=False, if_table_exists='replace'):
        df.to_sql(name=table, con=self.conn, if_exists=if_table_exists, index=index)
        self.conn.commit()

    def read_data(self, sql_command):
        df = pd.read_sql(sql_command, con=self.conn)
        return df

    def execute_sql(self, sql_command):
        query = self.db_cursor.execute(sql_command)
        self.conn.commit()
        return query

    def close_conn(self):
        self.conn.commit()
        self.conn.close()

    def restart_conn(self):
        self.conn.commit()
        self.conn.close()
        self.conn = sqlite3.connect(self.db_name)


def connectedToNode():
    return w3.isConnected()


def getHistoricalSample(start, end, increment):
    if not connectedToNode():
        sys.exit('not connected to node.')

    DB = DBController('Transactions.db')
    first_run = True
    for block_counter in range(start, end, increment):
        block = w3.eth.get_block(block_counter)
        tx_df = pd.DataFrame(columns=['blockHash', 'blockNumber', 'from', 'gas', 'gasPrice', 'hash', 'input', 'nonce', 'to', 'transactionIndex', 'value', 'type', 'v', 'r', 's'])
        for tx in block.transactions:
            tx_raw = w3.eth.get_transaction(tx)
            tx_json = Web3.toJSON(tx_raw)
            tx_df.loc[len(tx_df)] = dict(json.loads(tx_json))

        if first_run:
            DB.write_data(tx_df.astype(str), 'transactions', if_table_exists='replace')  # cast all values as strings b/c sqlite does not support large integers
        else:
            DB.write_data(tx_df.astype(str), 'transactions', if_table_exists='append')  # cast all values as strings b/c sqlite does not support large integers

        print(f'Read block number {block_counter:,} with {len(tx_df):,} txs')
        first_run = False


argv = sys.argv[1:]
options = 'sei:'
start, end, increment = 0, 0, 0
args, values = getopt.getopt(argv, 's:e:i:')
for currentArgument, currentValue in args:
    if currentArgument in ['-s']:
        start = int(currentValue)

    elif currentArgument in ['-e']:
        end = int(currentValue)

    elif currentArgument in ['-i']:
        increment = int(currentValue)

getHistoricalSample(start, end, increment)
