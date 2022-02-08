#!/bin/bash


ENCODED_AUTH=$(echo -n ${ORIOKS_LOGPASS} | base64)

RESPONSE=$(curl --silent -H "Accept: application/json" -H "User-Agent: orioks_monitoring/0.2 GNU/Linux" -H "Authorization: Basic ${ENCODED_AUTH}" https://orioks.miet.ru/api/v1/auth)

RAW_TOKEN=$(echo ${RESPONSE} | jq .token --raw-output)

echo "ORIOKS_API_TOKEN=${RAW_TOKEN}"
