from decimal import Decimal
from datetime import datetime
import enum
from typing import List, Optional

from schemas.product import (
    Image,
    Variant,
    SpecificPrice,
    Weight,
    Barcode,
    AttributeGroup,
    AttributePair,
    Attribute,
    Stock,
    Product,
    WeightUnit
)
from constants import SpecificPriceType, WeightUnit

class Parser:
    
    def __init__(self, product: dict) -> None:
        self.product = product
        self.tags: List[str] = self.handle_tags
        self.attribute_groups: List[AttributeGroup] = self.parse_attribute_groups()
        self.images: List[Image] = self.handle_images
        self.variants: List[Variant] = self.handle_variants()


    def handle_product(self) -> Product:
        product = Product(
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
            is_taxable=None,
            is_virtual=None,
            link_rewrite=None,
            lang_id=None,
            meta_title=None,
            meta_description=None,
            variants=self.variants,
            price=self.variants[0].price,
            weight=self.variants[0].weight,
            barcode=self.variants[0].barcode,
            categories=None,
            manufacturers=self.product["vendor"],
            specific_prices=self.variants[0].specific_prices,
            cost=None,
            sku=self.variants[0].sku,
            shop_id=None,
            stock=self.variants[0].stock,
            
        )

        return product


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

    def parse_variant(self, variant: dict) -> Variant:

        gram = Decimal(variant["grams"])
        weight = Weight(
            value=gram,
            weight_unit=WeightUnit.GR,
        )

        stock = Stock(
            quantity=variant["inventory_quantity"],
            out_of_stock_action=None,
        )
        id = variant["id"]
        price = Decimal(variant["price"])
        sku = variant["sku"]
        attribute_pairs = self.variant_option(variant)
        images = self.variant_image(variant)
        
        variant = Variant(
            id=id,
            sku=sku,
            barcode=Barcode(ean_13=variant["barcode"], upc=None),
            price=price,
            weight=weight,
            images=images,
            stock=stock,
            attribute_pairs=attribute_pairs,
            specific_prices=None,
        )

        return variant

    def parse_attribute_groups(self) -> List[AttributeGroup]:

        options = self.product.get("options", None)
        attribute_groups: List[AttributeGroup] = []
        for option in options:
            attribute_group = self.attribute_group(option)
            attribute_groups.append(attribute_group)
            
        return attribute_groups

    def attribute_group(self, option: dict) -> AttributeGroup:
        attribute_group = AttributeGroup(
            id=option["id"],
            name=option["name"],
            lang_id=None,
            attributes={},
        )

        attributes = option.get("values", [])
        for attribute in attributes:
            attribute = Attribute(
                id=None,
                name=attribute,
                position=None,
                lang_id=None,
            )
            attribute_group.attributes[attribute.name] = attribute

        return attribute_group


    def variant_option(self, variant: dict) -> List[AttributePair]:

        attribute_pairs: List[AttributePair] = []
        options = [variant["option1"], variant["option2"], variant["option3"]]
        options = {
            "option_1": variant["option1"],
            "option_2": variant["option2"],
            "option_3": variant["option3"],
        }

        for i, v in enumerate(options.values()):
            if not v:
                continue

            attribute_group = self.attribute_groups[i]
            attr_pair = AttributePair(
                attribute=attribute_group.get_attribute_by(v),
                attribute_group=attribute_group,
            )
            attribute_pairs.append(attr_pair)

        return attribute_pairs

    def variant_image(self, variant: dict) -> Optional[List[Image]]:
    
        id = variant.get("image_id", None)
        if id:
            for image in self.images:
                if image.id == id:
                    return [image]
        return None

    