from pydantic import BaseModel


class TerminologyCode(BaseModel):
    system: str
    code: str
    display: str