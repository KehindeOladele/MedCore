from fastapi import HTTPException, status
from app.modules.organizations.exceptions import OrganizationError

"""
Department module exceptions.
"""

class DepartmentError(HTTPException):
    """
    Base exception for the Departments module.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class DepartmentAlreadyExistsError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="A department with this name already exists."
        )



class DepartmentNotFoundError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The department does not exist."
        )


class InvalidParentDepartmentError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The specified parent department does not exist."
        )


class CircularDepartmentHierarchyError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Circular department hierarchy detected."
        )


class DepartmentHasChildrenError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department has child departments and cannot be deleted."
        )


class DepartmentInUseError(DepartmentError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Department is currently in use and cannot "
                "be deleted."
            )
        )