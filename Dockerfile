FROM docker.io/python:3-slim AS builder

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

RUN apt update && apt install git -y

COPY . /usr/src

WORKDIR /usr/src

RUN python -m pipenv sync

FROM docker.io/python:3-slim AS runner

COPY --from=builder /usr/src/ /usr/src/

WORKDIR /usr/src/

# Activate venv
ENV PATH="/usr/src/.venv/bin:$PATH"

# Replace dash with bash as the default shell
RUN rm -v /bin/sh && ln -svf /bin/bash /bin/sh

# Install CLI
RUN pip install .

CMD ["/usr/src/.venv/bin/python", "src/main.py"]
