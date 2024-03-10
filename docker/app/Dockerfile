FROM python:3.10.6-slim as builder

WORKDIR /opt/py_build/

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        net-tools \
        iputils-ping \
        vim \
        wget \
        unzip \
        build-essential \
        gcc \
        zlib1g \
        libjpeg-dev \
        python3-dev \
        python3-setuptools

COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip wheel -r requirements.txt --wheel-dir ./wheels

FROM python:3.10.6-slim
WORKDIR /opt/signer/
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        procps \
        net-tools \
        iputils-ping \
        vim \
        wget \
        unzip \
        gpg
COPY --from=builder /opt/py_build/wheels /wheels


RUN --mount=type=cache,target=/root/.cache/pip pip install /wheels/*
