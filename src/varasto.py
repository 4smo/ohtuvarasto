"""Varasto module for managing storage."""
class Varasto:
    """Class representing a storage container."""
    def __init__(self, tilavuus, alku_saldo = 0):
        """Initialize Varasto with given volume and initial balance."""
        self.tilavuus = self._aseta_tilavuus(tilavuus)
        self.saldo = self._aseta_saldo(alku_saldo, tilavuus)

    def _aseta_tilavuus(self, tilavuus):
        """Set volume, zero if invalid."""
        if tilavuus > 0.0:
            return tilavuus
        return 0.0

    def _aseta_saldo(self, alku_saldo, tilavuus):
        """Set balance, validate against volume."""
        if alku_saldo < 0.0:
            return 0.0
        if alku_saldo <= tilavuus:
            return alku_saldo
        return tilavuus

    # huom: ominaisuus voidaan myös laskea.
    # Ei tarvita erillistä kenttää viela_tilaa tms.
    def paljonko_mahtuu(self):
        """Calculate how much space is available in the storage."""
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        """Add amount to the storage."""
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        """Remove amount from the storage and return the amount taken."""
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        """Return string representation of the storage."""
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
