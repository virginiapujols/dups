import random


def generate_pair_of_duplicates(buckets):
    """
    To create positive examples, for each bucket, we perform
    the following:
        1. Create the pair (master, duplicate), where duplicate is
        one of the duplicates in the bucket and master is the
        original report in the bucket. [We implement this approach]
        2. Create the pairs (duplicate1,duplicate2) where the two
        duplicates belong to the same bucket. [TODO: alternative approach]
    Paper: A Discriminative Model Approach for Accurate Duplicate Bug Report Retrieval
    :param buckets: dictionary of masters (key) with its duplicate bug reports (value).
    :return: Tuples of duplicates (dup1, dup2)
    """
    pair_of_duplicates = []
    for master in buckets:
        duplicates = buckets[master]
        for duplicate in duplicates:
            pair_of_duplicates.append((master, duplicate))

    return pair_of_duplicates


def generate_pair_of_non_duplicates(buckets):
    """
    To create negative examples, one could pair one report
    from one bucket with another report from the other bucket.
    Paper: A Discriminative Model Approach for Accurate Duplicate Bug Report Retrieval

    :param buckets: dictionary of masters (key) with its duplicate bug reports (value).
    :return: Tuples of non-duplicates (dup1 of a bucket, dup2 of a different bucket)

    The variable 'pair_of_non_duplicates' allows for repeated values.

    the 'count' variable limits the amount of members in the pair_of_non_duplicates
    list that in this case will be the total number of duplicates in
    all buckets.

    """
    count = len(buckets.keys())
    for master in buckets:
        count += len(buckets[master])

    pair_of_non_duplicates = []
    keys = buckets.keys()
    while count is not 0:
        random_keys = random.sample(keys, 2)
        bucket_list1 = buckets[random_keys[0]]
        bucket_list2 = buckets[random_keys[1]]

        dup_pair1 = random.choice(bucket_list1)
        dup_pair2 = random.choice(bucket_list2)

        non_dup_pair1 = (dup_pair1[0], dup_pair2[0])
        non_dup_pair2 = (dup_pair1[1], dup_pair2[1])

        pair_of_non_duplicates.append(non_dup_pair1)
        pair_of_non_duplicates.append(non_dup_pair2)
        count -= 1

    return pair_of_non_duplicates


