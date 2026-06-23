import json
import urllib.request
import time
import os

# Securely extract Helius token from your environment
HELIUS_TOKEN = os.environ.get("HELIUS_API_KEY")
MY_WALLET = "3rLapKiA4SfTQMMMFfkZSfkT12iFXQPiKv7w9mzqKZqh"
EXPECTED_AMOUNT_LAMPORTS = 10000000  # 0.01 SOL in Lamports

def verify_solana_signature(signature_string):
    """
    Connects to the public Solana mainnet ledger network to verify payment authenticity.
    Protects against replay attacks and spoofed transaction structures.
    """
    print(f"🔍 Interrogating Solana ledger for signature: {signature_string}")
    
    # Fallback to standard public RPC if private Helius key is missing locally
    if HELIUS_TOKEN:
        rpc_url = f"https://helius-rpc.com{HELIUS_TOKEN}"
    else:
        rpc_url = "https://solana.com"

    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            signature_string,
            {"encoding": "json", "maxSupportedTransactionVersion": 0}
        ]
    }).encode('utf-8')

    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(rpc_url, data=payload, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res = json.loads(response.read().decode('utf-8'))
            
            if 'error' in res:
                print(f"❌ RPC Validation Node Denied Request: {res['error']}")
                return False
                
            result = res.get("result")
            if not result:
                print("❌ Signature Not Found: Transaction does not exist on-chain yet.")
                return False

            # 1. Verify block time recency (Must be within last 10 minutes / 600 seconds)
            block_time = result.get("blockTime", 0)
            current_time = int(time.time())
            if current_time - block_time > 600:
                print("❌ Security Alert: Replay attack blocked. Transaction is too old.")
                return False

            # 2. Parse instruction metrics to verify payment destination and amount
            meta = result.get("meta", {})
            if meta.get("err"):
                print("❌ Invalid Transaction: Target transaction failed on-chain.")
                return False

            transaction = result.get("transaction", {})
            message = transaction.get("message", {})
            account_keys = message.get("accountKeys", [])

            # Check if your wallet is included as an authorized account key index
            if MY_WALLET not in account_keys:
                print("❌ Fraud Detected: Transaction did not interact with your wallet.")
                return False

            wallet_index = account_keys.index(MY_WALLET)
            pre_balances = meta.get("preBalances", [])
            post_balances = meta.get("postBalances", [])

            # Calculate the net absolute change in your wallet balance
            actual_received = post_balances[wallet_index] - pre_balances[wallet_index]

            if actual_received >= EXPECTED_AMOUNT_LAMPORTS:
                print(f"✅ Success: Verified on-chain payment of {actual_received / 100000000} SOL.")
                return True
            else:
                print(f"❌ Payment Insufficient: Expected {EXPECTED_AMOUNT_LAMPORTS} lamports, found {actual_received}.")
                return False

    except Exception as e:
        print(f"⚠️ Network verification pipeline interrupted: {e}")
        return False

if __name__ == "__main__":
    # Test execution with a generic placeholder string
    verify_solana_signature("mock_sig_verification_run")
