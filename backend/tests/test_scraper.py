# Student Name: Ruvi Kathiriya

# Student ID: ET21BTAI031

# Course: Web Programming

# Academic Year: Third Year B.Tech (AI & DS)

# Semester: 6

# Group: 15
from app.scraper.scraper import parse_detail, parse_listing

LISTING = """
<html><body><ol>
<li><article class="product_pod">
  <div class="image_container"><a href="a-light-in-the-attic_1000/index.html">
    <img src="../media/cache/2c/da/cover.jpg" alt="A Light in the Attic"></a></div>
  <p class="star-rating Three"></p>
  <h3><a href="a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
  <div class="product_price"><p class="price_color">£51.77</p>
  <p class="instock availability"><i class="icon-ok"></i> In stock </p></div>
</article></li></ol></body></html>
"""

DETAIL = """
<html><body>
<ul class="breadcrumb"><li><a href="/">Home</a></li><li><a href="/b">Books</a></li>
<li><a href="/p">Poetry</a></li><li class="active">A Light in the Attic</li></ul>
<p class="instock availability"><i></i> In stock (22 available) </p>
<div id="product_description" class="sub-header"><h2>Product Description</h2></div>
<p>It's hard to imagine a world without this book.</p>
</body></html>
"""


def test_parse_listing():
    items = parse_listing(LISTING, "https://books.toscrape.com/catalogue/page-1.html")
    assert len(items) == 1
    item = items[0]
    assert item["title"] == "A Light in the Attic"
    assert item["price"] == "£51.77"
    assert item["rating"] == "Three"
    assert item["product_url"] == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    assert item["image_url"].endswith("/media/cache/2c/da/cover.jpg")


def test_parse_detail():
    d = parse_detail(DETAIL)
    assert d["category"] == "Poetry"
    assert "22 available" in d["availability"]
    assert d["description"].startswith("It's hard to imagine")
