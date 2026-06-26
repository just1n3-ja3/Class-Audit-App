from dataclasses import dataclass


@dataclass
class Transaction:
    timestamp: str
    name: str
    record_type: str
    amount: float
    remarks: str

    def __str__(self):
        remarks_part = f" | {self.remarks}" if self.remarks else ""
        return (
            f"[{self.timestamp}] {self.name:<20} "
            f"{self.record_type:<10} ₱{self.amount:>10,.2f}{remarks_part}"
        )