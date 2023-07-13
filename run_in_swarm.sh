docker service create \
    --replicas 1 \
    --name retiler \
    -p 8080:8080 \
    --mount type=bind,source=/home/mishin/retiling/app/config.json,destination=/app/config.json \
    retiler:v1