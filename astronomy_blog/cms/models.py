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


class AstroCalendarPage(Page, ClusterableModel):
    template = "cms/astrocalendar_page.html"

    # background_image = models.ForeignKey(
    #     'wagtailimages.Image',  # 👈 Correct usage in Wagtail 7
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+'
    # )

    content_panels = Page.content_panels + [
        # FieldPanel('background_image'),  # This works in Wagtail 7
        InlinePanel('events', label="Astronomical Events"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['events'] = self.events.all()
        return context

class AstroEvent(models.Model):
    page = ParentalKey(AstroCalendarPage, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    description = RichTextField()
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('eclipse', 'Eclipse'),
            ('meteor', 'Meteor Shower'),
            ('planetary', 'Planetary'),
            ('other', 'Other')
        ],
        default='other'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('description'),
        FieldPanel('event_type'),
    ]

    def __str__(self):
        return f"{self.title} on {self.date}"


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
