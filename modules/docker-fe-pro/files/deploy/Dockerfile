# Pinned to the exact patch tag, not a floating minor tag -- a floating tag
# would silently move the production interpreter on an unrelated rebuild.
# Match the laptop's version exactly.
FROM python:{{PYTHON_VERSION}}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# {{ACCOUNT, default svc}} ({{UID, default 2003}}): fe-pro's service account
# (SERVER.md, "Accounts"), which owns /srv/stacks/{{NAME}}/data on the host.
# Never 1000 (finne): that uid is Finn, and root-equivalent. Every writable
# path is under /data, so /app stays root-owned and the service can't rewrite
# its own code.
ENV PYTHONDONTWRITEBYTECODE=1
RUN groupadd --gid {{UID}} {{ACCOUNT}} && useradd --uid {{UID}} --gid {{UID}} --create-home {{ACCOUNT}}
USER {{UID}}:{{UID}}

EXPOSE {{PORT}}

CMD [{{ENTRYPOINT, e.g. "python", "serve.py"}}]
