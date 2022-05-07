FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./requirements.txt /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py

RUN pip install -r requirements.txt

ENV PATH="${PATH}:/root/.local/bin"

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN rm requirements.txt

COPY ./ /app/
