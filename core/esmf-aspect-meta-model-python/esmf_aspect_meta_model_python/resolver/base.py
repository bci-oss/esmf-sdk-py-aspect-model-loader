#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from esmf_aspect_meta_model_python import utils
from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph
from esmf_aspect_meta_model_python.samm_meta_model import SammUnitsGraph


class ResolverInterface(ABC):
    """
    Abstract class defining the interface for resolver classes.

    This class provides the template method `read` which all subclasses must implement to specify
    how they read data and return it.

    Methods:
        read(): Method to be overridden by subclasses to provide specific reading logic.
        get_aspect_urn(): Method to be overridden by subclasses to provide specific to provide specific logic to find
            the appropriate aspect urn.
        get_samm_version(): Method to find a SAMM version.
    """

    def __init__(self):
        self.graph = AdaptiveGraph()
        self.samm_graph = None
        self.samm_version = ""

    @abstractmethod
    def read(self, input_data: Union[str, Path]):
        """
        Abstract method to read data.

        Subclasses must implement this method to handle the specific details of reading data
        from their respective sources and return the data in the required format.

        Args:
            input_data (str): The input data to be read.

        Returns:
            Data read from the source, the type of the data can be decided based on the specific subclass.
        """

    @staticmethod
    def _validate_samm_version(samm_version: str):
        """
        Validates the provided SAMM version string against a supported version.

        This method checks if the `samm_version` provided and matches of the SAMM version supported by the system.

        Args:
            samm_version (str): The version string of SAMM to be validated. Expected to be in the format like '1.2.3'.

        Raises:
            ValueError: If `samm_version` is empty or not supplied.
        """
        if not samm_version:
            raise ValueError("SAMM version not found in the Graph.")
        elif samm_version > SammUnitsGraph.SAMM_VERSION:
            raise ValueError(f"{samm_version} is not supported SAMM version.")

    def set_samm_version(self, steam_input: Union[str, Path]) -> None:
        """
        Sets the SAMM version by extracting it from the specified file.

        This method uses the AdaptiveGraph class to extract the SAMM version from the given file.
        There is also a validation against known SAMM versions to ensure the version is supported and recognized.

        Args:
            steam_input (Union[str, Path]): The path to the file from which the SAMM version is to be extracted.

        Raises:
            ValueError: If the extracted version is not supported or if it is not found in the file.
        """
        version = utils.get_samm_version_from_input(steam_input)
        self._validate_samm_version(version)
        self.samm_version = version

    def prepare_aspect_model(self, graph: AdaptiveGraph):
        """Resolve all additional graph elements if needed."""
