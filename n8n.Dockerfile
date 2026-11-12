ARG N8N_VERSION=2.47.5
# n8n's hardened Alpine runtime no longer includes apk. Bring its matching
# package manager back only for the build, rather than assuming it exists.
FROM alpine:3.24 AS package-manager
FROM docker.n8n.io/n8nio/n8n:${N8N_VERSION}

COPY --from=package-manager /sbin/apk /sbin/apk
COPY --from=package-manager /lib/apk /lib/apk
COPY --from=package-manager /usr/lib/libapk.so* /usr/lib/
COPY --from=package-manager /etc/apk/ /etc/apk/

USER root

RUN set -eux; \
    . /etc/os-release; \
    case "$VERSION_ID" in 3.24|3.24.*) ;; *) echo "Review Alpine ABI before upgrading n8n" >&2; exit 1;; esac; \
    apk add --no-cache imagemagick imagemagick-webp; \
    magick -version; \
    rm -f /sbin/apk /usr/lib/libapk.so*

USER node
