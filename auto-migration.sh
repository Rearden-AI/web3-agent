#!/bin/sh

SUPPORTED_ENVS="dev stage prod"
UPDATE_ONLY=0
REVISION_AND_UPGRADE=0

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 <env> [-u|-ru]"
    echo "Supported environments: $SUPPORTED_ENVS"
    exit 1
fi

ENV=$1

if [ "$#" -eq 2 ]; then
    if [ "$2" = "-u" ]; then
        UPDATE_ONLY=1
    elif [ "$2" = "-ru" ]; then
        REVISION_AND_UPGRADE=1
    else
        echo "Invalid option: $2"
        echo "Usage: $0 <env> [-u|-ru]"
        exit 1
    fi
fi

if ! echo "$SUPPORTED_ENVS" | grep -wq "$ENV"; then
    echo "Error: Unsupported environment '$ENV'"
    echo "Supported environments: $SUPPORTED_ENVS"
    exit 1
fi

if [ "$UPDATE_ONLY" -eq 1 ]; then
    python3 .scripts/migration.py $ENV -u
elif [ "$REVISION_AND_UPGRADE" -eq 1 ]; then
    python3 .scripts/migration.py $ENV -ru
else
    python3 .scripts/migration.py $ENV
fi