echo "Proxy subnet creation ({region})..."
gcloud compute networks subnets create southamerica-east1-proxy-subnet \
    --purpose=REGIONAL_MANAGED_PROXY \
    --role=ACTIVE \
    --region={region} \
    --network="{network_name}" \
    --range=172.16.0.0/23 \
    --project="{project_id}" \
    || echo "Proxy subnet already exists (continuing)"
