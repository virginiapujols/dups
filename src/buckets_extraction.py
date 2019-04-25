

def create_buckets(report_list):
    buckets_dict = {}
    for bug_report in report_list:
        if bug_report.is_duplicate:
            # if it's already in the bucket update the list
            if bug_report.duplicate_id in buckets_dict:
                buckets_dict[bug_report.duplicate_id].append(bug_report)
            # else, create a new list with the bug report
            else:
                buckets_dict[bug_report.duplicate_id] = [bug_report]

    return buckets_dict

