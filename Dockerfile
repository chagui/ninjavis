FROM python:3.7.2

ENTRYPOINT ["python", "ninjavis.py"]
WORKDIR /home

COPY requirements.txt /tmp/.
RUN pip install --upgrade pip -r /tmp/requirements.txt

COPY ninjavis.py .
COPY templates templates/