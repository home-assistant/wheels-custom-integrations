#!/bin/sh

for component in components/*; do
manifest=$(jq --raw-output ".manifest" "${component}")

echo "Process: ${component} -> ${manifest}"
curl -sSL -f "${manifest}" | jq --raw-output '.requirements | join("\n")' >> ./requirements_raw.txt
done

sort ./requirements_raw.txt | uniq -u > ./requirements.txt

echo "List:"
cat ./requirements.txt