# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.0.9] - 2026-08-27

### Added
- Regional RESTRICTED SSL policy
  ``gateway-ssl-policy-restricted`` (TLS 1.2+) via
  ``bash__create_ssl-policy.bash`` and
  ``bash__check_ssl-policy.bash``.
- ``GCPGatewayPolicy`` in ``deploy__gateway.yml`` attaches the SSL
  policy to Gateway ``ingress-gcp-gateway`` (mitigates weak ciphers
  such as 3DES / Sweet32).
- ``IngressGCPGateway.SSL_POLICY_NAME`` constant shared by
  infrastructure scripts and the Gateway policy template.
- ``create_infrastructure`` / ``check_infrastructure`` create and
  verify the SSL policy before certificate steps.

### Security
- Client-to-load-balancer cipher suite restricted to disable 3DES
  (CVE-2016-2183 / Sweet32).


## [0.0.8] - 2026-07-29

### Changed
- Default Certificate Manager resource name prefixes shortened:
  ``gateway-certificate--{slug}`` and
  ``gateway-dns-auth--{slug}`` (was
  ``ingress-gcp-gateway-certificate--`` /
  ``ingress-gcp-gateway-dns-auth--``).


## [0.0.7] - 2026-07-29

### Added
- ``IngressGCPGateway.get_certificate_name`` and
  ``get_dns_authorization_name`` helpers for slugified defaults.

### Changed
- ``IngressGCPGateway`` constructor — ``certificate_name`` is
  optional; when omitted, uses
  ``get_certificate_name(server_name)``.
- ``deploy__gateway.yml`` — TLS annotation uses
  ``{certificate_name}`` instead of a hardcoded cert name.


## [0.0.4] - 2026-07-29

### Added
- Dependency ``python-slugify`` for default Certificate Manager resource
  names derived from ``server_name``.

### Changed
- ``IngressGCPGateway.create_infrastructure`` — ``dns_authorization_name``
  and ``certificate_name`` are optional; when omitted, names include a
  slugified ``server_name`` suffix.
- ``IngressGCPGateway.check_infrastructure`` — requires ``server_name``;
  optional ``certificate_name`` uses the same slugified default as
  ``create_infrastructure``.


## [0.0.3] - 2026-07-14

### Added
- Initial satellite package for Pumpwood GKE Gateway ingress on
  Kubernetes, extracted from the monolithic ``pumpwood-deploy`` package.
- **`IngressGCPGateway`**: regional Gateway API ingress with TLS
  termination via Certificate Manager
  (``networking.gke.io/cert-manager-certs``) and HTTP-to-HTTPS redirect
  on the GKE L7 regional external managed load balancer.
- **`create_infrastructure`** class method: creates the regional
  managed proxy subnet, enables Gateway API on the GKE cluster, and
  provisions a regional Google-managed Certificate Manager certificate
  (DNS authorization + CNAME instructions).
- **`check_infrastructure`** class method: describes certificate
  status until ``ACTIVE``.
- Kubernetes resource template ``deploy__gateway.yml``: Gateway,
  redirect HTTPRoute, app HTTPRoute, and ``HealthCheckPolicy``.
- Bash infrastructure scripts:
  - ``bash__create_proxy-subnet.bash``
  - ``bash__allow_gateway_k8s_api.bash``
  - ``bash__create_certificate-manager.bash``
  - ``bash__check_certificate-manager.bash``
- Optional ``certificate_name`` constructor argument (default
  ``ingress-gcp-gateway-certificate``).
- Project scaffolding: ``build.sh``, ``pyproject.toml``,
  ``README.md``, ``LICENSE``, and generated API documentation under
  ``docs/``.
