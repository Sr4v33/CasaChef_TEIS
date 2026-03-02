from dataclasses import dataclass
from typing import Optional


@dataclass
class DailyProductionEntity:
    """Entidad de dominio DailyProduction.

    Representa los cupos de producción de un plato para un día concreto.
    Es el mecanismo central de control de sobreventas en CasaChef.
    """
    dish_id: int
    date: str               # formato ISO: YYYY-MM-DD
    available_units: int
    production_id: Optional[int] = None

    def reserve(self, quantity: int) -> None:
        """Reserva unidades del cupo diario."""
        if quantity <= 0:
            raise ValueError("La cantidad a reservar debe ser mayor a 0")
        if quantity > self.available_units:
            raise ValueError(
                f"No hay suficientes cupos: solicitado={quantity}, disponible={self.available_units}"
            )
        self.available_units -= quantity

    def adjust(self, new_units: int) -> None:
        """Ajusta los cupos disponibles del día."""
        if new_units < 0:
            raise ValueError("Los cupos disponibles no pueden ser negativos")
        self.available_units = new_units

    def has_availability(self, quantity: int) -> bool:
        return self.available_units >= quantity
