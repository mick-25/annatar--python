# index.py

import os
from datetime import datetime
import logging
import sys

from annatar.main import app  # Adjust the import based on your actual application structure

from prometheus_client import CollectorRegistry, multiprocess
import uvicorn

NUM_CORES = os.cpu_count() or 1
BUILD_VERSION = os.getenv("BUILD_VERSION", "UNKNOWN")
HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
PORT = int(os.getenv("LISTEN_PORT", "8000"))
WORKERS = int(os.getenv("WORKERS", 2 * NUM_CORES))
PROM_DIR = os.getenv(
    "PROMETHEUS_MULTIPROC_DIR", f"/tmp/annatar.metrics-{datetime.now().timestamp()}"
)
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging._nameToLevel[LOG_LEVEL.upper()],  # type: ignore
)

if __name__ == "__main__":
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = PROM_DIR
    if not os.path.isdir(PROM_DIR):
        os.mkdir(PROM_DIR)
    multiprocess.MultiProcessCollector(CollectorRegistry())

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
        workers=WORKERS,
        loop="uvloop",
        log_level="error",
    )
