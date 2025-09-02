# Aleo Offline Signing Tool

## Overview

The offline signing tool enables secure, air-gapped signing of Aleo transactions. It is designed for environments where private keys must remain offline, providing a workflow for generating, signing, and preparing Aleo transactions without exposing sensitive credentials to the internet.

## Features

- **Key Generation:** Use the included `aleo-key-gen` binary to generate Aleo keypairs securely.
- **Program Support:** Compatible with Aleo mainnet programs such as `credits.aleo`, `token_registry.aleo`, and `vlink_council_v03.aleo`.
- **Offline Signing:** Sign transactions locally, ensuring private keys never leave the offline environment.
- **Interoperability:** Signed transactions can be transferred to an online broadcaster for submission to the Aleo network.

## Directory Structure

- `aleo-key-gen`: Binary for Aleo keypair generation.
- `programs/`: Contains Aleo program files for transaction creation.
	- `credits.aleo`
	- `token_registry.aleo`
	- `vlink_council_v03.aleo`

## Usage

### 1. Key Generation

Run the key generation binary in your offline environment:
```bash
./aleo-key-gen authorize_pk <privateKey> <network> <gas_fee> <dest_program_name> propose <proposal_id>  <proposal_hash > auth.raw

Example:
authorize_pk <privateKey> mainnet 150000 vlink_council_v03.aleo propose 1u32 4792523426430471532711464760825230956840456088329954363345840494666188056448field > auth.raw
```


Follow the prompts to securely generate and store your Aleo keypair.

### 2. Prepare Transaction

- Use the Aleo program files in `programs/` to construct your transaction.
- Prepare the transaction data according to the program's requirements.

### 3. Sign Transaction

- Use your offline signing tool to sign the transaction with your private key.
- Ensure the signed transaction is saved in a transferable format (e.g., JSON or raw).

### 4. Broadcast Transaction

- Transfer the signed transaction to an online environment.
- Use the broadcaster tool (see `broadcaster/README.md`) to submit the transaction to the Aleo network.

## Security Recommendations

- Always keep your private keys in the offline environment.
- Verify all transaction data before signing.
- Use secure methods (e.g., USB, QR code) to transfer signed transactions.

## License

See `LICENSE` for details.
