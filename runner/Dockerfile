FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends nmap ca-certificates && rm -rf /var/lib/apt/lists/* && useradd --uid 10001 --create-home nexo
WORKDIR /app
COPY server.py /app/server.py
USER 10001:10001
EXPOSE 8080
CMD ["python", "-B", "/app/server.py"]
