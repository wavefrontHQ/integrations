# Telegraf agent configured for Wavefront output intended to be used as it's own deployment to collect metrics

FROM wavefronthq/telegraf:latest

ENV ECS_CONTAINER_METADATA_ENDPOINT=""

ENV WAVEFRONT_PROXY=wavefront-proxy
ENV WAVEFRONT_PROXY_PORT=2878
ENV SOURCE_OVERRIDE=address

ENV INTERVAL=10s

RUN mkdir -p /etc/telegraf/telegraf.d

COPY telegraf.conf /etc/telegraf/telegraf.conf

CMD ["telegraf", "--config", "/etc/telegraf/telegraf.conf", "--config-directory", "/etc/telegraf/telegraf.d"]
