from __future__ import unicode_literals

from django.forms import Media
from django.test import TestCase

from js_asset.js import JS


class AssetTest(TestCase):
    def test_asset(self):
        media = Media(
            css={"print": ["app/print.css"]},
            js=[
                "app/test.js",
                JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
                JS("app/asset-without.js", {}),
            ],
        )
        html = "%s" % media

        # print(html)

        self.assertInHTML(
            '<link href="/static/app/print.css" type="text/css" media="print" rel="stylesheet" />',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/test.js"></script>',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/asset.js" data-the-answer="42" id="asset-script"></script>',  # noqa
            html,
        )
        self.assertInHTML(
            '<script type="text/javascript" src="/static/app/asset-without.js"></script>',  # noqa
            html,
        )

    def test_absolute(self):
        media = Media(js=[JS("https://cdn.example.org/script.js", static=False)])
        html = "%s" % media

        self.assertInHTML(
            '<script type="text/javascript" src="https://cdn.example.org/script.js"></script>',  # noqa
            html,
        )

    def test_asset_merging(self):
        media1 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media2 = Media(js=["thing.js", JS("other.js"), "some.js"])
        media = media1 + media2
        self.assertEqual(len(media._js), 3)
        self.assertEqual(media._js[0], "thing.js")
        self.assertEqual(media._js[2], "some.js")

    def test_repr(self):
        self.assertEqual(
            repr(
                JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42})
            ).lstrip("u"),
            'JS(app/asset.js, {"data-the-answer": 42, "id": "asset-script"}, static=True)',  # noqa
        )

    def test_set(self):
        media = [
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 42}),
            JS("app/asset.js", {"id": "asset-script", "data-the-answer": 43}),
        ]

        self.assertEqual(len(set(media)), 2)
