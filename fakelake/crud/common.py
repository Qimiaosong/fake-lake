import copy

_datasourceTypes = {
    0: "MySQL",
    1: "Kafka",
    2: "MaxCompute",
    3: "PostgreSQL",
    4: "Doris"
}

_ent_datasourceTypes = copy.copy(_datasourceTypes)

VersionDatasourceDict = {
    0: _datasourceTypes,
    1: _datasourceTypes,
    2: _ent_datasourceTypes,
    3: _datasourceTypes,
    4: _datasourceTypes,
    5: _datasourceTypes,
    6: _datasourceTypes,
    7: _datasourceTypes,
    8: _datasourceTypes
}
