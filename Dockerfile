FROM ghcr.io/ministryofjustice/analytical-platform-airflow-python-base:1.19.0@sha256:472d4b7c2067ebef7e8c67f8aa1fcf813a3ca64ad31feb2eed649dc05bd1b08a

ARG MOJAP_IMAGE_VERSION="default"
ENV MOJAP_IMAGE_VERSION=${MOJAP_IMAGE_VERSION}             
                       
# Copy requirements.txt
COPY requirements.txt requirements.txt 

# Copy application code
COPY src/ .

# Install requirements
RUN <<EOF
pip install --no-cache-dir --requirement requirements.txt
EOF

# Switch back to non-root user (analyticalplatform)
# USER ${CONTAINER_UID}

# Execute main.py script
ENTRYPOINT ["python3", "main.py"]
