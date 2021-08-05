# eth-historical-transactions
Web3 script that downloads all transactions from mined ethereum blocks and saves them to as SQLlite database file.  Must provide a starting block, ending block, and increment amount.

Example:<br/>
**python3 web3_get_historical_tx.py -s 12000000 -e 12000100 -i 10**

Script will print each block that is read and will save "Transactions.db" in working directory


