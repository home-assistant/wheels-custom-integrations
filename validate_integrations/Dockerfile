FROM homeassistant/amd64-homeassistant-base

COPY ./components  /validate/components
COPY ./validate_integrations /validate

RUN \
    python3 -m pip --disable-pip-version-check install -r /validate/requirements.txt

ENTRYPOINT [ "sh", "/validate/run.sh" ]