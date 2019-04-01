# Gmail functions
from app.lib.google_auth import service_for_user


class GmailService(object):

    def __init__(self, user, user_id='me'):
        self.user = user
        self.service = service_for_user(user)
        self.user_id = user_id

    def get_email_address(self):
        return self.service.users().profile(
                userId=self.user_id).execute()

    def get_message(self, msg_id):
        """Get a Message with given ID.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

        Returns:
        A Message.
        """
        try:
            message = self.service.users().messages().get(
                userId=self.user_id, id=msg_id).execute()
            return message
        except Exception as error:
            print('An error occurred: %s' % error)

    def list_messages(self, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
        """
        try:
            response = self.service.users().messages().list(
                userId=self.user_id, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            # while 'nextPageToken' in response:
            #     page_token = response['nextPageToken']
            #     response = service.users().messages().list(
            #         userId=user_id, q=query, pageToken=page_token).execute()
            #     messages.extend(response['messages'])

            return messages
        except Exception as e:
            print('An error occurred: %s' % e)
