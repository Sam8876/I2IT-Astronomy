from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# from modelcluster.fields import ParentalManyToManyField
from wagtail.images.models import Image


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
    date = models.DateField("Post date", blank=True, null=True)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("subheading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "link", "ul", "ol"])),
            ("richtext", blocks.RichTextBlock(features=[
                "h2", "h3", "bold", "italic", "link", "ul", "ol", "image", "embed"
            ])),
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



class AstroEventPage(Page):
    template = "cms/astro_event_page.html"
    """Main page for Astro Events"""
    content_panels = Page.content_panels + [
        InlinePanel('carousel_images', label="Carousel Images"),
    ]
    subpage_types = []  # no subpages allowed
    max_count = 1  # only 1 page


class AstroEventImage(models.Model):
    """Carousel image linked to AstroEventPage"""
    page = ParentalKey(AstroEventPage, related_name="carousel_images", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    class Meta:
        ordering = ["id"]

# class AstroCalendarPage(Page, ClusterableModel):
#
#
#     content_panels = Page.content_panels + [
#         # FieldPanel('background_image'),  # This works in Wagtail 7
#         InlinePanel('events', label="Astronomical Events"),
#     ]
#
#     def get_context(self, request):
#         context = super().get_context(request)
#         context['events'] = self.events.all()
#         return context
#
# class AstroEvent(models.Model):
#     page = ParentalKey(AstroCalendarPage, related_name='events', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     date = models.DateField()
#     description = RichTextField()
#     event_type = models.CharField(
#         max_length=50,
#         choices=[
#             ('eclipse', 'Eclipse'),
#             ('meteor', 'Meteor Shower'),
#             ('planetary', 'Planetary'),
#             ('other', 'Other')
#         ],
#         default='other'
#     )
#
#     panels = [
#         FieldPanel('title'),
#         FieldPanel('date'),
#         FieldPanel('description'),
#         FieldPanel('event_type'),
#     ]
#
#     def __str__(self):
#         return f"{self.title} on {self.date}"

class MemberBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    title = blocks.CharBlock(required=True)
    photo = ImageChooserBlock(required=True)

class DepartmentBlock(blocks.StructBlock):
    department_name = blocks.CharBlock(required=True)
    members = blocks.ListBlock(MemberBlock())

    class Meta:
        template = "cms/blocks/department_block.html"
        icon = "group"
        label = "Department"

class AboutPage(Page):
    template = "cms/about_page.html"

    club_description = RichTextField()
    departments = StreamField([
        ("department", DepartmentBlock())
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("club_description"),
        FieldPanel("departments"),
    ]

class GalleryPage(Page):
    """
    The main Gallery page (one per site).
    Displays all categories with carousels of their images.
    """
    intro = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("categories", label="Gallery Categories"),
    ]


class GalleryCategory(ClusterableModel):
    """
    A category for grouping gallery images.
    Example: Eclipses, Planets, Club Events
    """
    page = ParentalKey(
        "GalleryPage",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,   # ✅ keep nullable for safety
        blank=True   # ✅ makes admin happy
    )
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel("title"),
        InlinePanel("images", label="Images"),
    ]

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    category = ParentalKey(
        "GalleryCategory",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+"
    )

    panels = [
        FieldPanel("image"),
    ]

    def __str__(self):
        return f"{self.image.title} ({self.category.title})"
