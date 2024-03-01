import argparse

import tritonclient.grpc as grpcclient

FLAGS = None

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--token",
        action="store_true",
        required=True,
        default=False,
        type=str,
        help="You can get tir auth token, project and endpoint from TIR dashboard >> Your Project >> API Tokens",
    )

    parser.add_argument(
        "-p",
        "--project",
        action="store_true",
        required=True,
        default=False,
        type=str,
        help=" You can get project id from TIR dashboard >> Your Project >> Endpoints >> Your Endpoint >> API Request",
    )

    parser.add_argument(
        "-s",
        "--svc",
        action="store_true",
        required=True,
        default=False,
        type=str,
        help="You can get svc id from TIR dashboard >> Your Project >> Endpoints >> Your Endpoint >> API Request",
    )

    FLAGS = parser.parse_args()

    triton_client = grpcclient.InferenceServerClient( url="infer-grpc.e2enetworks.net:9000", verbose=True, ssl=True)

    headers={'x-auth-token': FLAGS.token, 'e2e-project': FLAGS.project, 'svc': FLAGS.svc}
    
    triton_client.get_model_repository_index(headers=headers)
    
