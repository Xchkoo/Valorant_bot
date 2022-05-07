FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./requirements.txt /tmp/

ENV PATH="${PATH}:/root/.local/bin"

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN rm requirements.txt

COPY ./ /app/
