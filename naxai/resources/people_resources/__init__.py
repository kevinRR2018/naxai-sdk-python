"""
People resources package for the Naxai SDK.

This package provides access to customer data management resources including:
- Attributes: For managing custom contact properties and fields
- Contacts: For creating and managing individual customer profiles
- Exports: For exporting contact data from the platform
- Imports: For importing contact data into the platform
- Segments: For grouping contacts based on attributes and behaviors
"""

from .attributes import AttributesResource
from .contacts import ContactsResource
from .exports import ExportsResource
from .imports import ImportsResource
from .segments import SegmentsResource

__all__ = ["AttributesResource",
           "ContactsResource",
           "ExportsResource",
           "ImportsResource",
           "SegmentsResource"]

RESOURCE_CLASSES = {
    "attributes": AttributesResource,
    "contacts": ContactsResource,
    "exports": ExportsResource,
    "imports": ImportsResource,
    "segments": SegmentsResource
}
