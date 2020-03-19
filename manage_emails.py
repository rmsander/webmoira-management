"""Command-line functionality for adding and deleting members from mailing lists through MIT's Web Moira system.  This
script is more suitable for adding or deleting many members at once (more efficient than using the Web Moira tool), but
for adding or deleting only a few more members at a time, the Web Moira tool might be a little more efficient."""

import os
import argparse


def delete_all_members(kerberos, mailing_list):
    """
    Call this function using the command-line option 'd' to delete all members from a chosen mailing list.
    
    Arguments:
        1. kerberos (str): Kerberos corresponding to the person with admin access to the web moira list you're editing 
                           (in most cases, this should be yours.  Do NOT include '@mit.edu'.
        2. mailing_list (str): Web moira corresponding to the mailing list you want to delete all members from; again, 
                               without '@mit.edu'.
    """
    # Call bash script to delete all members from list
    os.system("ssh {}@athena.dialup.mit.edu './delete_all_members.sh {}'".format(kerberos, mailing_list))
    print("Deleted all members from the mailing list {}".format(mailing_list))


def add_members_to_list(kerberos, mailing_list, path_to_mailing_list_file):
    """
    Call this function using the command-line option 'd' to delete all members from a chosen mailing list.

    Arguments:
        1. kerberos (str): Kerberos corresponding to the person with admin access to the web moira list you're editing 
                           (in most cases, this should be yours.  Do NOT include '@mit.edu'.
        2. mailing_list (str): Web moira corresponding to the mailing list you want to add members to; again, 
                               without '@mit.edu'.
        3. path_to_mailing_list (str): Path (on your local machine) to the file of Kerberos you want to add as members
                                       of your mailing list.
        """
    # First, transfer the file
    file_name = path_to_mailing_list_file.split("/")[-1]  # Get file name
    os.system("scp {} {}@athena.dialup.mit.edu:~/".format(path_to_mailing_list_file, kerberos))
    print("Transferred email file to Athena server...")

    # Now read the names from the file and transfer
    os.system("ssh {}@athena.dialup.mit.edu './add_members_to_list.sh {} {}'".format(kerberos, mailing_list, file_name))
    print("Added members from {} to mailing list {}".format(file_name, mailing_list))


def parse_args():
    """Standard command-line argument parser."""
    # Create command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("kerberos", help="Your MIT Kerberos", type=str)
    parser.add_argument("mailing_list", help="A TBP moira mailing list you have admin privileges for", type=str)
    parser.add_argument("-a", "--add", help="Option for adding members", required=False, action="store_true")
    parser.add_argument("-d", "--delete", help="Option for deleting members", required=False, action="store_true")
    parser.add_argument("-f", "--file", help="File for the kerberoses that you add to the list", required=False,
                        type=str)
    parser.add_argument("-t", "--transfer", help="Option if you need to transfer bash files over", action="store_true")

    # Parse arguments
    results = vars(parser.parse_args())
    print("Your email management selections: \n {}".format(results))
    k = results["kerberos"]
    m = results["mailing_list"]
    a = results["add"]
    d = results["delete"]
    f = results["file"]
    t = results["transfer"]

    return k, m, a, d, f, t


def main():
    # Parse args
    k, m, a, d, f, t = parse_args()

    # Check that we're not doing too many things at once
    assert (a + d < 2)

    # If we need to transfer files over, do so
    if t:
        os.system("scp delete_all_members.sh {}@athena.dialup.mit.edu:~/".format(k))
        os.system("scp add_members_to_list.sh {}@athena.dialup.mit.edu:~/".format(k))
        os.system("ssh {}@athena.dialup.mit.edu chmod +x delete_all_members.sh add_members_to_list.sh".format(k))

    if a:  # Add members to list
        add_members_to_list(k, m, f)
    elif d:  # Delete members from list
        delete_all_members(k, m)


if __name__ == "__main__":
    main()
