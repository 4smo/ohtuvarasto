"""Test module for Varasto class."""
import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Test class for Varasto functionality."""
    def setUp(self):
        """Set up test fixtures."""
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Test that constructor creates an empty storage."""
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Test that new storage has correct volume."""
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        """Test that adding increases balance."""
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Test that adding decreases available space."""
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Test that taking returns correct amount."""
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Test that taking increases available space."""
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_konstruktori_nollaa_negatiivisen_tilavuuden_ja_saldon(self):
        """Test that constructor zeros negative volume and balance."""
        v = Varasto(-1, -5)
        self.assertAlmostEqual(v.tilavuus, 0)
        self.assertAlmostEqual(v.saldo, 0)

    def test_konstruktori_tayttaa_kun_alkusaldo_yli_tilavuuden(self):
        """Test that constructor fills when initial balance exceeds volume."""
        v = Varasto(5, 8)
        self.assertAlmostEqual(v.tilavuus, 5)
        self.assertAlmostEqual(v.saldo, 5)

    def test_lisays_negatiivinen_ei_muuta_saldoa(self):
        """Test that negative addition does not change balance."""
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisays_yli_tilavuuden_tayttaa_varaston(self):
        """Test that adding over volume fills the storage."""
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_otto_negatiivinen_palauttaa_nolla_eika_muuta_saldoa(self):
        """Test negative taking returns zero and does not change balance."""
        saatu = self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(saatu, 0)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_otto_yli_saldon_tyhjentaa_varaston(self):
        """Test that taking over balance empties the storage."""
        self.varasto.lisaa_varastoon(6)
        saatu = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu, 6)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_str_muoto(self):
        """Test string representation format."""
        self.varasto.lisaa_varastoon(3)
        self.assertEqual(str(self.varasto), "saldo = 3, vielä tilaa 7")
