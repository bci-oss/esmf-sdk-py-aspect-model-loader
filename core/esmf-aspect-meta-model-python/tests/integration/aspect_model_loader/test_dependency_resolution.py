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

import pytest

from rdflib.term import URIRef, Literal
from os import makedirs, remove
from os.path import abspath, dirname, join, isfile

from esmf_aspect_meta_model_python.resolver.local_file import LocalFileResolver


class TestDependencyResolution:

    ROOT_PATH: str = dirname(dirname(abspath(__file__)))
    SOURCE_PATH = join(ROOT_PATH, "resources", "traversal_dependency")
    SECRET_PATH = join(ROOT_PATH, "secrets")

    model_path = ["models", "org.example.test", "1.0.0"]
    secret_path = ["secrets", "1.0.0"]

    @classmethod
    def setup_class(cls):
        cls.evil_model_dir  = join(cls.ROOT_PATH, cls.SOURCE_PATH, *cls.model_path)
        cls.evil_model_name = "Evil.ttl"
        cls._create_file(cls.evil_model_dir, cls.evil_model_name)

        cls.secret_dir = join(cls.ROOT_PATH, cls.SOURCE_PATH, *cls.secret_path)
        cls.secret_model_name = "confidential.ttl"
        cls._create_file(cls.secret_dir, cls.secret_model_name)


    @classmethod
    def _create_file(cls, file_path, file_name):
        file_full_path = join(file_path, file_name)

        if isfile(file_full_path):
            remove(file_full_path)

        makedirs(file_path, exist_ok=True)

        if file_name == cls.evil_model_name:
            cls._create_evil_model_file(file_full_path)
        elif file_name == cls.secret_model_name:
            cls._create_secret_model_file(file_full_path)
        else:
            raise NotImplementedError(f"Unknown file name: {file_name}")

    @classmethod
    def _create_evil_model_file(cls, file_full_path):
        with open(file_full_path, "w") as f:
            # absolute path component → os.path.join discards base_path entirely
            f.write(
                '@prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#> .\n'
                f'@prefix evil: <urn:samm:{join(cls.ROOT_PATH, cls.SOURCE_PATH, "secrets")}:1.0.0#> .\n'
                '<urn:samm:org.example.test:1.0.0#Evil> a samm:Aspect ;\n'
                '   samm:properties () ; samm:operations () .\n'
            )

    @classmethod
    def _create_secret_model_file(cls, file_full_path):
        with open(join(file_full_path), "w") as f:
            f.write(
                '@prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#> .\n'
                '@prefix ex: <http://example.com/secret#> .\n'
                'ex:LeakedSecret ex:value "TOP-SECRET-CREDENTIAL-12345" .\n'
            )

    @classmethod
    def teardown_class(cls):
        remove(join(cls.evil_model_dir, cls.evil_model_name))
    
    def test_parse_namespace_relative_path_return_path(self):
        result = LocalFileResolver._parse_namespace("urn:samm:../secrets:1.0.0#")

        assert result == ("../secrets", "1.0.0")
    
    def test_parse_namespace_absolute_path_return_none(self):
        result = LocalFileResolver._parse_namespace("urn:samm:/etc:1.0.0#")

        assert result == (None, None)


    def test_read_secrets(self):
        local_file_resolver = LocalFileResolver()
        graph = local_file_resolver.read(join(self.evil_model_dir, self.evil_model_name))
        local_file_resolver.prepare_aspect_model(graph)
        result = list(local_file_resolver.graph.triples((URIRef("http://example.com/secret#LeakedSecret"), None, None)))

        assert len(result) == 0
