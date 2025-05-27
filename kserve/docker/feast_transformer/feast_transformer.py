import json
from typing import Dict, List, Union

import kserve
import numpy as np
import requests

from kserve import InferInput, InferRequest, InferResponse
from kserve.model import PredictorConfig, PredictorProtocol
from kserve.logging import logger
from kserve.protocol.grpc import grpc_predict_v2_pb2 as pb


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
        """Extract entity IDs and return them as a dict.

        Args:
            payload (Dict|InferRequest): Input payload containing entity IDs.

        Returns:
            Dict: A dictionary containing the extracted entity IDs.
        """
        pass
        # TODO: Handle the payload based on the protocol
        # the protocol here means the protocol of the transformer
        # # REST v2 and gRPC v2 protocols use InferRequest
        # if isinstance(payload, InferRequest):
        #     pass
        #     inputs = {}
        #     for infer_input in payload.inputs:
        #         inputs[infer_input.name] = infer_input.data
        # # REST v1 protocol uses a dict with "instances" key
        # else:
        #     pass
        #     payload = {
        #         "instances": [
        #             {"entity_id": "v5zlw0"},
        #             ...
        #         ]
        #     }
        #     entities = {}
        #     entity_ids = []
        #     for instance in payload["instances"]:
        #         entity_ids.append(instance[self.feast_entity_id])
        #     entities[self.feast_entity_id] = entity_ids
        #     entities = {
        #         "entity_id": ["v5zlw0", "dllwj31", ...]
        #     }
        #     return entities

    def build_predict_request(self, feast_results: Dict) -> Dict:
        """Build the predict request for all entities and return it as a dict.

        Args:
            feast_results (Dict): entity feast_results extracted from the feature store

        Returns:
            Dict: Returns the entity ids with feast_results

        """
        feature_names = feast_results["metadata"]["feature_names"]
        results = feast_results["results"]
        num_datapoints = len(results[0]["values"])
        num_features = len(feature_names) - 1 # Exclude the entity ID feature

        instances = []
        for i in range(num_datapoints):
            instance = []
            for j, feature_name in enumerate(feature_names):
                if feature_name != self.feast_entity_id:
                    feature = results[j]["values"][i]
                    instance.append(feature)
            instances.append(instance)
        # for v1 predictor protocol, we can directly pass the dict
        if self.protocol == PredictorProtocol.REST_V1.value:
            logger.info(f"I'M IN REST V1 BLOCK! build_predict_request")
            output = {"instances": instances}
            return output
        # for v2 predictor protocol, we need to build an InferRequest
        else:
            logger.info(f"I'M IN REST V2 BLOCK! build_predict_request")
            data = np.array(instances, dtype=np.float32).flatten()
            logger.info(f"Data shape: {data.shape}, Data type: {data.dtype}")
            infer_inputs = [
                InferInput(
                    name="INPUT_0",
                    datatype="FP32",
                    shape=[
                        num_datapoints,
                        num_features,
                    ],
                    data=pb.InferTensorContents(fp32_contents=data),
                )
            ]
            output = InferRequest(
                model_name=self.name,
                infer_inputs=infer_inputs
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
            Dict|InferRequest: Transformed payload to ``predict`` handler or return InferRequest for predictor call.
        """
        logger.info(f"Headers: {headers}")
        logger.info(f"Type of payload: {type(payload)}")
        logger.info(f"Payload:")
        logger.info(f"    Model Name: {payload.model_name}")
        logger.info(f"    From gGRPC: {payload.from_grpc}")
        logger.info(f"    Parameters: {payload.parameters}")

        logger.info(f"Length of payload.inputs : {len(payload.inputs)}")
        for i, infer_input in enumerate(payload.inputs):
            logger.info(f"    payload.inputs[{i}].name : {infer_input.name}")
            logger.info(f"    payload.inputs[{i}].datatype : {infer_input.datatype}")
            logger.info(f"    payload.inputs[{i}].shape : {infer_input.shape}")
            logger.info(f"    payload.inputs[{i}].data : {infer_input.data}")
            logger.info(f"")
        # TODO: Prepare and send a request for the feast online feature server
        # feast_response = requests.post(
        #     self.feast_url,
        #     data=json.dumps({
        #         "feature_service": self.feature_service,
        #         "entities": self.extract_entity_ids(payload)
        #     }),
        #     headers={
        #         "Content-Type": "application/json",
        #         "Accept": "application/json"
        #     }
        # )
        # feast_results = feast_response.json()
        feast_results = {
            "metadata": {
                "feature_names": [
                    "entity_id",
                    "transaction_count_7d",
                    "credit_score",
                    "account_age_days",
                    "user_has_2fa_installed",
                    "user_has_fraudulent_transactions_7d"
                ]
            },
            "results": [
                {
                    "values": [
                        "v5zlw0", "2jf7aw"
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "1970-01-01T00:00:00Z"
                    ]
                },
                {
                    "values": [
                        None, 1
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "1970-01-01T00:00:00Z"
                    ]
                },
                {
                    "values": [
                        480, 520
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "2025-04-29T22:00:34Z"
                    ]
                },
                {
                    "values": [
                        655, 399
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "2025-04-29T22:00:34Z"
                    ]
                },
                {
                    "values": [
                        1, 2
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "2025-04-29T22:00:34Z"
                    ]
                },
                {
                    "values": [
                        0.0, 0.0
                    ],
                    "statuses": [
                        "PRESENT"
                    ],
                    "event_timestamps": [
                        "2025-05-05T22:00:50Z"
                    ]
                }
            ]
        }

        # TODO: Prepare the request for the predictor
        output = self.build_predict_request(feast_results)
        logger.info(f"Output of preprocess: {output}")
        logger.info(f"Type of output: {type(output)}")
        return output
