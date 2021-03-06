import unittest
from propnet import ureg
from propnet.core.materials import Material
from propnet.core.quantity import QuantityFactory
from propnet.core.graph import Graph
from propnet.core.provenance import ProvenanceElement

from propnet.symbols import add_builtin_symbols_to_registry
from propnet.core.registry import Registry


class MaterialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        add_builtin_symbols_to_registry()
        # Create some test properties and a few base objects
        cls.q1 = QuantityFactory.create_quantity(Registry("symbols")['bulk_modulus'],
                                                 ureg.Quantity.from_tuple([200, [['gigapascals', 1]]]))
        cls.q2 = QuantityFactory.create_quantity(Registry("symbols")['shear_modulus'],
                                                 ureg.Quantity.from_tuple([100, [['gigapascals', 1]]]))
        cls.q3 = QuantityFactory.create_quantity(Registry("symbols")['bulk_modulus'],
                                                 ureg.Quantity.from_tuple([300, [['gigapascals', 1]]]))
        cls.material = None
        cls.graph = Graph()

    def setUp(self):
        self.material = Material()

    def test_material_setup(self):
        self.assertTrue(len(self.material._quantities_by_symbol) == 0,
                        "Material not initialized properly.")

    def test_material_add_quantity(self):
        self.material.add_quantity(self.q1)
        self.assertEqual(len(self.material._quantities_by_symbol), 1,
                         "Material did not add the quantity.")
        self.material.add_quantity(self.q2)
        self.assertEqual(len(self.material._quantities_by_symbol), 2,
                         "Material did not add quantity to itself.")

    def test_material_remove_quantity(self):
        self.material.add_quantity(self.q1)
        self.material.add_quantity(self.q2)
        self.material.remove_quantity(self.q1)
        self.assertEqual(
            len(self.material._quantities_by_symbol[Registry("symbols")['shear_modulus']]),
            1, "Material did not remove the correct quantity.")
        self.material.remove_quantity(self.q2)
        self.assertEqual(
            len(self.material._quantities_by_symbol[Registry("symbols")['shear_modulus']]),
            0, "Material did not remove the quantity correctly.")

    def test_material_remove_symbol(self):
        self.material.add_quantity(self.q1)
        self.material.add_quantity(self.q2)
        self.material.add_quantity(self.q3)
        self.material.remove_symbol(Registry("symbols")['bulk_modulus'])
        self.assertTrue(
            Registry("symbols")['shear_modulus'] in self.material._quantities_by_symbol.keys(),
            "Material did not remove Symbol correctly.")
        self.assertTrue(
            self.q2 in self.material._quantities_by_symbol[Registry("symbols")['shear_modulus']],
            "Material did not remove Symbol correctly.")
        self.assertEqual(len(self.material._quantities_by_symbol), 1,
                         "Material did not remove Symbol correctly.")

    def test_get_symbols(self):
        self.material.add_quantity(self.q1)
        self.material.add_quantity(self.q2)
        self.material.add_quantity(self.q3)
        out = self.material.get_symbols()
        self.assertEqual(
            len(out), 2, "Material did not get Symbol Types correctly.")
        self.assertTrue(Registry("symbols")['bulk_modulus'] in out,
                        "Material did not get Symbol Types correctly.")
        self.assertTrue(Registry("symbols")['shear_modulus'] in out,
                        "Material did not get Symbol Types correctly.")

    def test_get_quantities(self):
        self.material.add_quantity(self.q1)
        self.material.add_quantity(self.q2)
        self.material.add_quantity(self.q3)
        out = self.material.get_quantities()
        self.assertTrue(all([q in out for q in [self.q1, self.q2, self.q3]]),
                        "Material did not get Quantity objects correctly.")

    def test_get_aggregated_quantities(self):
        self.material.add_quantity(self.q1)
        self.material.add_quantity(self.q2)
        self.material.add_quantity(self.q3)
        agg = self.material.get_aggregated_quantities()
        # TODO: add a meaningful test here

    def test_add_default_quantities(self):
        material = Material(add_default_quantities=True)
        self.assertEqual(list(material['temperature'])[0],
                         QuantityFactory.create_quantity("temperature", 300,
                                                         provenance=ProvenanceElement(model='default')))
        self.assertEqual(list(material['relative_permeability'])[0],
                         QuantityFactory.create_quantity("relative_permeability", 1,
                                                         provenance=ProvenanceElement(model='default')))


if __name__ == "__main__":
    unittest.main()
