# -*- coding: utf-8 -*-
import json

import pytest
import requests
import requests_mock

from chaosspring.probes import chaosmonkey_enabled, watcher_configuration, assaults_configuration


def test_chaosmonkey_is_enabled():
    with requests_mock.mock() as m:
        m.get(
            "http://localhost:8080/actuator/chaosmonkey/status",
            status_code=200,
            text="Ready to be evil!")

        enabled = chaosmonkey_enabled(
            base_url="http://localhost:8080/actuator")

    assert enabled is True


def test_chaosmonkey_not_enabled():
    with requests_mock.mock() as m:
        m.get(
            "http://localhost:8080/actuator/chaosmonkey/status",
            status_code=200,
            text="You switched me off!")

        enabled = chaosmonkey_enabled(
            base_url="http://localhost:8080/actuator")

    assert enabled is False


def test_watcher_configuration():
    text_response = {
        "controller": True,
        "restController": False,
        "service": True,
        "repository": False,
        "component": False
    }

    with requests_mock.mock() as m:
        m.get(
            "http://localhost:8080/actuator/chaosmonkey/watcher",
            status_code=200,
            json=text_response)

        configuration = watcher_configuration(
            base_url="http://localhost:8080/actuator")
        assert m.called
        assert "service" in configuration
        assert configuration["service"] == True


def test_assaults_configuration():
    text_response = {
        "level": 3,
        "latencyRangeStart": 1000,
        "latencyRangeEnd": 3000,
        "latencyActive": True,
        "exceptionsActive": False,
        "killApplicationActive": False,
        "restartApplicationActive": False
    }

    with requests_mock.mock() as m:
        m.get(
            "http://localhost:8080/actuator/chaosmonkey/assaults",
            status_code=200,
            json=text_response)

        configuration = assaults_configuration(
            base_url="http://localhost:8080/actuator")
        assert m.called
        assert "level" in configuration
        assert configuration["level"] == 3
