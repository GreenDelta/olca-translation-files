"""
Provides methods for checking a translated file.
"""

import messages

if __name__ == '__main__':
    messages.check_file('../app-messages/messages_fr.properties',
                        '../app-messages/messages.properties')