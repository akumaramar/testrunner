FROM fluent/fluentd:v1.16.3-debian-1.0

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    ruby-dev \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Elasticsearch plugin
RUN gem install fluent-plugin-elasticsearch --no-document

COPY fluent.conf /fluentd/etc/

USER fluent

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD curl -f http://localhost:24224 || exit 1
