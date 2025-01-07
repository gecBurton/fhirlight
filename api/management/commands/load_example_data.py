import json
import os
from graphlib import TopologicalSorter

from django.core.management import BaseCommand

from api import serializers

EXAMPLE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tests", "data"
)


def extract_reference(document) -> set[str]:
    references = set()

    def _extract_reference(doc):
        if isinstance(doc, dict):
            for k, v in doc.items():
                if k == "reference":
                    references.add(v.split("/")[-1])
                else:
                    _extract_reference(v)
        elif isinstance(doc, list):
            for d in doc:
                _extract_reference(d)

    _extract_reference(document)
    return references


def get_examples() -> list[str]:
    examples = {}
    for file_path in os.listdir(EXAMPLE_DIR):
        with open(os.path.join(EXAMPLE_DIR, file_path)) as f:
            example = json.load(f)
        references = extract_reference(example)
        examples[file_path.removesuffix(".json")] = references
    graph = TopologicalSorter(examples)
    return list(graph.static_order())


def load_examples():
    file_names = get_examples()
    for file_name in file_names:
        with open(os.path.join(EXAMPLE_DIR, file_name + ".json")) as f:
            example = json.load(f)
        resource_type = file_name.split("-")[1] + "Serializer"

        serializer_class = getattr(serializers, resource_type)
        serializer = serializer_class(data=example)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_examples()
