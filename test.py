#!/usr/bin/env python3
def test() -> bool:
    c1 = 0b1001

    return bool(c1 & 0b0001)

print(test())
