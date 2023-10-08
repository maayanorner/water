# input: g-graph, m - manipulator, erm - set of edges in the manipulation, t - type of manipulation
# output: return the LB and UB of the graph after the manipulation, erm
def lb_ub_for_gm_d(g, m, neighbors, erm, t):
    gc = g.copy()
    # compute the graph G(m) according to erm
    gc.add_edges_from(erm)
    # return lb, ub, cut_size
    return cut_value_d(gc, m, neighbors)


def lb_ub_for_gm(g, m, neighbors, erm, t):
    gc = g.copy()
    # compute the graph G(m) according to erm
    gc.add_edges_from(erm)
    # return lb, ub, cut_size
    return cut_value(gc, m, neighbors)


# input: g-graph, m - manipulator,  1 - add 3 - remove
# return: set of all possible subset of edges that m can add, remove or remove and add. according to type of manipulation
def get_set_all_manipulation(g, m, t):
    if t == 1:  # add
        missing_edges = []
    for v in g.nodes():
        if v != m and not g.has_edge(m, v):
            missing_edges.append((m, v))

    all_subsets = []
    for r in range(len(missing_edges) + 1):
        subsets = itertools.combinations(missing_edges, r)
        all_subsets.extend(subsets)

    return all_subsets


# compute manipulation by brute force algorithm
# d : true = directed, false = undirected
def process_manipulations_plus_all_manipulations_d(param, d):
    g = param[0]
    m = param[1]

    print("start for manipulator", m)

    neighbors = list(g.neighbors(m))

    print('neighbors:')
    print(str(len(neighbors)))
    if d:
        mn, mx, _ = cut_value_d(g, m, neighbors)
    else:
        mn, mx, _ = cut_value_d(g, m, neighbors)
    print('d0')
    gc = g.copy()
    print('d1')
    # get all optional manipulation
    manipulation_sets = get_set_all_manipulation(g, m, 1)  # 1 - add,2-add, 3 - remove
    print("have {} cutsets ".format(len(manipulation_sets)))
    if d:
        f = functools.partial(lb_ub_for_gm_d, g, m, neighbors)
    else:
        f = functools.partial(lb_ub_for_gm, g, m, neighbors)
    print("starting multiprocessing with imap ")
    with multiprocessing.Pool() as p:
        ret = p.imap(f, manipulation_sets)

        mna = mn
        mxa = mx
        mnb = mn
        mxb = mx
        mnc = mn
        mxc = mx
        mnd = mn
        mxd = mx
        cnt = 1
        for item in ret:
            if cnt % 10000 == 0:
                print(cnt)
            cnt += 1
            if item == -1:
                continue
            else:
                mn1 = item[0]
                mx1 = item[1]

                mna = max(mna, mn1)
                mxa = max(mxa, mx1)

                if mn1 > mnb and mx1 > mxb:
                    mnb = mn1
                    mxb = mx1

                if mn1 > mnc and mx1 >= mxc:
                    mnc = mn1
                    mxc = mx1

                if mn1 >= mnd and mx1 > mxd:
                    mnd = mn1
                    mxd = mx1

    st = " PLUS MAN: LB {} UB {} OPT-LB {}, OPT-UB {}, OPT-LB-UB {}-{}, OPT W1 {}-{}, OPT W2 {}-{} ".format(mn, mx, mna,
                                                                                                            mxa, mnb,
                                                                                                            mxb, mnc,
                                                                                                            mxc, mnd,
                                                                                                            mxd)
    if mn < mna or mx < mxa:
        with open("output.txt", "a") as f:
            print(st, file=f)
            print('FOUND!')
            return ("Manipulation found for {}".format(m), st)

    print('not found')

    return "no manipulations for manipulator {}".format(m)
