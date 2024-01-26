FROM scilus/scilus:1.6.0

RUN apt update && apt install -y \
        git \
        python3-venv \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pipx && \
    python3 -m pipx ensurepath && \
    pipx install hatch
