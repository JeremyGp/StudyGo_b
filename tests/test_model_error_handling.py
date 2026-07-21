import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.usuario import Usuario


class ModelErrorHandlingTest(unittest.TestCase):
    def test_usuario_rechaza_parametros_invalidos_con_error_amigable(self):
        with self.assertRaises(ValueError):
            Usuario(campo_invalido=True)

    def test_usuario_puede_crearse_con_datos_validos(self):
        usuario = Usuario(nombre="Ana", correo="ana@example.com", contrasena_hash="hash123")
        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.correo, "ana@example.com")


if __name__ == "__main__":
    unittest.main()
