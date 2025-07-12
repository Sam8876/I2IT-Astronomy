from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
# class HomePage(Page):
#     body = StreamField([
#         ("heading", blocks.CharBlock(classname="full title")),
#         ("subheading", blocks.CharBlock(classname="title")),
#         ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link", "ul", "ol"])),
#         ("image", ImageChooserBlock()),
#         ("quote", blocks.BlockQuoteBlock()),
#         ("html", blocks.RawHTMLBlock()),
#         ("button", blocks.StructBlock([
#             ("text", blocks.CharBlock(required=True)),
#             ("url", blocks.URLBlock(required=True)),
#         ])),
#     ], use_json_field=True, blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel("body"),
#     ]

class BlogIndexPage(Page):
    """Holds and lists all BlogPage children (URL: /posts/)."""
    subpage_types = ["cms.BlogPage"]
    # Optional intro text
    intro = StreamField(
        [("paragraph", blocks.RichTextBlock())],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    # Provide children in the template context
    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = (
            BlogPage.objects.live().descendant_of(self).order_by("-date")
        )
        return context

    # Prevent regular pages being added under /posts/

class BlogPage(Page):
    """A single blog article."""
    template = "cms/blog_page.html"
    date = models.DateField("Post date")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("subheading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link", "ul", "ol"])),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("embed", EmbedBlock()),
            ("html", blocks.RawHTMLBlock()),
            ("button", blocks.StructBlock([
                ("text", blocks.CharBlock(required=True)),
                ("url", blocks.URLBlock(required=True)),
            ])),

        ],
        use_json_field=True,
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    # Only allow BlogPage under BlogIndexPage
    parent_page_types = ["cms.BlogIndexPage"]
    subpage_types: list[str] = []  # can’t create pages beneath a post
