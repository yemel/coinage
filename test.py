from bitforge import Script, Address

s1 = Script.pay_to_pubkey_out(Address('a' * 20))
s2 = Script.pay_to_pubkey_in(Address('a' * 20), 'x' * 650)

print Script.is_pay_to_pubkey_out(s1)
print not Script.is_pay_to_pubkey_out(s2)

print not Script.is_pay_to_pubkey_in(s1)
print Script.is_pay_to_pubkey_in(s2)


# from bitforge.encoding import *
# from bitforge import Input, Script, Output, Transaction
# from bitforge.script.opcode import *
#
# # print repr(encode_int(0xaeae))
# # print repr(encode_int(0xaeae, length=5))
# # print repr(encode_int(0xaeae, length=5, big_endian=False))
#
#
# # for n in [2, 2 ** 10, 2 ** 20, 2**40]:
# #     print encode_hex(encode_int(n)), encode_hex(encode_varint(n))
#
# iscript = Script.compile([
#     '304502206e21798a42fae0e854281abd38bacd1aeed3ee3738d9e1446618c4571d10',
#     '90db022100e2ac980643b0b82c0e88ffdfec6b64e3e6ba35e7ba5fdd7d5d6cc8d25c6b241501'
# ])
#
# oscript = Script.compile([
#     OP_DUP,
#     OP_HASH160,
#     '404371705fa9bd789a2fcd52d2c580b65d35549d',
#     OP_EQUALVERIFY,
#     OP_CHECKSIG
# ])
#
# i = Input(
#     tx_id     = 'f5d8ee39a430901c91a5917b9f2dc19d6d1a0e9cea205b009ca73dd04470b9a6',
#     txo_index = 1,
#     script    = iscript
# )
#
# o = Output(
#     amount = 100,
#     script = oscript
# )
#
# t = Transaction(
#     inputs  = [i],
#     outputs = [o]
# )
#
#
# def test_input():
#     actual   = encode_hex(i.to_bytes())
#     expected = 'a6b97044d03da79c005b20ea9c0e1a6d9dc12d9f7b91a5911c9030a439eed8f501000000934433303435303232303665323137393861343266616530653835343238316162643338626163643161656564336565333733386439653134343636313863343537316431304c4c39306462303232313030653261633938303634336230623832633065383866666466656336623634653365366261333565376261356664643764356436636338643235633662323431353031ffffffff'
#
#     assert actual == expected
#
#
# def test_output():
#     actual   = encode_hex(o.to_bytes())
#     expected = '64000000000000002d76a9283430343337313730356661396264373839613266636435326432633538306236356433353534396488ac'
#
#     assert actual == expected
#
#
# def test_transaction():
#     actual   = encode_hex(t.to_bytes())
#     expected = '0100000001a6b97044d03da79c005b20ea9c0e1a6d9dc12d9f7b91a5911c9030a439eed8f501000000934433303435303232303665323137393861343266616530653835343238316162643338626163643161656564336565333733386439653134343636313863343537316431304c4c39306462303232313030653261633938303634336230623832633065383866666466656336623634653365366261333565376261356664643764356436636338643235633662323431353031ffffffff0164000000000000002d76a9283430343337313730356661396264373839613266636435326432633538306236356433353534396488ac00000000'
#
#     assert actual == expected
#
# test_input()
# test_output()
# test_transaction()
