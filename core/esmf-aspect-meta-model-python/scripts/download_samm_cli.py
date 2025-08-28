"""Download SAMM CLI.

Windows: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.10.2/samm-cli-2.10.2-windows-x86_64.zip
  Linux: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.10.2/samm-cli-2.10.2-linux-x86_64.tar.gz
    JAR: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.10.2/samm-cli-2.10.2.jar
"""

from esmf_aspect_meta_model_python.samm_cli.download import download_samm_cli


if __name__ == "__main__":
    download_samm_cli()
