echo "Creating regional SSL policy ({region})..."
gcloud compute ssl-policies create "{ssl_policy_name}" \
  --profile=RESTRICTED \
  --min-tls-version=1.2 \
  --region="{region}" \
  --project="{project_id}" \
  || echo "SSL policy already exists (continuing)"
