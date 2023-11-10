FROM python:3.10
WORKDIR /Kirby42Bot
COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


CMD ["python twitch-irc.py"]