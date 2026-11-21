FROM python:3.13.9-slim-bookworm
WORKDIR /bot
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY bot.py arena.py mechfight.py /bot/
USER 65534:65534
ENTRYPOINT ["python3", "-u", "/bot/bot.py"]
