#!/bin/bash
set -e

if [ -z "$@" ]; then
    echo "No command provided. Waiting forever for someone to attach to this container..."
    sleep infinity
fi

exec "$@"
