FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04


RUN apt update && \
  apt install -y \
  wget \
  bzip2 \
  build-essential \
  git \
  git-lfs \
  curl \
  ca-certificates \
  libsndfile1-dev \
  libgl1 \
  python3 \
  python3-pip \
  python3.10-venv


WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

RUN pip install -U pip && pip install -r requirements.txt

