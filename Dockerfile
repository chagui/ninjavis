FROM python:3.7
RUN pip install ninjavis
ENTRYPOINT ["ninjavis"]

