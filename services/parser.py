from decimal import Decimal
from datetime import datetime
from typing import List, Optional

from schemas.product import (
    Image,
    Variant,
    ManufacturerEntity,
    CategoryInfo,
    SpecificPrice,
    Weight,
    Barcode,
    Product
)
from constants import SpecificPriceType

class Parser:
    
    def __init__(self, product: dict) -> None:
        self.product = product
        self.tags: List[str] = self.handle_tags
        self.images: List[Image] = self.handle_images

    def handle_product(self) -> Product:
        result = Product(
            id=self.product["id"],
            name=self.product["title"],
            description=self.product["body_html"],
            short_description=None,
            tags=self.tags,
            images=self.images,
            created_date=datetime.strptime(
                self.product["created_at"], "%Y-%m-%dT%H:%M:%S%z"
            ),
            updated_date=datetime.strptime(
                self.product["created_at"], "%Y-%m-%dT%H:%M:%S%z"
            ),
            is_active=self.product["status"] == "active",
            
        )
        return result


    def handle_tags(self) -> List[str]:
        tag_data = self.product.get("tags", None)
        tags = None
        if tag_data:
            tags = tag_data.split(",")

        return tags

    def handle_images(self) -> List[Image]:
        image_data = self.product.get("images", None)
        images: List[Image] = []
        is_cover = 0
        for i_d, idx in enumerate(image_data):
            if idx == 0:
                is_cover = 1
            position = i_d.get("position", None)
            image = Image(
                id=i_d["id"],
                path=i_d["src"],
                name=i_d["alt"],
                position=str(position),
                is_cover=is_cover,
                base64_attachment=None,
            )
            images.append(image)

        return images

    def handle_variants(self):
        variant_data = self.product["variants"]
        variants: List[Variant] = []

        for v_d in variant_data:
            variant = self.parse_variant(v_d)
            variants.append(variant)

        return variants

    def parse_variant(self, variant: dict):
        id = variant["id"]
        price = Decimal(variant["price"])
        sku = variant["sku"]
        
    

    