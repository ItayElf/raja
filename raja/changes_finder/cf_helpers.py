import os
from typing import List, Tuple
from subprocess import Popen, PIPE
from raja.changes_finder.changes import Change, Subtract, Replace, Append, Delete


def _parse_int(encoded: bytes, start_i: int) -> Tuple[int, int]:
    """Returns a tuple with two ints, first one is the number that was parsed and the other how many times 'i' was incremented
    :raise ValueError"""
    i = start_i
    num = chr(encoded[i + 1]).encode()
    i += 1
    while i + 1 < len(encoded) and chr(encoded[i + 1]).encode() not in [b"A", b"S", b"R"]:
        num += chr(encoded[i + 1]).encode()
        i += 1
    if not num.decode().isdigit():
        raise ValueError(f"error at i={i}")
    return int(num), i - start_i


def parse_encoded(encoded: bytes) -> List[Change]:
    """Returns list of changes from encoded strings"""
    changes = []
    i = 0
    while i < len(encoded):
        if encoded[i] == ord(b"R"):
            value = chr(encoded[i + 1]).encode()
            prev = chr(encoded[i + 2]).encode()
            i += 2
            num, to_add = _parse_int(encoded, i)
            i += to_add
            changes.append(Replace(value, num, prev))
        elif encoded[i] in [ord(b"A"), ord(b"S")]:
            cls = Append if encoded[i] == ord(b"A") else Subtract
            val = chr(encoded[i + 1]).encode()
            i += 1
            num, to_add = _parse_int(encoded, i)
            i += to_add
            changes.append(cls(val, num))
        elif encoded[i] == ord(b"D"):
            changes.append(Delete())
        i += 1
    return changes


def get_changes_bin(bin_path: str, previous: bytes, current: bytes) -> List[Change]:
    """Returns the changes generated from the given exe"""
    p = Popen([bin_path], stdin=PIPE, stdout=PIPE)
    i1 = str(len(previous)).encode() + b"\n" + previous + b"\n" if previous else b"0\nA\n"
    i2 = str(len(current)).encode() + b"\n" + current + b"\n" if current else b"0\nA\n"
    full_input = i1 + i2
    p.stdin.write(full_input)
    ans = p.communicate(input=full_input)[0].strip()
    if os.name == "nt":
        ans = ans.replace(b"\r\n", b"\n")
    return parse_encoded(b"\n".join(ans.split(b"\n")[1:]))


def get_changes_bin_file(bin_path: str, fname: str, data: bytes) -> Tuple[List[Change], int]:
    """Returns the changes between the file content and the data"""
    p = Popen([bin_path, fname], stdin=PIPE, stdout=PIPE)
    full_input = str(len(data)).encode() + b"\n" + data + b"\n"
    if not data:
        full_input = b"0\nA\n"
    ans = p.communicate(input=full_input)[0].strip()
    splt = ans.split(b"\n")
    return parse_encoded(b"\n".join(splt[1:])), int(splt[0])


def get_changes_bin2(bin_path: str, previous_fname: str, current_fname: str) -> Tuple[List[Change], int]:
    """Returns the changes generated from the given exe using cli args
    :raise FileNotFoundError"""
    p = Popen([bin_path, previous_fname, current_fname], stdin=PIPE, stdout=PIPE)
    ans = b""
    while True:
        line = p.stdout.readline()
        if not line:
            break
        ans += line
    if os.name == "nt":
        ans = ans.replace(b"\r\n", b"\n")
    if ans.endswith(b"\n"):
        ans = ans[:-1]
    if b"Couldn't open file" in ans:
        raise FileNotFoundError(f"{previous_fname} or {current_fname}")
    splt = ans.split(b"\n")
    return parse_encoded(b"\n".join(splt[1:])), int(splt[0])


def combine_encodeds(encodeds: List[bytes]) -> List[Change]:
    """Returns list of changes from many encoded changes byte strings"""
    combined = b"".join(encodeds)
    return parse_encoded(combined)
