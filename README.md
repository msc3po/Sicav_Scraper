

# SICAVs Scraper

This project aims to scrape and maintain a database of SICAVs from the CNMV portal. It's designed to be orchestrated using Docker and Docker Compose.

## Requirements:

- Docker
- Docker Compose

Optionally, if you already have a python environment in your dev machine, you can use poetry.

- Poetry (For Python Dependency Management)

## Quick Start:

1.  Clone the Repository:

    ```bash
    git clone https://github.com/msc3po/Sicavs_scraper
    cd Sicavs_scraper
    ```

2.  Build and Start the Scraper Container:

    ```bash
    docker-compose up
    ```

3.  Check the information:

    You can access the DB by executing the following line:

    ```bash
    docker exec -it sicavs_scraper-db-1 mongosh
    ```

    Then, in the mongo shell, you can query the data like this:

    ```mongosh
    use sicavs
    db.data.find()
    ```

    To List SICAVS filtered by data creation, register number , ISIN and name :

    ```js
    db.data.find({}, {
          fecha_de_creacion: 1,
          numero_de_registro: 1,
          ISIN: 1,
          nombre: 1,
        }).sort({ fecha_de_creacion: -1 });
    ```

    Accesing a SICAV by ISIN:

    ```js
    db.data.findOne({
      ISIN: "ES0107601033",
    });
    ```

## Tests

These tests run with docker so you don't have to instantiate a database nor install python dev environment.

The tests include both unit and integration testing with database.

To run the tests write the following in your terminal:

```bash
scripts/run_test.sh
```