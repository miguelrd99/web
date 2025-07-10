#!/bin/bash
export STREAMLIT_CONFIG_FILE=".streamlit/config.toml"
python -m streamlit run prueba_spark.py --server.port 8000 --server.address 0.0.0.0
