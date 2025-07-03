from main import parse_page

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

def test_parser():
    parsed = parse_page(html_doc) 
    assert parsed["links"] == ["http://example.com/elsie", "http://example.com/lacie", "http://example.com/tillie"]
    assert parsed["title"] == "The Dormouse's story"
    # TODO: Better version of the words test, as words should include every individual word in the html document (not tags)
    assert "Dormouse" in parsed["words"]