"""
CLI Tool for National Internship Ingestion.
Usage:
    python scripts/import_internships.py --catalog [--dry-run]
    python scripts/import_internships.py --file data.json [--dry-run] [--source "Partner Portal"]
    python scripts/import_internships.py --file data.csv [--dry-run]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from services.internship.importer import InternshipImporter
from services.internship.national_catalog import NATIONAL_INTERNSHIP_RECORDS


def main():
    parser = argparse.ArgumentParser(description="MPath National Internship Importer")
    parser.add_argument("--file", help="Path to JSON or CSV file to import")
    parser.add_argument("--catalog", action="store_true", help="Ingest built-in verified statutory and national catalog")
    parser.add_argument("--source", default="Official Portal Ingestion", help="Source name for the batch")
    parser.add_argument("--source-code", default="aicte-national-hub", help="Unique identifier code for source")
    parser.add_argument("--dry-run", action="store_true", help="Preview results without modifying database")

    args = parser.parse_args()

    with app.app_context():
        if args.catalog:
            print(f"[*] Running ingestion for {len(NATIONAL_INTERNSHIP_RECORDS)} verified national statutory records...")
            if args.dry_run:
                print("    [DRY-RUN MODE ACTIVATED: No changes will be written to database]")
            res = InternshipImporter.ingest_records(
                records=NATIONAL_INTERNSHIP_RECORDS,
                source_name=args.source,
                source_code=args.source_code,
                dry_run=args.dry_run
            )
            print("\n" + "=" * 50)
            print("IMPORT SUMMARY REPORT:")
            print(f"  Records Detected: {res['total_found']}")
            print(f"  New Inserted:     {res['new']}")
            print(f"  Updated/Refreshed:{res['updated']}")
            print(f"  Duplicates:       {res['duplicates']}")
            print(f"  Invalid Skipped:  {res['invalid']}")
            if res["errors"]:
                print(f"  Errors Encountered: {len(res['errors'])}")
                for err in res["errors"][:5]:
                    print(f"    - {err}")
            print("=" * 50)
            return

        if args.file:
            path = args.file
            if not os.path.exists(path):
                print(f"[!] Error: File '{path}' does not exist.")
                sys.exit(1)
            print(f"[*] Ingesting file: {path}")
            if args.dry_run:
                print("    [DRY-RUN MODE ACTIVATED: No changes will be written to database]")
            if path.endswith(".json"):
                res = InternshipImporter.import_from_json(path, source_name=args.source, dry_run=args.dry_run)
            elif path.endswith(".csv"):
                res = InternshipImporter.import_from_csv(path, source_name=args.source, dry_run=args.dry_run)
            else:
                print("[!] Unsupported file format. Please provide .json or .csv")
                sys.exit(1)

            print("\n" + "=" * 50)
            print("IMPORT SUMMARY REPORT:")
            print(f"  Records Detected: {res['total_found']}")
            print(f"  New Inserted:     {res['new']}")
            print(f"  Updated/Refreshed:{res['updated']}")
            print(f"  Duplicates:       {res['duplicates']}")
            print(f"  Invalid Skipped:  {res['invalid']}")
            print("=" * 50)
            return

        parser.print_help()


if __name__ == "__main__":
    main()
