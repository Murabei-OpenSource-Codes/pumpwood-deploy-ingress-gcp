"""Kubernetes deployment package for GKE Gateway ingress.

Provides ``IngressGCPGateway`` for Pumpwood stacks on GKE. The class
renders a Gateway and HTTPRoute so TLS termination and HTTP-to-HTTPS
redirect are handled by the GKE L7 regional external managed load
balancer.

TLS uses a regional Certificate Manager certificate referenced with
``networking.gke.io/cert-manager-certs``. Create that certificate in
GCP before applying the Gateway (ManagedCertificate is not supported
by the Gateway controller).

Example:
    ```python
    from pumpwood_deploy.deploy import DeployPumpWood
    from pumpwood_deploy_api_gateway import ApiGatewayNoCertificate
    from pumpwood_deploy_ingress_gcp import IngressGCPGateway

    deploy.add_microservice(
        ApiGatewayNoCertificate(version="1.2.0"))

    deploy.add_microservice(
        IngressGCPGateway(
            server_name="app.example.com",
            public_ip_name="pumpwood-gateway-ip",
            target_service="apigateway-nginx",
            certificate_name="ingress-gcp-gateway-certificate",
        ))
    ```

Use with ``DeployPumpWood`` from ``pumpwood-deploy``. Deploy
``ApiGatewayNoCertificate`` first so the ``apigateway-nginx`` Service
exists before the Gateway routes traffic to it.
"""
from .deploy import IngressGCPGateway


__all__ = [
    IngressGCPGateway,
]
