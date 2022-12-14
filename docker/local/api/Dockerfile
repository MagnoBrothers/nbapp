FROM python:3.11.0-alpine3.16

ENV USER_ID=1000
ENV GROUP_ID=1000
ENV USER_NAME=api

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN addgroup \
    --gid ${GROUP_ID} \
    --system ${USER_NAME} && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup ${USER_NAME} \
    --no-create-home \
    --uid ${USER_ID} \
    ${USER_NAME}

RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    postgresql-client \
    g++ \
    python3-dev \
    musl-dev \
    build-base \
    linux-headers \
    pcre-dev \
    libpq \
    libffi-dev \
    openssl-dev \
    cargo

COPY --chown=${USER_ID}:${GROUP_ID} ./nbapi/requirements/local.lock.txt /requirements/

RUN pip install -U pip wheel && \
    pip install -r /requirements/local.lock.txt

COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/entrypoint /entrypoint
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/start /start
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/api/start-test /start-test
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/local/huey/start-worker /start-worker

RUN chmod +x /entrypoint && \
    chmod +x /start && \
    chmod +x /start-test && \
    chmod +x /start-worker

WORKDIR /nbapi/
USER ${USER_NAME}

ENTRYPOINT [ "/entrypoint" ]
