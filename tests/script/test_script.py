import pytest, inspect
from pytest import raises, fixture, fail

from bitforge.script import Script, Instruction
from bitforge.script.opcode import *
import bitforge.script.opcode as opcode_module
from bitforge.encoding import *
from bitforge.tools import Buffer
from bitforge import Address


class TestScript:
    def test_create_emtpy(self):
        s = Script()
        assert s.instructions == tuple()

    def test_binary_single(self):
        s = Script.from_bytes(b'\0')
        assert s.instructions == (Instruction(OP_0),)

    def test_binary_const_pushes(self):
        for length in range(1, 76):
            opcode = Opcode(length)
            string = b'a' * length

            op_bytes = bytes(bytearray([length]))
            s = Script.from_bytes(op_bytes + string)

            assert s.instructions == (Instruction(opcode, string),)

    def test_binary_var_pushes(self):
        s1 = Script.from_bytes(OP_PUSHDATA1.bytes + b'\3' + b'abc')
        assert s1.instructions == (Instruction(OP_PUSHDATA1, b'abc'),)

        s2 = Script.from_bytes(OP_PUSHDATA2.bytes + b'\3\0' + b'abc')
        assert s2.instructions == (Instruction(OP_PUSHDATA2, b'abc'),)

        s2 = Script.from_bytes(OP_PUSHDATA4.bytes + b'\3\0\0\0' + b'abc')
        assert s2.instructions == (Instruction(OP_PUSHDATA4, b'abc'),)

        with raises(Buffer.InsufficientData):
            Script.from_bytes(OP_PUSHDATA1.bytes + b'\3' + b'a')

        with raises(Buffer.InsufficientData):
            Script.from_bytes(OP_PUSHDATA2.bytes + b'\3\0' + b'a')

        with raises(Buffer.InsufficientData):
            Script.from_bytes(OP_PUSHDATA4.bytes + b'\3\0\0\0' + b'a')

    def test_binary_all_nonpush_opcodes(self):
        opcodes = []
        for name, value in inspect.getmembers(opcode_module):
            if isinstance(value, Opcode) and not value.is_push():
                opcodes.append(value)

        bytes = b''.join(opcode.bytes for opcode in opcodes)

        s = Script.from_bytes(bytes)
        assert s.instructions == tuple(map(Instruction, opcodes))

    def test_from_string(self):

        def test_script_string(string, instructions):
            script = Script.from_string(string)
            assert script.to_string() == string
            assert len(script.instructions) == instructions

        test_script_string('OP_0 OP_PUSHDATA4 3 0x010203 OP_0', 3)
        test_script_string('OP_0 OP_PUSHDATA2 3 0x010203 OP_0', 3)
        test_script_string('OP_0 OP_PUSHDATA1 3 0x010203 OP_0', 3)
        test_script_string('OP_0 3 0x010203 OP_0', 3)

        with raises(Script.UnknownOpcodeName):
            Script.from_string('OP_99')

        with raises(Script.MissingPushArguments):
            Script.from_string('OP_PUSHDATA1')

        with raises(Script.MissingPushArguments):
            Script.from_string('OP_PUSHDATA1 3')

        with raises(Script.InvalidPushDataLength):
            Script.from_string('OP_PUSHDATA1 3 0x01020302')

        with raises(Script.InvalidPushData):
            Script.from_string('OP_PUSHDATA1 3 010203')

        with raises(Script.InvalidPushData):
            Script.from_string('3 010203')

    def test_is_push_only(self):
        script = Script.from_string('OP_1 OP_16')
        assert script.is_push_only() is True

        script = Script.from_string('OP_PUSHDATA1 1 0x01')
        assert script.is_push_only() is True

        script = Script.from_string('OP_1 OP_RETURN')
        assert script.is_push_only() is False

    def test_is_pay_to_pubkey_in(self):
        yes = [
            Script.pay_to_pubkey_in(Address('a' * 20), 'foo'),
            Script.pay_to_pubkey_in(Address('x' * 20), 'bar')
        ]

        no = [
            Script(),
            Script.pay_to_pubkey_out(Address('a' * 20))
        ]

        assert all(map(Script.is_pay_to_pubkey_in, yes))
        assert not any(map(Script.is_pay_to_pubkey_in, no))

    def test_is_pay_to_pubkey_out(self):
        yes = [
            Script.pay_to_pubkey_out(Address('a' * 20)),
            Script.pay_to_pubkey_out(Address('x' * 20))
        ]

        no = [
            Script(),
            Script.pay_to_pubkey_in(Address('a' * 20), 'foo')
        ]

        assert all(map(Script.is_pay_to_pubkey_out, yes))
        assert not any(map(Script.is_pay_to_pubkey_out, no))

    def test_is_pay_to_script_out(self):
        embedded = Script.pay_to_pubkey_out(Address('x' * 20))

        yes = [ Script.pay_to_script_out(embedded) ]

        no = [
            Script(),
            Script.pay_to_pubkey_out(Address('a' * 20)),
            Script.pay_to_script_in(embedded, [ 'foo' ])
        ]

        assert all(map(Script.is_pay_to_script_out, yes))
        assert not any(map(Script.is_pay_to_script_out, no))

    def test_is_pay_to_script_in(self):
        embedded = Script.pay_to_pubkey_out(Address('x' * 20))

        yes = [
            Script.pay_to_script_in(embedded, [ 'foo' ]),
            Script.pay_to_script_in(Script.compile([ 'bar' ]), [ 'foo' ]),
            Script.pay_to_script_in(Script.compile([ 'baz' ]), [ 'one', 'two' ]),
        ]

        no = [
            Script(),
            # Script.pay_to_pubkey_in(Address('a' * 20), 'foo'),
            # Script.pay_to_script_out(Script())
        ]

        assert all(map(Script.is_pay_to_script_in, yes))
        assert not any(map(Script.is_pay_to_script_in, no))
