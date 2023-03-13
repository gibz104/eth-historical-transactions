# <h1 align="center">eth-historical-transactions</h1>

**Web3.py script that downloads all transactions from mined ethereum blocks and saves them to a SQLite database file.**

[![Test OS](https://img.shields.io/badge/runs_on-ubuntu_|_mac_os_|_windows-blue.svg)](https://github.com/gibz104/google-sheets-writer/actions/workflows/tests.yaml)

# Example

Must provide a starting block (-s), ending block (-e), and block increment amount (-i).

`python3 web3_get_historical_tx.py -s 12000000 -e 12000100 -i 10`

