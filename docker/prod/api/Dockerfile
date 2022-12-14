FROM python:3.10.2-alpine3.15 as base
FROM base as builder

RUN mkdir /install
RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    g++ \
    python3-dev \
    musl-dev \
    build-base \
    linux-headers \
    pcre-dev \
    libffi-dev

WORKDIR /install
COPY ./nbapi/requirements/prod.lock.txt /requirements/
RUN pip install -U pip && \
    pip install \
    --no-warn-script-location \
    --prefix=/install \
    -r /requirements/prod.lock.txt

FROM base

ENV USER_ID=1000
ENV GROUP_ID=1000
ENV USER_NAME=api

ENV PYTHONUNBUFFERED 1

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
    pcre-dev \
    libpq

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --chown=${USER_ID}:${GROUP_ID} nbapi /nbapi
COPY --chown=${USER_ID}:${GROUP_ID} ./.env /nbapi/.env
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/prod/api/entrypoint /entrypoint
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/prod/api/start /start
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/prod/api/start-test /start-test
COPY --chown=${USER_ID}:${GROUP_ID} ./docker/prod/celery/worker/start-worker /start-worker

RUN chmod +x /entrypoint && \
    chmod +x /start && \
    chmod +x /start-test && \
    chmod +x /start-worker

WORKDIR /nbapi
USER ${USER_NAME}

ENTRYPOINT ["/entrypoint"]
