from databricks.labs.community_connector.sources.absorb.absorb import AbsorbLakeflowConnect
from tests.unit.sources.test_suite import LakeflowConnectTests


class TestAbsorbConnector(LakeflowConnectTests):
    connector_class = AbsorbLakeflowConnect
    sample_records = 5
