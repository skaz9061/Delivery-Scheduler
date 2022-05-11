# Module for handling package issues.
from datetime import time


def check_issues(truck_time, delayed, priority_dict, package_hash):
    """
    Checks the status of all issues of delayed packages and addresses them.

    :param datetime.time truck_time: the time to check the status
    :param list[str] delayed: list of package ids that are delayed
    :param dict[datetime.time -> list[str]] priority_dict: package lists associated with each deadline
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    # Time complexity O(n^2)

    if truck_time >= time(10, 20):
        fix_address(9, '410 S State St', package_hash)

    add_delayed(truck_time, delayed, package_hash, priority_dict)  # O(n^2)


def fix_address(pkg_id, new_address, package_hash):
    """
    Replaces the current address of a package with a new address.

    :param str pkg_id: id of the package
    :param str new_address: the new address of the package
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    # Time complexity O(n)
    pkg = package_hash.lookup(str(pkg_id))  # O(n)
    pkg.address = new_address


def add_delayed(curr_time, delayed_pkgs, package_hash, priority_dict):
    """
    If any packages have reached their delayed time, they are added to the appropriate package list.

    :param datetime.time curr_time: the time to check packages
    :param list[str] delayed_pkgs: list of delayed package ids
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :param dict[datetime.time -> list[str]] priority_dict: package lists associated with each deadline
    :return:
    """
    # Time complexity O(n^2)

    altered_pkgs = list()

    for pkg_id in delayed_pkgs:  # O(n^2)
        pkg = package_hash.lookup(pkg_id)  # O(n)

        if pkg.delay_time <= curr_time:
            pkg.advance_status(pkg.delay_time)
            priority_dict[pkg.deadline].append(pkg.id)
            altered_pkgs.append(pkg_id)

    for pkg_id in altered_pkgs:  # O(n^2)
        delayed_pkgs.remove(pkg_id)  # O(n)
