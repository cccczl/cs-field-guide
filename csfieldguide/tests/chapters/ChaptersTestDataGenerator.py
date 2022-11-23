"""Create test data for chapter tests."""

import os.path
import yaml

from chapters.models import (
    Chapter,
    ChapterSection,
    GlossaryTerm,
)


class ChaptersTestDataGenerator:
    """Class for generating test data for chapters."""

    def __init__(self):
        """Create ChaptersTestDataGenerator object."""
        self.BASE_PATH = "tests/chapters/"
        self.LOADER_ASSET_PATH = os.path.join(self.BASE_PATH, "loaders/assets/")

    def load_yaml_file(self, yaml_file_path):
        """Load a yaml file.

        Args:
            yaml_file_path:  The path to a given yaml file (str).

        Returns:
            Contents of a yaml file.
        """
        yaml_file = open(yaml_file_path, encoding="UTF-8").read()
        return yaml.load(yaml_file)

    def create_chapter(self, number, introduction=None):
        """Create Chapter object.

        Args:
            number: Identifier of the chapter (int).

        Returns:
            Chapter object.
        """
        if not introduction:
            introduction = f"<p>Introduction for chapter {number}</p>"
        chapter = Chapter(
            slug=f"chapter-{number}",
            name=f"Chapter {number}",
            number=number,
            introduction=introduction,
        )

        chapter.save()
        return chapter

    def create_chapter_section(self, chapter, number):
        """Create ChapterSection object.

        Args:
            number: Identifier of the chapter section (int).

        Returns:
            ChapterSection object.
        """
        chapter_section = ChapterSection(
            slug=f"section-{number}",
            name=f"Section {number}",
            number=number,
            content=f"<p>Content for section {number}.</p>",
            chapter=chapter,
        )

        chapter_section.save()
        return chapter_section

    def create_glossary_term(self, number):
        """Create GlossaryTerm object.

        Args:
            number: Identifier of the glossary term (int).

        Returns:
            GlossaryTerm object.
        """
        glossary_term = GlossaryTerm(
            slug=f"glossary-term-{number}",
            term=f"Glossary Term {number}",
            definition=f"<p>Definition for glossary term {number}.</p>",
        )

        glossary_term.save()
        return glossary_term
