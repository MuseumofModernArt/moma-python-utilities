FROM apache/beam_python3.12_sdk:2.58.1 as beam

COPY requirements.txt .
COPY . pipelines/
COPY setup.py .

# Pre-install Python dependencies. For reproducibile builds,
# supply all of the dependencies and their versions in a requirements.txt file.
RUN pip install -r requirements.txt
RUN python3 -m pip install .

# FROM gcr.io/dataflow-templates-base/python312-template-launcher-base:20240812-rc01 as template_launcher
# FROM apache/beam_python3.12_sdk:2.58.1

# FROM python:3.12-slim

# ARG WORKDIR=/dataflow/template
# RUN mkdir -p ${WORKDIR}
# WORKDIR ${WORKDIR}

# RUN apt-get update && \
#     apt-get install -y default-jre && \
#     apt-get install -y ant && \
#     apt-get clean
# RUN apt-get update && apt-get install -y libffi-dev && rm -rf /var/lib/apt/lists/*

# COPY . pipelines/
# COPY setup.py .
# COPY requirements.txt .

# COPY --from=template_launcher /opt/google/dataflow/python_template_launcher /opt/google/dataflow/python_template_launcher
# COPY --from=apache/beam_python3.12_sdk:2.58.1 /opt/apache/beam /opt/apache/beam

# ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
# ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
# ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/pipelines/__init__.py"
# ENV FLEX_TEMPLATE_PYTHON_PY_OPTIONS=""
# ENV FLEX_TEMPLATE_PYTHON_EXTRA_PACKAGES=""

# RUN pip install --no-cache-dir apache-beam[gcp]==2.58.1
# RUN pip install -r requirements.txt
# RUN python3 -m pip install .

# ENTRYPOINT ["/opt/apache/beam/boot"]

# FROM ${FINAL_TARGET} as final