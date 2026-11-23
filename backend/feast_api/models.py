from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Quote:
    id: int
    event_type: str
    event_date: str
    guests: int
    name: str
    email: str
    notes: str
    status: str
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(**{field: row[field] for field in cls.__dataclass_fields__})

    def to_dict(self):
        return asdict(self)
