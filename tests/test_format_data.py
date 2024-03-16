import pytest
from sicavs.spiders.Msc3poSpider import Msc3poSpider
from .mocks import createMockResponse


@pytest.fixture
def mocked_mongo(mocker):
    mocker.patch("sicavs.spiders.Msc3poSpider.MongoClient")
    return mocker


@pytest.fixture
def spider(mocked_mongo):
    return Msc3poSpider()


def test_sicav_data_structure(spider):
    # Given
    print("given")

    spider = Msc3poSpider()
    response = createMockResponse()

    # When
    print("when")
    results = list(spider.parse_sicav_details(response))

    # Then
    print("then")
    assert len(results) == 1

    result = results[0]
    sicav_data = result["sicav_data"]
    print("result", result, flush=True)
    print("sicav dat", sicav_data, flush=True)
    folleto = result["folleto"]
    print("folleto", folleto, flush=True)
    expected_keys_sicav_data = [
        "nombre",
        "num_registro_oficial",
        "fecha_registro_oficial",
        "domicilio",
        "capitales",
        "ISIN",
    ]

    expected_keys_folleto = ["fecha", "domicilio", "capitales"]

    for key in expected_keys_sicav_data:
        assert key in sicav_data

    for key in expected_keys_folleto:
        assert key in folleto

    for key in expected_keys_sicav_data:
        assert sicav_data[key] is not None

    for key in expected_keys_folleto:
        assert folleto[key] is not None

    assert sicav_data["nombre"].strip() != ""

    assert sicav_data["nombre"] == "1948 INVERSIONS, SICAV S.A."
    assert sicav_data["num_registro_oficial"] == "1480"
    assert sicav_data["fecha_registro_oficial"] == "28/12/2000"
    assert (
        sicav_data["domicilio"]
        == "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)"
    )
    assert sicav_data["capitales"]["inicial"] == 5000000
    assert sicav_data["capitales"]["maximo_estatutario"] == 50000000
    assert sicav_data["ISIN"] == "ES0109642035"

    assert folleto["fecha"] == "07/07/2023"
