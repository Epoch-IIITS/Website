FROM python:3.13-slim

# One thread per job: deterministic results and matched to --cpus 1. Tracing stays off so
# LangChain never tries to reach the network. HOME points at the per-container tmpfs.
ENV OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    LANGSMITH_TRACING=false \
    LANGCHAIN_TRACING_V2=false \
    HOME=/tmp

COPY requirements.txt /opt/learn/requirements.txt
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.14.1 \
    && pip install --no-cache-dir -r /opt/learn/requirements.txt
COPY runner.py /opt/learn/runner.py
USER 65534:65534
WORKDIR /tmp
CMD ["python", "-I", "/opt/learn/runner.py"]
