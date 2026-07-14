# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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


### Changed
- No changes.


### Removed
- No removes.
