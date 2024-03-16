import os
import pytest
from sicavs.spiders.Msc3poSpider import Msc3poSpider


def setup_function():
    if os.environ.get("MONGODB_HOST"):
        del os.environ["MONGODB_HOST"]
    if os.environ.get("MONGODB_DATABASE"):
        del os.environ["MONGODB_DATABASE"]
    if os.environ.get("MONGODB_PORT"):
        del os.environ["MONGODB_PORT"]


def teardown_function():
    setup_function()


def test_default_initalization(monkeypatch):
    monkeypatch.delenv("MONGODB_HOST", raising=False)
    monkeypatch.delenv("MONGODB_DATABASE", raising=False)
    monkeypatch.delenv("MONGODB_PORT", raising=False)

    spider = Msc3poSpider()

    assert spider.client is not None
    assert spider.db.name == "sicavs"
    assert spider.client.HOST == "localhost"
    assert spider.client.PORT == 27017

    def test_environment_variable_initialization(monkeypatch):
        monkeypatch.setenv("MONGODB_HOST", "test_host")
        monkeypatch.setenv("MONGODB_DATABASE", "test_db")
        monkeypatch.setenv("MONGODB_PORT", "1234")

        spider = Msc3poSpider()

        assert spider.client is not None
        assert spider.db.name == "test_db"
        assert spider.client.HOST == "test_host"
        assert spider.client.PORT == 12345
