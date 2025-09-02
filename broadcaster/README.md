# broadcaster.py

## Overview

`broadcast.py` is a command-line tool for normalizing Aleo authorization files and broadcasting transactions to the Aleo chain via RPC. It automates the process of extracting and normalizing authorization JSON, generating transactions, and broadcasting them using Aleo's RPC endpoints.

## Features

- **Authorization Normalization:** Extracts and normalizes JSON from raw authorization files.
- **Transaction Generation:** Generates Aleo transactions using provided program and function names.
- **Broadcasting:** Sends transactions to the Aleo testnet and fetches the result.
- **Imports Handling:** Automatically fetches and includes program imports required for the transaction.

## Requirements

- Python 3
- `requests` and `pycurl` libraries

Install dependencies:
```bash
pip install requests pycurl
```

## Usage

```bash
python broadcast.py --program_name <program_name> --func_name <function_name> --auth_raw <path_to_auth.raw>
```

- `--program_name`: Name of the Aleo program to interact with.
- `--func_name`: Function within the program to call.
- `--auth_raw`: Path to the raw authorization file, output of offline signing tool.

## Example

```bash
python broadcast.py --program_name vlink_council_v03.aleo --func_name propose --auth_raw auth.raw
```

## How It Works

1. **Normalize Authorization:** Reads and normalizes the authorization JSON from the provided file.
2. **Generate Transaction:** Fetches program code and imports, then generates a transaction using Aleo RPC.
3. **Broadcast Transaction:** Broadcasts the transaction and fetches the result using the request ID.

## Error Handling

- If the authorization file cannot be normalized, the script exits with an error.
- If the request ID cannot be extracted automatically, you will be prompted to provide it manually.

## License

See `LICENSE` for details.


