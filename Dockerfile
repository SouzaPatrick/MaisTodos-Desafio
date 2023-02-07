FROM python:3.10.8-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements/base-requirements.txt .
COPY requirements/dev-requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt


FROM python:3.10.8-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD ["python", "wsgi.py"]
