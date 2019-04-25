import xml.etree.ElementTree as ET


def find_duplicate_reports_to_xml(dataset_xml_path):
    tree = ET.parse(dataset_xml_path)
    root = tree.getroot()
    master_reports = set()
    dup_bugs = ET.Element('bugs')
    non_dup_bugs = ET.Element('bugs')

    count_duplicates = 0
    count_non_duplicates = 0
    for bug_element in root.findall('bug'):
        if bug_element.find('dup_id') is None:
            print('saving non-duplicate')
            count_non_duplicates += 1
            non_dup_bugs.append(bug_element)
        else:
            print('saving duplicate')
            count_duplicates += 1
            dup = bug_element.find('dup_id').text
            master_reports.add(dup)
            dup_bugs.append(bug_element)

    tree_dups = ET.ElementTree(element=dup_bugs)
    tree_dups.write(open("data/duplicate_reports.xml", 'wb'))

    tree_non_dups = ET.ElementTree(element=non_dup_bugs)
    tree_non_dups.write(open("data/non_duplicate_reports.xml", 'wb'))

    print('Duplicates: ', count_duplicates)
    print('Non-Duplicates: ', count_non_duplicates)
    return master_reports


def filter_master_of_duplicates(master_ids):
    dataset_xml_path = "/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/non_duplicate_reports.xml"

    tree = ET.parse(dataset_xml_path)
    root = tree.getroot()
    non_dup_bugs = ET.Element('bugs')

    count_non_duplicates = 0
    for bug_element in root.findall('bug'):
        bug_id = bug_element.find('bug_id').text
        if bug_id in master_ids:
            count_non_duplicates += 1
            non_dup_bugs.append(bug_element)

    tree_non_dups = ET.ElementTree(element=non_dup_bugs)
    tree_non_dups.write(open("data/non_duplicate_reports.xml", 'wb'))
    print('Filtered Non-Duplicates: ', count_non_duplicates)


def merge_dup_with_non_dup():
    path_dup = '/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/duplicate_reports.xml'
    path_non_dup = '/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/non_duplicate_reports.xml'
    xml_elements = ET.Element('bugs')

    tree_dup = ET.parse(path_dup)
    for bug_element in tree_dup.getroot().findall('bug'):
        xml_elements.append(bug_element)

    tree_non_dup = ET.parse(path_non_dup)
    for bug_element in tree_non_dup.getroot().findall('bug'):
        xml_elements.append(bug_element)

    merged_tree = ET.ElementTree(element=xml_elements)
    merged_tree.write(open("data/filtered_mozilla_report_2018.xml", 'wb'))


# path = "/Users/virginiapujols/Documents/RIT/SEMESTER 4/Data science/FinalProject/bugs_dedupl_data_science/src/data/mozilla_reports_2018.xml"
# master_dup_ids = find_duplicate_reports_to_xml(path)
#
# filter_master_of_duplicates(master_dup_ids)
merge_dup_with_non_dup()

