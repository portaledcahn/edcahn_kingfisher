from ocdskingfisherprocess.transform.compile_releases import CompileReleasesTransform
from ocdskingfisherprocess.transform.upgrade_1_0_to_1_1 import Upgrade10To11Transform
from ocdskingfisherprocess.transform.record import RecordTransform
from ocdskingfisherprocess.transform.record_new_only import RecordTransformNewOnly
from ocdskingfisherprocess.transform import TRANSFORM_TYPE_COMPILE_RELEASES, TRANSFORM_TYPE_UPGRADE_1_0_TO_1_1, TRANSFORM_TYPE_RECORD, TRANSFORM_TYPE_RECORD_NEW_ONLY


def get_transform_instance(type, isopen, config, database, destination_collection, run_until_timestamp=None):
    if type == TRANSFORM_TYPE_COMPILE_RELEASES:
        return CompileReleasesTransform(config, database, destination_collection, run_until_timestamp=run_until_timestamp)
    elif type == TRANSFORM_TYPE_UPGRADE_1_0_TO_1_1:
        return Upgrade10To11Transform(config, database, destination_collection, run_until_timestamp=run_until_timestamp)
    elif type == TRANSFORM_TYPE_RECORD and isopen:
       return RecordTransform(config, database, destination_collection, run_until_timestamp=run_until_timestamp)
    elif type == TRANSFORM_TYPE_RECORD_NEW_ONLY:
        return RecordTransformNewOnly(config, database, destination_collection, run_until_timestamp=run_until_timestamp)
    else:
        raise Exception("That transform type is not known")
   