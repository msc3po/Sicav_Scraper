import pytest
from mongomock import MongoClient
from sicavs.spiders.Msc3poSpider import Msc3poSpider


@pytest.fixture
def mock_db():
    client = MongoClient()
    db = client["test_sicavs"]
    collection = db["data"]

    collection.insert_one(
        {
            "nombre": "1948 INVERSIONS, SICAV S.A.",
            "num_registro_oficial": "1480",
            "fecha_registro_oficial": "28/12/2000",
            "domicilio": "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)",
            "capitales": {
                "inicial": 5000000,
                "maximo_estatutario": 50000000,
            },
            "ISIN": "ES0109642035",
            "folletos": [
                {
                    "fecha": "06/07/2022",
                    "domicilio": "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)",
                    "capitales": {
                        "inicial": 5000000,
                        "maximo_estatutario": 50000000,
                    },
                }
            ],
        }
    )

    return db


def test_insert_new_data(mock_db):
    spider = Msc3poSpider()
    spider.db = mock_db

    # Datos de muestra
    sicav_data = {
        "nombre": "1948 INVERSIONS, SICAV S.A.",
        "num_registro_oficial": "1480",
        "fecha_registro_oficial": "28/12/2000",
        "domicilio": "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)",
        "capitales": {
            "inicial": 5000000,
            "maximo_estatutario": 50000000,
        },
        "ISIN": "ES0109642035",
    }
    folleto = {
        "fecha": "07/07/2023",
        "domicilio": "Plaza del Sol, 1 - 28027 Madrid (Madrid)",
        "capitales": {
            "inicial": 5000000,
            "maximo_estatutario": 50000000,
        },
    }

    spider.collection = mock_db["data"]
    spider.collection.update_one(
        {"num_registro_oficial": sicav_data["num_registro_oficial"]},
        {"$set": sicav_data, "$addToSet": {"folletos": folleto}},
        upsert=True,
    )

    # Recuperar el documento actualizado
    updated_sicav = mock_db["data"].find_one({"num_registro_oficial": "1480"})

    # Verificar que contiene 2 folletos
    assert len(updated_sicav["folletos"]) == 2

    # Verificar que el último folleto es el más reciente
    assert updated_sicav["folletos"][-1]["fecha"] == "07/07/2023"

    # Actualiza el domicilio y los capitales del SICAV

    updated_sicav_data = {
        "nombre": "1948 INVERSIONS, SICAV S.A.",
        "num_registro_oficial": "1480",
        "fecha_registro_oficial": "28/12/2000",
        "domicilio": "Calle nueva dirección, 20 - 28027 Madrid (Madrid)",
        "capitales": {
            "inicial": 5500000,
            "maximo_estatutario": 52000000,
        },
        "ISIN": "ES0109642035",
    }

    spider.collection.update_one(
        {"num_registro_oficial": updated_sicav_data["num_registro_oficial"]},
        {"$set": updated_sicav_data},
    )

    # Recuperar el documento actualizado
    updated_sicav_after_changes = mock_db["data"].find_one(
        {"num_registro_oficial": "1480"}
    )

    # Verificar que los datos se han actualizado correctamente
    assert (
        updated_sicav_after_changes["domicilio"]
        == "Calle nueva dirección, 20 - 28027 Madrid (Madrid)"
    )
    assert updated_sicav_after_changes["capitales"]["inicial"] == 5500000
    assert updated_sicav_after_changes["capitales"]["maximo_estatutario"] == 52000000


def test_no_duplicate_folletos_when_no_changes(mock_db):
    spider = Msc3poSpider()
    spider.db = mock_db

    sicav_data = {
        "nombre": "1948 INVERSIONS, SICAV S.A.",
        "num_registro_oficial": "1480",
        "fecha_registro_oficial": "28/12/2000",
        "domicilio": "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)",
        "capitales": {
            "inicial": 5000000,
            "maximo_estatutario": 50000000,
        },
        "ISIN": "ES0109642035",
    }
    folleto = {
        "fecha": "06/07/2022",
        "domicilio": "Calle Juan Ignacio Luca de Tena, 11 - 28027 Madrid (Madrid)",
        "capitales": {
            "inicial": 5000000,
            "maximo_estatutario": 50000000,
        },
    }

    spider.collection = mock_db["data"]
    spider.collection.update_one(
        {"num_registro_oficial": sicav_data["num_registro_oficial"]},
        {"$set": sicav_data, "$addToSet": {"folletos": folleto}},
        upsert=True,
    )

    updated_sicav = mock_db["data"].find_one({"num_registro_oficial": "1480"})
    assert len(updated_sicav["folletos"]) == 1
    assert updated_sicav["folletos"][0]["fecha"] == "06/07/2022"
