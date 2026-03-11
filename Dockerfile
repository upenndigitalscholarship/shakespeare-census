FROM python:3.6-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk update \
    && apk add --virtual build-deps \
        gcc \
        python3-dev \
        musl-dev \
        postgresql-dev \
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        libffi-dev

# Install pip packages
COPY ./requirements.txt ./code/requirements.txt
RUN pip install -r /code/requirements.txt

# Cleanup build artifacts
RUN find /usr/local -type f -name "*.pyc" -delete \
    && find /usr/local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM python:3.6-alpine AS release

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code

# Install runtime dependencies
RUN apk update \
    && apk add --no-cache \
        libpq \
        libjpeg \
        zlib \
        freetype \
        libffi \
        gettext \
        postgresql-client \
        curl \
    && rm -rf /var/cache/apk/*

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . /code/

WORKDIR /code

# Default command - can be overridden
CMD ["gunicorn", "-c", "/code/gunicorn.conf.py", "config.wsgi"]

ENV X_IMAGE_TAG=v0.0.0

LABEL Description="Shakespeare Census Image" Vendor="REVSYS"
LABEL Version="${X_IMAGE_TAG}"
