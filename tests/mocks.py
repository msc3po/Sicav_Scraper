from scrapy.http import HtmlResponse


def createMockResponse():
    fake_html = ""

    with open("./tests/html_snapshot.txt", "r") as file:
        fake_html = file.read()

    return HtmlResponse(
        url="https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18",
        body=fake_html,
        encoding="utf-8",
    )
