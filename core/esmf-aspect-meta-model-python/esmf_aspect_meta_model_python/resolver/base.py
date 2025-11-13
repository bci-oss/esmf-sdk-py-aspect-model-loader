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

import esmf_aspect_meta_model_python.constants as const

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
        self.samm_version = const.SAMM_VERSION

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

    def prepare_aspect_model(self, graph: AdaptiveGraph):
        """Resolve all additional graph elements if needed."""
