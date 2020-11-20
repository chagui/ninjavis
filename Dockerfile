FROM python:3.6
RUN pip install ninjavis
ENTRYPOINT ["ninjavis"]

