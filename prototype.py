"""
Copyright (c) 2025, by TheMadWhisperer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

-------------------------------------------------------------------------------------

INTENTION:

This system was designed to weather even the most advanced attacks powered by quantum
computers that may possess power that is not yet known at the time the code is written.

The algorithm does not rely on mathematical formulas, but on a deterministic entropy driven
walk in a maze of mirros. Think of it this way: The maze shifts its shape each time you
take a step and if you try to observe, you'll never know where you were or where you are
actually going. But with the right key, you will get there.

                                                                        - TheMadWhisperer

This source file is a proof of concept. For the experimental API, please refer to "./src"
"""

"""
API sketch
encrypt(password, entropy block, plaintext, align?)
decrypt(password, entropy block)
config(argon2 time cost > limit, argon2 memory cost > limit)
"""

import argon2 as argon2
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

"""
This is an example field of entropy. Any length can be used. Preferably 1024.
Please keep in mind this is just a demonstration. The actual API uses naturally
sourced entropy field of 1024 bytes.
"""
field = list("d9226d4bd8779baa69db272f89a2e05c")
# field   = list("                                ")
field = [ord(x) for x in field]
# field = [0x00 for x in field]
field[0]=0x0

"""
Argon2 makes brute-forcing more painful and using quantum computers more wasteful.
It can be updated, exchanged for a quantum algoritm, tuned up in time or memory cost. 
"""
argon_output = argon2.hash_password_raw(
    b"Password123",
    b"pepper for salt",
    time_cost=30, # tune as needed (preferably as high as your CPU can handle without melting)
    memory_cost=262144,
    parallelism=1,
    hash_len=1024, # can we derive hash_len from entropy ORed together, just for fun?
    type=argon2.low_level.Type.ID)

def blender(x, y):
    for a,i in enumerate(x):
        y.insert((a+i)%len(y), y.pop(i%(len(y)-1)))

def rotate_L(x, y):
    r=y[y[0]%len(y)]
    # print("rotating left by", r%len(field), "chars")
    for i in range(0, r%len(field)):
        y.insert(-1, y.pop(0))

def rotate_R(x, y):
    r=y[y[0]%len(y)]
    # print("rotating right by", r%len(field), "chars")
    for i in range(0, r%len(field)):
        y.insert(0, y.pop(-1))


"""
This is the magical swarm of machines that transform keys deterministically,
but irreversibly - making them essentially quantum and AI resilient.

Even if you reconstruct the whole transformation path with a correct key,
nothing you might learn from it will be useful - it's always one of a kind
journey that can only be walked with the correct key.

In this practical example, we are using lambda and fixed args for ease of use.

x: argon2 array, y: field array, a: argon2 index, b: field intex
"""
lut = [
    lambda x,y,a,b: y.__setitem__(b, ((y[b]*x[a]))),
    lambda x,y,a,b: y.__setitem__(b, (y[b]+1)),
    lambda x,y,a,b: y.__setitem__(b, (y[b]-1)),
    lambda x,y,a,b: y.__setitem__(b, y[b]+x[a]),
    lambda x,y,a,b:  blender(x, y),
    lambda x,y,a,b:  rotate_L(x, y),
    lambda x,y,a,b:  rotate_R(x, y)]

for a,i in enumerate(argon_output):
    selector  = (i%len(lut)) -1
    lut[selector](argon_output, field, a%len(field), a%len(field))

field = [chr(x%0xFF) for x in field]
field = ''.join(field)
print("mirror machine key:", field)

"""
When we are done dancing while blindfolded, and we got to the correct door,
we may try to open the door now - hoping for the best.
"""
plaintext = b"This is test of encryption"

hkdf = HKDFExpand(
    algorithm=hashes.BLAKE2b(64),
    length=32,
    info=b"key",
)

key = hkdf.derive(bytes(field, 'utf-8'))
print("key:", key)

hkdf = HKDFExpand(
    algorithm=hashes.BLAKE2b(64),
    length=16,
    info=b"nonce",
)

nonce = hkdf.derive(bytes(field, 'utf-8'))
print("nonce:", nonce)

hkdf = HKDFExpand(
    algorithm=hashes.BLAKE2b(64),
    length=len(plaintext),
    info=b"mask"
)

mask = hkdf.derive(bytes(field, 'utf-8'))
print("mask:", mask)


# place mask on the plaintext: whatever.mask(plaintext, mask)
plaintext=list(plaintext)
for c in range(0, len(plaintext)):
    plaintext[c] ^= mask[c]
plaintext=bytes(plaintext)

cipher = Cipher(algorithms.ChaCha20(key=key, nonce=nonce), mode=None, backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()


print("plaintext:", plaintext)
print("ciphertext:", ciphertext)

decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("decrypted pre-xor:", decrypted)

decrypted=list(decrypted)
for c in range(0, len(decrypted)):
    decrypted[c] ^= mask[c]
decrypted=bytes(decrypted)
print("decrypted:", decrypted)

# test of failed decryption

cipher = Cipher(algorithms.ChaCha20(key=key, nonce=bytes(16)), mode=None, backend=default_backend())
decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print(decrypted)
