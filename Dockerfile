FROM blockstream/elementsd:0.21.0.2

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN mkdir -p /root/.elements/elementsregtest
COPY elements.conf /root/.elements/elements.conf

ENTRYPOINT ["/docker-entrypoint.sh"]
