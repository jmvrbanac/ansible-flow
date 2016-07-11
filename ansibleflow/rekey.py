import sys

from ansible.errors import AnsibleError
from ansible.parsing.vault import VaultLib


def load_vault_key(key_path):
    key = None
    with open(key_path, 'r') as fp:
        key = fp.read().strip()

    if key is None:
        raise Exception('Could not load key or it had zero content')

    return VaultLib(key)


def decrypt_file(file_path, vault):
    plaintext = None
    with open(file_path, 'r') as fp:
        ciphertext = fp.read()
        try:
            plaintext = vault.decrypt(ciphertext)
        except AnsibleError as e:
            print('Error: {0}'.format(e))
            print('Please verify that you are using the correct key.')
            sys.exit(1)

        return plaintext


def encrypt_file(plaintext, file_path, vault):
    with open(file_path, 'w') as fp:
        ciphertext = vault.encrypt(plaintext)
        fp.write(ciphertext)


def rekey_vault_file(original_file, new_file, original_vault, new_vault):
    plaintext = decrypt_file(original_file, original_vault)
    encrypt_file(plaintext, new_file, new_vault)

    print('Re-encrypted {}'.format(original_file))


def argument_handler(value, all_args):
    original_vault = load_vault_key(all_args.orig_key)
    new_vault = load_vault_key(all_args.new_key)

    rekey_vault_file(
        all_args.filename,
        all_args.filename,
        original_vault,
        new_vault
    )
