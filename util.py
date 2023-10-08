
def evaluate_welfare(gd, T):
    val = 0
    for (b,bid,s,sid) in T:
        val += gd.f_b(b,bid) - gd.f_s(s, sid)

    return val



