#!/usr/bin/env bash
set -euo pipefail
ROOT="$(pwd)"
KONG_YML="$ROOT/kong.yml"
SAMPLE_ORIG="$ROOT/sample_data/original.txt"
SAMPLE_SUB="$ROOT/sample_data/submission.txt"
BIG_BIN="$ROOT/big.bin"
CONTAINER_NAME="kong-dbless"
NETWORK_NAME="kong-net"

echo "=== RATE-LIMIT LOOP (8 attempts) ==="
for i in $(seq 1 8); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -F "original=@${SAMPLE_ORIG}" -F "submission=@${SAMPLE_SUB}" http://localhost:8000/check || true)
  echo "attempt $i -> HTTP $code"
  sleep 1
done
echo