#!/bin/bash
# ACCT Sovereign Sentinel: Native Node Deployment (v1.6.3)
# Usage: ./node_deployment.sh [MODEL_PATH] [PORT]

MODEL=${1:-"model.gguf"}
PORT=${2:-8080}
THRESHOLD=80

echo "[SOVEREIGN] Initializing Sentinel Node on port $PORT..."
echo "[SOVEREIGN] Model: $MODEL"
echo "[SOVEREIGN] Effort Axiom: Throttling at $THRESHOLD% CPU..."

# Deploy the llama-server with Native Effort Scaling
# Note: This assumes llama-server is in the PATH or same directory
./llama-server \
  -m "$MODEL" \
  --port "$PORT" \
  --bucket-mul \
  --bucket-mul-cpu-threshold "$THRESHOLD" \
  --host 0.0.0.0 \
  --n-gpu-layers -1 # Use all VRAM available

# If the server crashes, ACCT Telemetry will log it
if [ $? -ne 0 ]; then
    echo "[CRITICAL] Sentinel Node failed to initialize. Check iron status."
    exit 1
fi
