FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# sets the cuda variables for CUDA support in docker
ENV NVIDIA_VISIBLE_DEVICES 
ENV NVIDIA_DRIVER_CAPABILITIES 

# Installs Poetry, Mypy, Ruff and Monkeytype
RUN pipx install poetry && pipx install mypy && pipx install ruff && pipx install MonkeyType

# copies the requirements file from the project root to the container and installs it
# copy "noop.txt" so the COPY instruction does not fail if no requirements.txt exists.
COPY requirements.txt* .devcontainer/noop.txt /tmp/pip-tmp/
RUN if [ -f "/tmp/pip-tmp/requirements.txt" ]; then pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt; fi \
    && rm -rf /tmp/pip-tmp