echo "Enabling Gateway API on cluster ({cluster_name})..."
gcloud container clusters update "{cluster_name}" \
  --region "{region}" \
  --project "{project_id}" \
  --gateway-api=standard