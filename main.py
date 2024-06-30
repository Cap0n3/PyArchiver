import argparse
from backup_utility import BackupUtility

def main():
    parser = argparse.ArgumentParser(description='PyArchiver - A simple backup CLI utility.')
    parser.add_argument('action', choices=['backup', 'extract'], help='Action to perform: backup or extract.')
    parser.add_argument('source', nargs='*', help='List of source files or directories to backup.')
    parser.add_argument('--destination', required=True, help='Path to the destination directory.')
    parser.add_argument('--archive', action='store_true', help='Create a password-protected archive.')
    parser.add_argument('--passphrase', help='Passphrase for the archive.')
    parser.add_argument('--archive-path', help='Path to the archive file (for extraction).')
    parser.add_argument('--verbose', action='store_true', help='Print detailed information.')

    args = parser.parse_args()

    backup_utility = BackupUtility(destination=args.destination, archive=args.archive, passphrase=args.passphrase)

    if args.action == 'backup':
        if not args.source:
            parser.error('The backup action requires at least one source file or directory.')
        backup_utility.process_list(args.source, verbose=args.verbose)
    elif args.action == 'extract':
        if not args.archive_path:
            parser.error('The extract action requires the --archive-path argument.')
        backup_utility.extract_archive_with_passphrase(args.archive_path, args.destination, verbose=args.verbose)

if __name__ == "__main__":
    main()