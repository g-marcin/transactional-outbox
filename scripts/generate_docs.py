#!/usr/bin/env python3
"""Generate OpenAPI documentation from FastAPI app."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from main import app


def generate_openapi_json(output_path: Path = Path("openapi.json")) -> None:
    """Generate OpenAPI schema JSON file."""
    schema = app.openapi()
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"✓ OpenAPI schema generated: {output_path}")


def generate_openapi_yaml(output_path: Path = Path("openapi.yaml")) -> None:
    """Generate OpenAPI schema YAML file (requires PyYAML)."""
    try:
        import yaml
    except ImportError:
        print("PyYAML not installed. Install with: pip install pyyaml")
        return

    schema = app.openapi()
    with open(output_path, "w") as f:
        yaml.dump(schema, f, default_flow_style=False)
    print(f"✓ OpenAPI schema generated: {output_path}")


def generate_html_docs(output_path: Path = Path("api-docs.html")) -> None:
    """Generate standalone Swagger UI HTML file."""
    schema = app.openapi()
    schema_json = json.dumps(schema).replace("'", "\\'")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
        }}
    </style>
</head>
<body>
    <redoc spec-url='data:application/json;utf8,{schema_json}'>
    </redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"✓ HTML documentation generated: {output_path}")


def generate_markdown_docs(output_path: Path = Path("API.md")) -> None:
    """Generate Markdown documentation from OpenAPI schema."""
    schema = app.openapi()
    info = schema.get("info", {})
    paths = schema.get("paths", {})

    md = f"""# {info.get('title', 'API Documentation')}

{info.get('description', '')}

**Version:** {info.get('version', 'unknown')}

## Endpoints

"""

    for path, methods in sorted(paths.items()):
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue

            summary = operation.get("summary", "")
            description = operation.get("description", "")
            tags = operation.get("tags", [])
            operation_id = operation.get("operationId", "")

            md += f"### `{method.upper()} {path}`\n\n"
            if summary:
                md += f"**{summary}**\n\n"
            if tags:
                md += f"Tags: {', '.join(tags)}\n\n"
            if description:
                md += f"{description}\n\n"

            request_body = operation.get("requestBody", {})
            if request_body:
                md += "**Request Body:**\n```json\n"
                schema_ref = (
                    request_body.get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                )
                md += json.dumps(schema_ref, indent=2)
                md += "\n```\n\n"

            responses = operation.get("responses", {})
            if responses:
                md += "**Responses:**\n"
                for status, response_info in responses.items():
                    md += f"- **{status}:** {response_info.get('description', '')}\n"
                md += "\n"

    with open(output_path, "w") as f:
        f.write(md)
    print(f"✓ Markdown documentation generated: {output_path}")


def main() -> None:
    """Generate all documentation formats."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate OpenAPI documentation from FastAPI app"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate OpenAPI JSON schema",
    )
    parser.add_argument(
        "--yaml",
        action="store_true",
        help="Generate OpenAPI YAML schema",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate standalone HTML documentation",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Generate Markdown documentation",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all formats",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for generated files",
    )

    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.all or args.json:
        generate_openapi_json(output_dir / "openapi.json")
    if args.all or args.yaml:
        generate_openapi_yaml(output_dir / "openapi.yaml")
    if args.all or args.html:
        generate_html_docs(output_dir / "api-docs.html")
    if args.all or args.markdown:
        generate_markdown_docs(output_dir / "API.md")

    if not any([args.json, args.yaml, args.html, args.markdown, args.all]):
        print("Generating all formats...")
        generate_openapi_json(output_dir / "openapi.json")
        generate_html_docs(output_dir / "api-docs.html")
        generate_markdown_docs(output_dir / "API.md")

    print(f"\n✓ Documentation generated in {output_dir}")


if __name__ == "__main__":
    main()
