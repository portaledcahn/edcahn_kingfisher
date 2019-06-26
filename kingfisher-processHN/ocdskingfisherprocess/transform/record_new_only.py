from ocdskingfisherprocess.transform.base import BaseTransform
import sqlalchemy as sa
import ocdsmerge
import datetime
import json

class RecordTransformNewOnly(BaseTransform):

    def process(self):
        # Is deleted?
        if self.destination_collection.deleted_at:
            return

        # This transform can only run when the source collection is fully stored!
        #if not self.source_collection.store_end_at:
        #    return

        # Have we already marked this transform as finished?
        #if self.destination_collection.store_end_at:
        #    return

        # Do the work ...
        for ocid in self.get_ocids():
            #if not self.has_ocid_been_transformed(ocid):
            self.process_ocid(ocid)
            # Early return?
            if self.run_until_timestamp and self.run_until_timestamp < datetime.datetime.utcnow().timestamp():
                return

        # Mark Transform as finished
        self.database.mark_collection_store_done(self.destination_collection.database_id)

    def get_ocids(self):
        ocids = []

        with self.database.get_engine().begin() as engine:
            query = engine.execute(sa.text(
                " SELECT ocid FROM release_with_collection " +
                " WHERE collection_id = :collection_id"
                " GROUP BY ocid, data_id" +
                " HAVING COUNT(data_id) = 1"
            ), collection_id=self.source_collection.database_id)

            for row in query:
                ocids.append(row['ocid'])

        return ocids

    def get_record_by_ocid(self,ocids):
        ocids = None

        with self.database.get_engine().begin() as engine:
            query = engine.execute(sa.text(
                " SELECT record.id FROM record " +
                " WHERE record.ocid = " + ocids
            ), collection_id=self.source_collection.database_id)

            for row in query:
                ocids = row['id']
        return ocids

    def get_record_data_by_ocid(self,ocids):
        data_id = None

        with self.database.get_engine().begin() as engine:
            query = engine.execute(sa.text(
                " SELECT record.data_id FROM record " +
                " WHERE record.ocid = :ocids"
            ), collection_id=self.source_collection.database_id, ocids=ocids)

            for row in query:
                data_id = row['data_id']
        return data_id

    def has_ocid_been_transformed(self, ocid):

        with self.database.get_engine().begin() as engine:
            query = engine.execute(sa.text(
                " SELECT compiled_release.ocid FROM compiled_release " +
                " JOIN collection_file_item ON  collection_file_item.id = compiled_release.collection_file_item_id " +
                " JOIN collection_file ON collection_file.id = collection_file_item.collection_file_id  " +
                " WHERE collection_file.collection_id = :collection_id AND compiled_release.ocid = :ocid "
            ), collection_id=self.destination_collection.database_id, ocid=ocid)

            return query.rowcount == 1

    def process_ocid(self, ocid):

        releases = []

        with self.database.get_engine().begin() as engine:
            query = engine.execute(sa.text(
                " SELECT DISTINCT release.* FROM release " +
                " JOIN collection_file_item ON  collection_file_item.id = release.collection_file_item_id " +
                " JOIN collection_file ON collection_file.id = collection_file_item.collection_file_id  " +
                " WHERE collection_file.collection_id = :collection_id AND release.ocid = :ocid "
            ), collection_id=self.source_collection.database_id, ocid=ocid)

            for row in query:
                releases.append(self.database.get_data(row['data_id']))

        compiledRelease = ocdsmerge.merge(releases)
        versionedRelease = ocdsmerge.merge_versioned(releases)

        out = {'ocid':ocid,'releases':releases,'compiledRelease':compiledRelease,'versionedRelease':versionedRelease}

        recordDataId = self.get_record_data_by_ocid(ocid)

        if recordDataId is not None:
            with self.database.get_engine().begin() as engine:
                query = engine.execute(sa.text(
                    " UPDATE data " +
                    " SET data = :data" +
                    " WHERE id = :data_id "
                ), data=json.dumps(out),data_id=recordDataId)
        else:
            self.store.store_file_item(ocid+'.json', None, 'record', out, 1)