import argparse
import kserve
from kserve import logging

from .feast_transformer import FeastTransformer

parser = argparse.ArgumentParser(parents=[kserve.model_server.parser])
parser.add_argument(
    "--feast_url",
    type=str,
    help="URL for the Feast online feature server, in the name of <host_name>:<port>",
    required=True,
)
parser.add_argument(
    "--feast_entity_id",
    type=str,
    help="Name of the entity ID key for feature store lookups.",
    required=True,
)
parser.add_argument(
    "--feature_service",
    type=str,
    help="Name of the feature service to retrieve from the feature store.",
    required=True,
)

args, _ = parser.parse_known_args()

if __name__ == "__main__":
    if args.configure_logging:
        logging.configure_logging(args.log_config_file)
    transformer = FeastTransformer(
        feast_url=args.feast_url,
        feast_entity_id=args.feast_entity_id,
        feature_service=args.feature_service,
        model_name=args.model_name,
        predictor_host=args.predictor_host,
        predictor_protocol=args.predictor_protocol,
    )
    server = kserve.ModelServer()
    server.start(models=[transformer])