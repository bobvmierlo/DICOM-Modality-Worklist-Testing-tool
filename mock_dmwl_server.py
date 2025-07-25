import logging
import datetime
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
from pydicom.uid import generate_uid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MockDMWLServer")

def create_worklist_item(patient_name, patient_id, accession, modality, station_ae, procedure_date):
    ds = Dataset()
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    ds.AccessionNumber = accession
    ds.StudyInstanceUID = generate_uid()
    ds.RequestedProcedureID = "PROC" + patient_id
    ds.ScheduledProcedureStepSequence = [Dataset()]
    sps = ds.ScheduledProcedureStepSequence[0]
    sps.Modality = modality
    sps.ScheduledStationAETitle = station_ae
    sps.ScheduledProcedureStepStartDate = procedure_date.strftime("%Y%m%d")
    sps.ScheduledProcedureStepStartTime = procedure_date.strftime("%H%M%S")

    ds.IssuerOfPatientID = "MockIssuer"
    ds.PatientSex = "O"
    ds.PatientBirthDate = "19700101"
    ds.PatientAge = "055Y"
    ds.PatientWeight = "70"
    return ds

def matches(ds_query, ds_item):
    for elem in ds_query:
        if elem.VR == "SQ":
            continue
        query_val = str(elem.value).strip()
        if not query_val:
            continue
        val = getattr(ds_item, elem.keyword, None)
        if val is None:
            return False
        val_str = str(val).lower()
        qval = query_val.lower()
        if elem.keyword == "PatientName":
            if qval.strip('*') not in val_str:
                return False
        else:
            if val_str != qval:
                return False
    return True

def handle_find(event):
    ds = event.identifier
    logger.info(f"Received C-FIND request with criteria:\n{ds}")
    today = datetime.datetime.now()
    worklist = [
        create_worklist_item("Smith^John", "1001", "ACC1001", "CT", "CT_AE", today),
        create_worklist_item("Doe^Jane", "1002", "ACC1002", "MR", "MR_AE", today - datetime.timedelta(days=1)),
        create_worklist_item("Müller^Anna", "1003", "ACC1003", "US", "US_AE", today - datetime.timedelta(days=2)),
        create_worklist_item("Garcia^Luis", "1004", "ACC1004", "XR", "XR_AE", today - datetime.timedelta(days=3)),
        create_worklist_item("Kumar^Raj", "1005", "ACC1005", "NM", "NM_AE", today - datetime.timedelta(days=4)),
    ]
    for item in worklist:
        if matches(ds, item):
            logger.info(f"Sending worklist item for patient {item.PatientName}")
            yield 0xFF00, item
    yield 0x0000, None

if __name__ == "__main__":
    ae = AE(ae_title="DMWL_AE")
    ae.add_supported_context(ModalityWorklistInformationFind)

    # ✅ Alleen deze AE Titles mogen een associatie starten
    ae.require_calling_aet = ["MY_AE"]

    handlers = [(evt.EVT_C_FIND, handle_find)]
    logger.info("Starting Mock DMWL SCP on port 11112...")
    ae.start_server(("0.0.0.0", 11112), evt_handlers=handlers, block=True)
