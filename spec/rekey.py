import tempfile

from ansibleflow import rekey
from spec import BaseSpec
from specter import require


class RekeyTests(BaseSpec):
    def before_each(self):
        self.key_file = tempfile.NamedTemporaryFile()
        with open(self.key_file.name, 'wb') as fp:
            fp.write('my_key_here')

        self.vault_key = rekey.load_vault_key(self.key_file.name)

    def can_encrypt_and_decrypt(self):
        enc_file = tempfile.NamedTemporaryFile()
        file_data = 'something'

        rekey.encrypt_file(file_data, enc_file.name, self.vault_key)
        require(len(open(enc_file.name, 'rb').read())).to.be_greater_than(0)

        pt = rekey.decrypt_file(enc_file.name, self.vault_key)
        require(pt).to.equal(file_data)
