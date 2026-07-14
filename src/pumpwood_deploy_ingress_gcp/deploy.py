"""Kubernetes deployment manifests for GKE Gateway ingress.

This module builds GKE Gateway API manifests for Pumpwood stacks on a
regional external managed load balancer. TLS termination uses a regional
Certificate Manager certificate referenced via
``networking.gke.io/cert-manager-certs``. HTTP-to-HTTPS redirect is
handled by the HTTPRoute.

Create a regional Google-managed Certificate Manager certificate in
GCP before deploy (DNS authorization + CNAME; see UAT
``create_certificates.bash``). Gateway controller does not support
ManagedCertificate.

Manifests are registered with ``DeployPumpWood.add_microservice`` from
``pumpwood-deploy``.
"""
import subprocess

from importlib import resources
from pumpwood_deploy.abc import BasePumpwoodDeployMicroservice
from pumpwood_deploy.type import PumpwoodDeploy, PumpwoodDeployDeployment


def _run_bash_script(script: str) -> None:
    """Run a bash script string and raise on failure.

    Args:
        script (str):
            Bash script body to execute.

    Returns:
        None:
            Always returns None when the script succeeds.

    Raises:
        subprocess.CalledProcessError:
            If bash exits with a non-zero status.
    """
    subprocess.run(
        ['/bin/bash', '-'],
        input=script,
        text=True,
        check=True)


deploy__gateway = resources\
    .files('pumpwood_deploy_ingress_gcp')\
    .joinpath('resources/deploy__gateway.yml')\
    .read_text(encoding='utf-8')
infrastructure__create_certificate = resources\
    .files('pumpwood_deploy_ingress_gcp')\
    .joinpath('resources/bash__create_certificate-manager.bash')\
    .read_text(encoding='utf-8')
infrastructure__check_certificate = resources\
    .files('pumpwood_deploy_ingress_gcp')\
    .joinpath('resources/bash__check_certificate-manager.bash')\
    .read_text(encoding='utf-8')
infrastructure__create_proxy_subnet = resources\
    .files('pumpwood_deploy_ingress_gcp')\
    .joinpath('resources/bash__create_proxy-subnet.bash')\
    .read_text(encoding='utf-8')
infrastructure__allow_gateway_k8s_api = resources\
    .files('pumpwood_deploy_ingress_gcp')\
    .joinpath('resources/bash__allow_gateway_k8s_api.bash')\
    .read_text(encoding='utf-8')


class IngressGCPGateway(BasePumpwoodDeployMicroservice):
    """Deploy GKE regional Gateway ingress with Certificate Manager TLS.

    Renders a Gateway and HTTPRoute pair. HTTPS termination uses a
    regional Certificate Manager certificate that must already exist in
    the same GCP project and region as the Gateway.

    Pair with ``ApiGatewayNoCertificate`` so the Gateway routes traffic
    to the NGINX service that adds CORS and security headers.

    Example:
        ```python
        import os
        from pumpwood_deploy_api_gateway import ApiGatewayNoCertificate
        from pumpwood_deploy_ingress_gcp import IngressGCPGateway

        deploy.add_microservice(
            ApiGatewayNoCertificate(
                version=os.getenv("API_GATEWAY"),
            ))

        deploy.add_microservice(
            IngressGCPGateway(
                server_name="app.example.com",
                public_ip_name="pumpwood-gateway-ip",
                target_service="apigateway-nginx",
                certificate_name="ingress-gcp-gateway-certificate",
            ))
        ```
    """
    def __init__(self, server_name: str, public_ip_name: str,
                 target_service: str = "apigateway-nginx",
                 certificate_name: str = (
                     "ingress-gcp-gateway-certificate"),
                 health_check_path: str = (
                     "/health-check/pumpwood-auth-app/")):
        """Initialize GKE Gateway ingress deployment configuration.

        Args:
            server_name (str):
                DNS hostname for the Gateway HTTPRoute.
            public_ip_name (str):
                Name of the GCP reserved external IP address
                (``NamedAddress``) bound to the Gateway.
            target_service (str):
                Kubernetes Service name for HTTPS traffic routing.
                Defaults to ``apigateway-nginx``.
            certificate_name (str):
                Regional Certificate Manager certificate name already
                created in GCP. Defaults to
                ``ingress-gcp-gateway-certificate``.
        """
        self.server_name = server_name
        self.public_ip_name = public_ip_name
        self.target_service = target_service
        self.certificate_name = certificate_name
        self.health_check_path = health_check_path

    def create_deployment_file(self) -> list[PumpwoodDeploy]:
        """Build Kubernetes manifests for the GKE Gateway ingress.

        Returns:
            list[PumpwoodDeploy]:
                Deployment ``ingress_gcp_gateway__gateway`` with Gateway
                and HTTPRoute resources.
        """
        gateway__formatted = deploy__gateway.format(
            server_name=self.server_name,
            public_ip_name=self.public_ip_name,
            target_service=self.target_service,
            certificate_name=self.certificate_name,
            health_check_path=self.health_check_path)

        return [
            PumpwoodDeployDeployment(
                name='ingress_gcp_gateway__gateway',
                content=gateway__formatted),
        ]

    @classmethod
    def create_infrastructure(
            cls, region: str, project_id: str, server_name: str,
            cluster_name: str, network_name: str = "default",
            dns_authorization_name: str = (
                "ingress-gcp-gateway-dns-auth"),
            certificate_name: str = (
                "ingress-gcp-gateway-certificate"),
            ) -> None:
        """Create GKE regional Gateway ingress infrastructure.

        Args:
            region (str):
                GCP region for the Gateway ingress.
            project_id (str):
                GCP project ID for the Gateway ingress.
            server_name (str):
                DNS hostname for Certificate Manager authorization
                and the managed certificate.
            cluster_name (str):
                GKE cluster name to enable the Gateway API on.
            network_name (str):
                GCP network name for the Gateway ingress.
                Defaults to ``default``.
            dns_authorization_name (str):
                GCP DNS authorization name for the Gateway ingress.
                Defaults to ``ingress-gcp-gateway-dns-auth``.
            certificate_name (str):
                Regional Certificate Manager certificate name.
                Defaults to ``ingress-gcp-gateway-certificate``.


        Returns:
            None:
                Always returns None when all scripts succeed.

        Raises:
            subprocess.CalledProcessError:
                If a gcloud command exits with a non-zero status.
        """
        proxy_subnet_script = infrastructure__create_proxy_subnet.format(
            region=region,
            network_name=network_name,
            project_id=project_id)
        _run_bash_script(proxy_subnet_script)

        allow_gateway_script = infrastructure__allow_gateway_k8s_api.format(
            cluster_name=cluster_name,
            region=region,
            project_id=project_id)
        _run_bash_script(allow_gateway_script)

        certificate_script = infrastructure__create_certificate.format(
            region=region,
            project_id=project_id,
            domain=server_name,
            dns_authorization_name=dns_authorization_name,
            certificate_name=certificate_name)
        _run_bash_script(certificate_script)

    @classmethod
    def check_infrastructure(
            cls, region: str, project_id: str,
            certificate_name: str = (
                "ingress-gcp-gateway-certificate")) -> None:
        """Check GKE regional Gateway ingress infrastructure.

        Args:
            region (str):
                GCP region for the Gateway ingress.
            project_id (str):
                GCP project ID for the Gateway ingress.
            certificate_name (str):
                Regional Certificate Manager certificate name.
                Defaults to ``ingress-gcp-gateway-certificate``.

        Returns:
            None:
                Always returns None when the script succeeds.

        Raises:
            subprocess.CalledProcessError:
                If a gcloud command exits with a non-zero status.
        """
        check_certificate_script = (
            infrastructure__check_certificate.format(
                region=region,
                project_id=project_id,
                certificate_name=certificate_name))
        _run_bash_script(check_certificate_script)
