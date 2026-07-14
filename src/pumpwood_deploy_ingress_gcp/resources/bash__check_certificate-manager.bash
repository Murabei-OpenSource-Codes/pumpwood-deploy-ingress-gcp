echo "Certificate status (wait until ACTIVE after CNAME propagates):"
gcloud certificate-manager certificates describe "{certificate_name}" \
  --location="{region}" \
  --project="{project_id}" \
  --format="yaml(name,managed.state,sanDnsnames)"