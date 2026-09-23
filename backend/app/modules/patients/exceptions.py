# ----- Delivery Response Model -----
class EmailDeliveryError(Exception):
    """Email Fialed to Deliver."""
    pass

# ----- Patient Error Model -----
class PatientError(Exception):
    """Base patient exception."""
    pass


# ----- Patient Not Found Error Model -----
class PatientNotFoundError(PatientError):
    """Patient does not exist."""
    pass


# ----- Patient Create Error Model -----
class PatientCreationError(PatientError):
    """Failed to create patient."""
    pass


# ----- Patient Update Error Model -----
class PatientUpdateError(PatientError):
    """Failed to update patient."""
    pass


# ----- Clinician Assignemnt Error Model -----
class ClinicianAssignmentError(PatientError):
    """Failed clinician assignment."""
    pass