"""Custom loader for loading interactives."""

from django.db import transaction
from django.conf import settings
from interactives.models import Interactive
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors.InvalidYAMLValueError import InvalidYAMLValueError


class InteractivesLoader(TranslatableModelLoader):
    """Custom loader for loading interactives."""

    @transaction.atomic
    def load(self):
        """Load the paths to interactive templates.

        MissingRequiredFieldError: When a config (yaml) file is missing a
            required field.
        """
        valid_language_codes = [lang[0] for lang in settings.LANGUAGES]
        interactives_structure = self.load_yaml_file(self.structure_file_path)
        interactive_translations = self.get_yaml_translations(
            self.structure_filename,
            required_slugs=interactives_structure.keys(),
            required_fields=["name"]
        )

        for interactive_slug, interactive_data in interactives_structure.items():
            translations = interactive_translations.get(interactive_slug, {})

            languages = interactive_data.get("languages", {})
            for language_code, template_path in languages.items():
                if language_code not in valid_language_codes:
                    error_text = "One of the following values:\n"
                    for code in valid_language_codes:
                        error_text += f"- {code}\n"
                    raise InvalidYAMLValueError(
                        self.structure_file_path,
                        "interactive's 'language' value",
                        error_text,
                    )
                else:
                    if not translations.get(language_code):
                        translations[language_code] = {}
                    translations[language_code]["template"] = template_path

            is_interactive = interactive_data.get("is_interactive")
            use_large_thumbnail = interactive_data.get("use_large_thumbnail")
            if use_large_thumbnail is None:
                use_large_thumbnail = False
            interactive, created = Interactive.objects.update_or_create(
                slug=interactive_slug,
                defaults={
                    'is_interactive': is_interactive,
                    'use_large_thumbnail': use_large_thumbnail,
                }
            )
            self.populate_translations(interactive, translations)
            self.mark_translation_availability(
                interactive,
                required_fields=["name", "template"]
            )
            interactive.save()

            term = 'Created' if created else 'Updated'
            self.log(f'{term} interactive: {interactive.__str__()}')
