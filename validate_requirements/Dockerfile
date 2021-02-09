FROM homeassistant/amd64-homeassistant-base

COPY ./components  /validate/components
COPY ./validate_requirements /validate
COPY ./templates/validate.template /validate/validate.template
COPY ./requirements.json /validate/requirements.json

RUN \
    tempio -conf /validate/requirements.json  -template /validate/validate.template -out /validate/apk.list \
    && apk add $(cat /validate/apk.list) \
    && python3 -m pip --disable-pip-version-check install -r /validate/requirements.txt

ENTRYPOINT [ "sh", "/validate/run.sh" ]
