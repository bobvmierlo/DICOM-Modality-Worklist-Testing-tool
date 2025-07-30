from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind

def query_worklist(query_data, calling_ae_title, called_ae_title, server_ip, server_port):
    ae = AE(ae_title=calling_ae_title)
    ae.add_requested_context(ModalityWorklistInformationFind)

    ds = Dataset()

    # Patient-related attributes
    ds.PatientName = f"*{query_data.get('PatientName', '').strip()}*" if query_data.get('PatientName') else '*'
    ds.PatientID = query_data.get('PatientID', '')
    ds.AccessionNumber = query_data.get('AccessionNumber', '')
    ds.PatientBirthDate = ''
    ds.PatientSex = ''
    ds.PatientSize = ''
    ds.PatientWeight = ''
    ds.PregnancyStatus = ''
    ds.MedicalAlerts = ''
    ds.Allergies = ''
    ds.PatientComments = ''
    ds.IssuerOfPatientID = ''

    # Study/Request-related attributes
    ds.RequestedProcedureID = ''
    ds.RequestedProcedureDescription = ''
    ds.RequestedProcedurePriority = ''
    ds.ConfidentialityConstraintOnPatientDataDescription = ''
    ds.ReferringPhysicianName = ''
    ds.RequestingPhysician = ''
    ds.StudyInstanceUID = ''

    # Visit-related attributes
    ds.AdmissionID = ''
    ds.SpecialNeeds = ''
    ds.CurrentPatientLocation = ''
    ds.PatientState = ''

    # Referenced study (optional)
    referenced_study = Dataset()
    referenced_study.ReferencedSOPClassUID = ''
    referenced_study.ReferencedSOPInstanceUID = ''
    ds.ReferencedStudySequence = [referenced_study]

    # Specific character set (to avoid encoding issues)
    ds.SpecificCharacterSet = 'ISO_IR 100'

    # Scheduled Procedure Step Sequence
    sps_item = Dataset()
    sps_item.Modality = query_data.get('Modality', '')
    sps_item.ScheduledStationAETitle = query_data.get('StationAETitle', '')
    sps_item.ScheduledProcedureStepStartDate = query_data.get('StartDate', '')
    sps_item.ScheduledProcedureStepStartTime = ''
    sps_item.ScheduledPerformingPhysicianName = ''
    sps_item.ScheduledProcedureStepDescription = ''
    sps_item.ScheduledProcedureStepID = ''
    sps_item.ScheduledStationName = ''
    sps_item.ScheduledProcedureStepLocation = ''

    # Protocol Code Sequence inside SPS
    protocol_code_item = Dataset()
    protocol_code_item.CodeValue = ''
    protocol_code_item.CodingSchemeDesignator = ''
    protocol_code_item.CodeMeaning = ''
    sps_item.ScheduledProtocolCodeSequence = [protocol_code_item]

    ds.ScheduledProcedureStepSequence = [sps_item]

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
