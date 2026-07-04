def is_graphical_manual(sequence):
    if sum(sequence) % 2 != 0:
        return False, "Sum of degrees is odd (Handshaking Lemma violation)."

    s = sorted(sequence, reverse=True)
    
    while True:
        s = [d for d in s if d > 0]
        
        if not s:
            return True, "The sequence is graphical."

        d = s.pop(0)

        if d > len(s):
            return False, f"Not enough nodes to attach degree {d}."

        for i in range(d):
            s[i] -= 1
            if s[i] < 0:
                return False, "Subtraction resulted in a negative degree."

        s.sort(reverse=True)

seq = [5, 4, 4, 2, 2, 1, 1]
is_graphical, message = is_graphical_manual(seq)

print(f"Sequence: {seq}")
print(f"Result: {is_graphical}")
print(f"Reason: {message}")