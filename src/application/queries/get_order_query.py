from dataclasses import dataclass


@dataclass
class GetOrderQuery:
    order_id: str
    include_items: bool = True