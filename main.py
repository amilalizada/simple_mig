import sys
from cart import Cart
from exporter import get_exporter
from importer import get_importer
from utils import find_logger

#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

logger = find_logger(__name__)


def process(source: Cart, target: Cart):
    importer = get_importer(cart=source)
    source_data = importer.start()
    logger.info("Source data count %s", len(source_data))

    exporter = get_exporter(source_data, cart=target)
    number_of_entity_count = exporter.start()
    logger.info("Number of the entities migrated %s", number_of_entity_count)


if __name__ == "__main__":
    # extract the values FOR these variables from the command line options (flags)
    # python main.py --source_url http://source.com --source_token SOURCE --target_url http://target.com --target_token TARGET
    source_url = sys.argv[2]
    source_token = sys.argv[4]

    target_url = None
    target_token = None

    source_cart = Cart(source_url, source_token)
    target_cart = Cart(target_url, target_token)
    process(source_cart, target_cart)
