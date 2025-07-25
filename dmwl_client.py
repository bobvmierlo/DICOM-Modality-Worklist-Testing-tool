from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind

def query_worklist(query_data, calling_ae_title, called_ae_title, server_ip, server_port):
    # Create AE with calling AE title
    ae = AE(ae_title=calling_ae_title)
    ae.add_requested_context(ModalityWorklistInformationFind)

    ds = Dataset()
    # Wildcard around PatientName for "contains" match
    patient_name = query_data.get('PatientName', '').strip()
    ds.PatientName = f"*{patient_name}*" if patient_name else '*'
    ds.PatientID = query_data.get('PatientID', '')
    ds.AccessionNumber = query_data.get('AccessionNumber', '')

    sps_item = Dataset()
    sps_item.Modality = query_data.get('Modality', '')
    sps_item.ScheduledStationAETitle = query_data.get('StationAETitle', '')
    sps_item.ScheduledProcedureStepStartDate = query_data.get('StartDate', '')
    ds.ScheduledProcedureStepSequence = [sps_item]

    # Here the called AE title (server's AE) is specified
    assoc = ae.associate(server_ip, server_port, ae_title=called_ae_title)

    results = []
    if assoc.is_established:
        responses = assoc.send_c_find(ds, ModalityWorklistInformationFind)
        for (status, identifier) in responses:
            if status and identifier:
                results.append(identifier)
        assoc.release()
    else:
        raise ConnectionError("Association rejected or failed")

    return results
