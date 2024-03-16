from sicavs.spiders.Msc3poSpider import Msc3poSpider
import scrapy


def setup_function():
    pass


def teardown_function():
    pass


def test_start_urls():
    spider = Msc3poSpider()
    assert spider.start_urls == [
        "https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18"
    ]


def test_next_page_url():
    spider = Msc3poSpider()
    mockResponse = createMockResponse()
    next_url = spider.construct_next_page_url(mockResponse)
    # Change the expected URL to what should be the next page.
    expected_url = "https://www.cnmv.es/YourExpectedNextPageURL"
    assert next_url == expected_url


def createMockResponse():
    # Add mock HTML content that represents the structure your spider expects.
    mock_html_content = """
    <!-- Other content -->
    <li>
        <span class='active'>Some page info</span>
    </li>
    <li>
        <a href="https://www.cnmv.es/YourExpectedNextPageURL">Link to next page</a>
    </li>
    <!-- Other content -->
    """
    response = scrapy.http.HtmlResponse(
        url="https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18",
        body=mock_html_content,
        encoding="utf-8",
    )
    return response
