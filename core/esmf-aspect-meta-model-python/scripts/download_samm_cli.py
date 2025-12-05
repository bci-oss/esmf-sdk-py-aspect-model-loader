"""Download SAMM CLI.

Windows: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0-windows-x86_64.zip
  Linux: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0-linux-x86_64.tar.gz
    JAR: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0.jar
"""

from esmf_aspect_meta_model_python.samm_cli.download import download_samm_cli

if __name__ == "__main__":
    download_samm_cli()
