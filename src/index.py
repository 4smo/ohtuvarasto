"""Main module for demonstrating Varasto functionality."""
from varasto import Varasto


def nayta_getterit(olutta):
    """Display getter methods."""
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def nayta_setterit(mehua):
    """Display setter methods."""
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def nayta_virhetilanteet():
    """Display error situations."""
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)
    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def nayta_ylitaytto_olut(olutta):
    """Display olut overflow."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")


def nayta_ylitaytto_mehu(mehua):
    """Display mehu overflow."""
    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def nayta_ylivuoto_olut(olutta):
    """Display olut underflow."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")


def nayta_ylivuoto_mehu(mehua):
    """Display mehu underflow."""
    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def alusta_varastot():
    """Initialize and display storages."""
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")
    return mehua, olutta


def main():
    """Main function to demonstrate Varasto class usage."""
    mehua, olutta = alusta_varastot()
    nayta_getterit(olutta)
    nayta_setterit(mehua)
    nayta_virhetilanteet()
    nayta_ylitaytto_olut(olutta)
    nayta_ylitaytto_mehu(mehua)
    nayta_ylivuoto_olut(olutta)
    nayta_ylivuoto_mehu(mehua)


if __name__ == "__main__":
    main()
