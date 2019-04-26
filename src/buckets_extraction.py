import random


def create_buckets(report_list):
    buckets_dict = {}
    for bug_report in report_list:
        if bug_report.is_duplicate:
            # if it's already in the bucket update the list
            if bug_report.duplicate_id in buckets_dict:
                buckets_dict[bug_report].append(bug_report)
            # else, create a new list with the bug report
            else:
                buckets_dict[bug_report] = [bug_report]

    return buckets_dict


def generate_pair_of_duplicates(buckets):
    pair_of_duplicates = []
    for master in buckets:
        duplicates = buckets[master]
        for duplicate in duplicates:
            pair_of_duplicates.append((master, duplicate))


def generate_pair_of_non_duplicates(buckets):
    count = len(buckets.keys())
    for master in buckets:
        count += len(buckets[master])

    keys = buckets.keys()
    while count is not 0:
        choice = random.choice(keys)
        # TODO create pair of non duplicate reports
        count -= 1




