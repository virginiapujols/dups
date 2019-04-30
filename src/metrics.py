
def mean_reciprocal_rank(rank_list, n_total):
    sum_reciprocal_ranks = 0
    for rank in rank_list:
        sum_reciprocal_ranks += 1 / rank

    mean_rank = sum_reciprocal_ranks / n_total
    return mean_rank


def recall_rate(n_detected, n_total):
    return n_detected / n_total
