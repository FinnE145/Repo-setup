# Pinned to the exact patch tag, not a floating minor tag -- a floating tag
# would silently move the production interpreter on an unrelated rebuild.
# Match the laptop's version exactly.
FROM python:{{PYTHON_VERSION}}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Matches finne's uid:gid on the host, so bind-mounted files under /data stay
# Finn-owned rather than becoming root-owned.
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --create-home app && chown -R 1000:1000 /app
USER 1000:1000

EXPOSE {{PORT}}

CMD [{{ENTRYPOINT, e.g. "python", "serve.py"}}]
