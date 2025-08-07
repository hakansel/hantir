from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from src.facade.hunter_io_helper import get_comma_seperated


class Response(BaseModel):
    status: str
    body: Optional[dict] = None
    error: Optional[str] = None
    total_email_count: Optional[int] = None


class DomainSearchEmailType(Enum):
    PERSONAL = "personal"
    GENERIC = "generic"


class DomainSearchEmailSeniority(Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    EXECUTIVE = "executive"


class DomainSearchEmailDepartment(Enum):
    EXECUTIVE = "executive"
    IT = "it"
    FINANCE = "finance"
    MANAGEMENT = "management"
    SALES = "sales"
    LEGAL = "legal"
    SUPPORT = "support"
    HR = "hr"
    MARKETING = "marketing"
    COMMUNICATION = "communication"
    EDUCATION = "education"
    DESIGN = "design"
    HEALTH = "health"
    OPERATIONS = "operations"


class DomainSearchRequiredFieldsDepartment(Enum):
    FULL_NAME = "full_name"
    POSITION = "position"
    PHONE_NUMBER = "phone_number"


class DomainSearchOptions(BaseModel):
    limit: int = 10
    offset: int = 0
    type_of_email: Optional[List[DomainSearchEmailType]] = None
    seniority_of_email: Optional[List[DomainSearchEmailSeniority]] = None
    department_of_email: Optional[List[DomainSearchEmailDepartment]] = None
    required_fields: Optional[List[DomainSearchRequiredFieldsDepartment]] = None

    def build_as_params(self) -> dict:
        return {
            "limit": self.limit,
            "offset": self.offset,
            "type": get_comma_seperated(self.type_of_email),
            "seniority": get_comma_seperated(self.seniority_of_email),
            "department": get_comma_seperated(self.department_of_email),
            "required": get_comma_seperated(self.required_fields),
        }
