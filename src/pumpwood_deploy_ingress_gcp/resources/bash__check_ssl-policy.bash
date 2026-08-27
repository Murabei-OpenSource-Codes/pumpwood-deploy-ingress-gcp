echo "SSL policy status:"
gcloud compute ssl-policies describe "{ssl_policy_name}" \
  --region="{region}" \
  --project="{project_id}" \
  --format="yaml(name,profile,minTlsVersion)"
