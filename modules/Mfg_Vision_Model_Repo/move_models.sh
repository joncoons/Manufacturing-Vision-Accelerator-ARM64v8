#!/bin/bash

set -e

exec mv -f /models_temp/* /model_volume &
exec python3 /app/main.py 