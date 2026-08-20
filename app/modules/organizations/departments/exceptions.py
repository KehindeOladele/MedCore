from app.modules.organizations.exceptions import OrganizationError

"""
Department module exceptions.
"""

class DepartmentError(OrganizationError):
    pass


class DepartmentAlreadyExistsError(
    DepartmentError
    ):
    default_message = (
        "A department with this name already exists."
    )


class InvalidParentDepartmentError(
    DepartmentError
    ):
    default_message = (
        "Invalid parent department."
    )


class CircularDepartmentHierarchyError(
    DepartmentError
    ):
    default_message = (
        "Circular department hierarchy detected."
    )


class DepartmentHasChildrenError(
    DepartmentError
    ):
    default_message = (
        "Department has child departments."
    )


class DepartmentInUseError(
    DepartmentError
    ):
    default_message = (
        "Department has child departments."
    )
