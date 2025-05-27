import base64
import json
from typing import Dict, List, Union

import numpy as np
import requests
from kserve.logging import logger
from kserve.model import PredictorConfig, PredictorProtocol
from kserve.protocol.grpc import grpc_predict_v2_pb2 as pb

import kserve
from kserve import InferInput, InferRequest, InferResponse


class FeastTransformer(kserve.Model):
    """A class object for the data handling activities of driver ranking
    Task and returns a KServe compatible response.

    Args:
        kserve (class object): The Model class from the KServe
        module is passed here.
    """

    def __init__(
        self,
        feast_url: str,
        feast_entity_id: str,
        feature_service: str,
        model_name: str,
        predictor_host: str,
        predictor_protocol: str,
    ):
        """Initialize the model name, predictor host, Feast serving URL,
           entity IDs, and feature references

        Args:
            feast_url (str): URL for the Feast online feature server, in the name of <host_name>:<port>.
            feast_entity_id (str): Name of the entity ID key for feature store lookups.
            feature_service (str): Name of the feature service to retrieve from the feature store.
            model_name (str): Name of the model used on the endpoint path (default is "model").
            predictor_host (str): Hostname for calling the predictor from the transformer (default is None).
            predictor_protocol (str): Inference protocol for the predictor (default is "v1").
        """
        super().__init__(
            name=model_name,
            predictor_config=PredictorConfig(
                predictor_host=predictor_host,
                predictor_protocol=predictor_protocol,
            )
        )
        self.feast_url = feast_url
        self.feast_entity_id = feast_entity_id
        self.feature_service = feature_service
        # self.predictor_host = predictor_host
        # self.predictor_protocol = predictor_protocol
        logger.info("Feast Online Feature Server URL = %s", feast_url)
        logger.info("Entity ID = %s", feast_entity_id)
        logger.info("Feature Service = %s", feature_service)
        logger.info("Model Name = %s", model_name)
        self.ready = True
        # logger.info("Predictor Host = %s", predictor_host)
        # logger.info("Predictor Protocol = %s", predictor_protocol)

    def extract_entity_ids(self, payload: Union[Dict, InferRequest]) -> Dict:
        """Extract entity IDs from the input payload.

        This method processes the input payload to extract entity IDs based on the 
        protocol (REST v1, REST v2, or gRPC v2) and returns them in a dictionary format.

        Args:
            payload (Dict|InferRequest): The input payload containing entity IDs.

        Returns:
            entites (Dict): A dictionary with the extracted entity IDs. For example:
            {
            "entity_id": ["v5zlw0", "000q95"]
            }
        """
        # The protocol here refers to the protocol used by the transformer deployment
        # v2
        if isinstance(payload, InferRequest):
            infer_input = payload.inputs[0]
            entity_ids = [
                # Decode each element based on the protocol: gRPC uses raw bytes, REST uses base64-encoded strings
                d.decode(
                    'utf-8') if payload.from_grpc else base64.b64decode(d).decode('utf-8')
                for d in infer_input.data
            ]
        # REST v1, type(payload) = Dict
        else:
            entity_ids = [
                instance[self.feast_entity_id]
                for instance in payload["instances"]
            ]

        return {self.feast_entity_id: entity_ids}

    def create_inference_request(self, feast_results: Dict) -> Union[Dict, InferRequest]:
        """Create the inference request for all entities and return it as a dict.

        Args:
            feast_results (Dict): entity feast_results extracted from the feature store

        Returns:
            output (Dict|InferRequest): Returns the entity ids with feast_results
        """
        feature_names = feast_results["metadata"]["feature_names"]
        results = feast_results["results"]
        num_datapoints = len(results[0]["values"])
        num_features = len(feature_names)

        # for v1 predictor protocol, we can directly pass the dict
        if self.protocol == PredictorProtocol.REST_V1.value:
            output = {
                "instances": [
                    {
                        feature_names[j]: results[j]['values'][i] for j in range(num_features) if feature_names[j] != "entity_id"
                    }
                    for i in range(num_datapoints)
                ]
            }
        # for v2 predictor protocol, we need to build an InferRequest
        else:
            # TODO: find a way to not hardcode the data types
            type_map = {
                "has_fraud_7d": "BOOL",
                "num_transactions_7d": "INT64",
                "credit_score": "INT64",
                "account_age_days": "INT64",
                "has_2fa_installed": "BOOL",
            }
            map_datatype = lambda feature_name: type_map.get(feature_name, "BYTES")

            output = InferRequest(
                model_name=self.name,
                parameters={
                    "content-type": "pd"
                },
                infer_inputs=[
                    InferInput(
                        name=feature_names[j],
                        datatype=map_datatype(feature_names[j]),
                        shape=[num_datapoints],
                        data=[
                            results[j]["values"][i]
                            for i in range(num_datapoints)
                        ]
                    )
                    for j in range(num_features)
                    if feature_names[j] != "entity_id"
                ]
            )
 
        return output

    def preprocess(
        self, payload: Union[Dict, InferRequest], headers: Dict[str, str] = None
    ) -> Union[Dict, InferRequest]:
        """Pre-process activity of the driver input data.

        Args:
            payload (Dict|InferRequest): Body of the request, v2 endpoints pass InferRequest.
            headers (Dict): Request headers.

        Returns:
            output (Dict|InferRequest): Transformed payload to ``predict`` handler or return InferRequest for predictor call.
        """
        logger.info(f"Headers: {headers}")
        logger.info(f"Type of payload: {type(payload)}")
        logger.info(f"Payload: {payload}")

        # Prepare and send a request for the Feast online feature server
        entites = self.extract_entity_ids(payload)
        logger.info(f"Extracted entities: {entites}")
        feast_response = requests.post(
            f"{self.feast_url}/get-online-features",
            data=json.dumps({
                "feature_service": self.feature_service,
                "entities": entites
            }),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        # Parse the response from the Feast online feature server
        if feast_response.status_code != 200:
            logger.error(
                f"Error fetching features from Feast: {feast_results}")
            raise Exception(
                f"Error fetching features from Feast: {feast_results}")
        feast_results = feast_response.json()
        logger.info(f"Feast results: {feast_results}")

        output = self.create_inference_request(feast_results)
        logger.info(f"Type of output: {type(output)}")
        logger.info(f"Output of preprocess: {output}")
        return output
