#!/usr/bin/env python3
import json
from io import BytesIO
import time
import argparse
import sys
import re
import requests
import pycurl

# ------------------------------
# STEP 1: Normalize Authorization JSON
# ------------------------------

def normalize_auth(raw_file: str) -> dict:
    """Extract and normalize authorization JSON from raw file."""
    t = open(raw_file, "r", encoding="utf-8", errors="ignore").read()

    def try_decode(x):
        c = 0
        while isinstance(x, str) and c < 4:
            try:
                x = json.loads(x)
            except:
                break
            c += 1
        if isinstance(x, dict) and len(x) == 1:
            (k, v), = x.items()
            if isinstance(v, str):
                try:
                    x = json.loads(v)
                except:
                    pass
        return x

    best = None
    stack = 0
    start = None
    in_str = False
    esc = False
    for i, ch in enumerate(t):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                if stack == 0:
                    start = i
                stack += 1
            elif ch == "}" and stack > 0:
                stack -= 1
                if stack == 0 and start is not None:
                    cand = t[start:i+1]
                    if best is None or len(cand) > len(best):
                        best = cand

    obj = None
    for candidate in [best, t]:
        if not candidate:
            continue
        try:
            x = json.loads(candidate)
            x = try_decode(x)
            if isinstance(x, dict):
                obj = x
                break
        except:
            pass

    if not isinstance(obj, dict):
        sys.exit("Could not normalize authorization JSON. Inspect auth.raw.")

    return obj

# ------------------------------
# STEP 2: RPC + Transaction Logic
# ------------------------------

# RPC URL
RPC_URL = "https://mainnet.aleorpc.com"

def get_program_code_string(program_name: str) -> str:
    """Fetch the `program_name` program details."""
    response = requests.get(f"https://api.explorer.provable.com/v1/mainnet/program/{program_name}")
    return response.json()

def rpc_request(payload: dict) -> str:
    """Send an RPC request to Aleo node and return response string."""
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, RPC_URL)
    c.setopt(c.POST, True)
    c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
    c.setopt(c.POSTFIELDS, json.dumps(payload))
    c.setopt(c.WRITEDATA, buffer)

    c.perform()
    c.close()

    return buffer.getvalue().decode("utf-8")

def generate_transaction(program_name: str, function_name: str, auth_payload: dict):
    """Generate and broadcast a transaction."""
    program_imports: dict = {}
    program_code = get_program_code_string(program_name)

    imports = re.findall(r"import\s+([a-zA-Z0-9_\.]+)", program_code)
    for imp in imports:
        program_imports[str(imp)] = get_program_code_string(imp)

    auth = auth_payload["authorization"]
    fee_auth = auth_payload["fee_authorization"]

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "generateTransaction",
        "params": {
            "authorization": auth,
            "program": program_code,
            "fee_authorization": fee_auth,
            "function": function_name,
            "broadcast": True,
            "imports": program_imports,
        },
    }

    print(">>> Generating transaction...")
    response = rpc_request(data)
    print("Response:", response)
    return response

def get_generated_transaction(request_id: str):
    """Fetch generated transaction by request_id."""
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getGeneratedTransaction",
        "params": {
            "request_id": request_id,
        },
    }

    print(f">>> Fetching transaction with request_id {request_id}...")
    response = rpc_request(data)
    print("Response:", response)
    return response

def broadcast_transaction(program_name, func_name, auth_payload):
    """Generate and broadcast a transaction, then fetch the result."""
    resp = generate_transaction(program_name, func_name, auth_payload)
    try:
        resp_json = json.loads(resp)
        req_id = resp_json.get("result")
        time.sleep(10)
        get_generated_transaction(req_id)
    except (AttributeError, TypeError, json.decoder.JSONDecodeError) as e:
        print("Could not extract request_id automatically. Error:", e)
        print("Please provide the request_id manually for fetching transaction.")

# ------------------------------
# MAIN
# ------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize auth.raw and broadcast Aleo transaction via RPC.")
    parser.add_argument("--program_name", required=True, help="Aleo program name")
    parser.add_argument("--func_name", required=True, help="Function name to call")
    parser.add_argument("--auth_raw", required=True, help="Path to raw auth file")

    args = parser.parse_args()

    # Normalize auth.raw -> dict
    try:
        auth_payload = normalize_auth(args.auth_raw)
    except Exception as e:
        print(f"Error normalizing auth_raw: {e}")
        sys.exit(1)

    broadcast_transaction(args.program_name, args.func_name, auth_payload)
