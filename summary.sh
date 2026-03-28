#!/usr/bin/env bash
set -euo pipefail

IMAGE_TAG="customer-analytics:latest"
CONTAINER_NAME="customer-analytics-pipeline"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
RAW_DATA_HOST="${1:-${SCRIPT_DIR}/results/data_raw.csv}"
RAW_DATA_NAME="$(basename "${RAW_DATA_HOST}")"
RAW_DATA_CONTAINER="/app/pipeline/${RAW_DATA_NAME}"

if [ ! -f "${RAW_DATA_HOST}" ]; then
  echo "Raw data file not found: ${RAW_DATA_HOST}"
  echo "Provide a raw dataset file at results/data_raw.csv or pass a path to summary.sh."
  exit 1
fi

mkdir -p "${RESULTS_DIR}"

echo "[1/5] Building Docker image: ${IMAGE_TAG}"
docker build -t "${IMAGE_TAG}" "${SCRIPT_DIR}"

echo "[2/5] Removing any previous container: ${CONTAINER_NAME}"
docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true

echo "[3/5] Starting container (detached): ${CONTAINER_NAME}"
docker run -d --name "${CONTAINER_NAME}" "${IMAGE_TAG}" tail -f /dev/null >/dev/null

cleanup() {
  echo "[5/5] Stopping/removing container: ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[4/5] Copying raw data into container"
docker cp "${RAW_DATA_HOST}" "${CONTAINER_NAME}:${RAW_DATA_CONTAINER}"

echo "[5/5] Running pipeline inside container"
docker exec "${CONTAINER_NAME}" python /app/pipeline/ingest.py "${RAW_DATA_CONTAINER}"

echo "Copying outputs to: ${RESULTS_DIR}"
OUTPUTS=(
  "data_raw.csv"
  "data_preprocessed.csv"
  "insight1.txt"
  "insight2.txt"
  "insight3.txt"
  "summary_plot.png"
  "clusters.txt"
)

for f in "${OUTPUTS[@]}"; do
  docker cp "${CONTAINER_NAME}:/app/pipeline/${f}" "${RESULTS_DIR}/${f}"
done

echo "Done. Results are in: ${RESULTS_DIR}"
