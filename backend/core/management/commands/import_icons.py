import csv
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from core.models import Icon, Tag


class Command(BaseCommand):
    help = "Import icons from local CSV + PNG/SVG folders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            default="data/map-icon-metadata.csv",
        )
        parser.add_argument(
            "--png",
            type=str,
            required=True,
            help="Folder with files like 00e8059e.png",
        )
        parser.add_argument(
            "--svg",
            type=str,
            required=True,
            help="Folder with files like 00e8059e.svg",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv"])
        if not csv_path.is_absolute():
            csv_path = Path.cwd() / csv_path

        png_dir = Path(options["png"])
        svg_dir = Path(options["svg"])

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")
        if not png_dir.exists():
            raise CommandError(f"PNG folder not found: {png_dir}")
        if not svg_dir.exists():
            raise CommandError(f"SVG folder not found: {svg_dir}")

        created = updated = 0
        missing_png = missing_svg = 0

        # utf-8-sig strips Excel's BOM so "unique-ID" matches correctly
        with csv_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                unique_id = (row.get("unique-ID") or "").strip()
                if not unique_id:
                    continue

                defaults = {
                    "designer": (row.get("designer") or "").strip(),
                    "metadata_source": (row.get("metadata-source") or "").strip(),
                    "uploader": (row.get("uploader") or "").strip(),
                    "primary_tag": (row.get("primary-tags") or "").strip(),
                    "when_created": (row.get("when-created") or "").strip(),
                    "when_uploaded": (row.get("when-uploaded") or "").strip(),
                    "where_created": (row.get("where-created") or "").strip(),
                    "icon_geography": (row.get("icon-geography") or "").strip(),
                    "icon_description": (row.get("icon-description") or "").strip(),
                    "icon_context": (row.get("icon-context") or "").strip(),
                    "creation_context": (row.get("creation-context") or "").strip(),
                    "notes": (row.get("notes") or "").strip(),
                }

                # status is set on first import only. In defaults it was reapplied on the
                # update path too, so every re-import republished the whole table and
                # silently undid reviews (a rejected icon came back published).
                icon, was_created = Icon.objects.update_or_create(
                    unique_id=unique_id,
                    defaults=defaults,
                    create_defaults={**defaults, "status": Icon.Status.PUBLISHED},
                )
                created += int(was_created)
                updated += int(not was_created)

                raw_tags = row.get("secondary-tags") or ""
                tag_objs = []
                for name in raw_tags.split(","):
                    name = name.strip()
                    if name:
                        tag, _ = Tag.objects.get_or_create(name=name)
                        tag_objs.append(tag)
                icon.tags.set(tag_objs)

                png_path = png_dir / f"{unique_id}.png"
                svg_path = svg_dir / f"{unique_id}.svg"

                if png_path.exists():
                    with png_path.open("rb") as pf:
                        icon.png_file.save(png_path.name, File(pf), save=True)
                else:
                    missing_png += 1

                if svg_path.exists():
                    with svg_path.open("rb") as sf:
                        icon.svg_file.save(svg_path.name, File(sf), save=True)
                else:
                    missing_svg += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created}, updated {updated}. "
                f"Missing PNG: {missing_png}, missing SVG: {missing_svg}."
            )
        )
