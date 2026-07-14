echo "Creating regional DNS authorization ({region})..."
gcloud certificate-manager dns-authorizations create "{dns_authorization_name}" \
  --domain="{domain}" \
  --location="{region}" \
  --project="{project_id}" \
  || echo "DNS authorization already exists (continuing)"

echo
echo "Add this CNAME at your DNS provider (required for issuance):"
gcloud certificate-manager dns-authorizations describe \
  "{dns_authorization_name}" \
  --location="{region}" \
  --project="{project_id}" \
  --format="yaml(dnsResourceRecord)"

echo
echo "Creating regional Google-managed certificate..."
gcloud certificate-manager certificates create "{certificate_name}" \
  --domains="{domain}" \
  --dns-authorizations="{dns_authorization_name}" \
  --location="{region}" \
  --project="{project_id}" \
  || echo "Certificate already exists (continuing)"
