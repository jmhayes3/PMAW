import os

import betamax

from betamax_serializers import pretty_json


betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = "tests/cassettes/"
    config.default_cassette_options["serialize_with"] = "prettyjson"
    config.default_cassette_options["match_requests_on"] = [
        "method",
        "uri",
        # "headers",
    ]
    config.define_cassette_placeholder(
        "<AUTH_TOKEN>",
        os.environ.get("X_MESSARI_API_KEY")
    )
    # config.preserve_exact_body_bytes = True
