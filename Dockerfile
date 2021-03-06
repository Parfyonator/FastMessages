FROM python:3.8

WORKDIR /app

COPY api.py requirements.txt ./

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "api.py" ]
