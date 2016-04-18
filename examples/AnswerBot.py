#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
import sys
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

import logging
import getpass
from optparse import OptionParser


"""
    Adapted from echo bot example in SleekXMPP.
    http://sleekxmpp.com/getting_started/echobot.html
"""

import requests
import sleekxmpp

class AnswerBot(sleekxmpp.ClientXMPP):

    """
    A simple LibraryH3lp bot that will respond to basic commands with
    predetermined responses. No fancy AI.

    To keep track of conversations, you should create a LibraryH3lp queue
    and assign *only* the bot as an operator on the queue.  Then the bot will
    answer all incoming chats from patrons on that queue.  When a patron
    requests a transfer to a human, the bot can transfer them to a different
    queue staffed by humans.
    """

    commands = {
        'hours': ('8am - 5pm weekdays. 9am - 5pm Saturday. Closed Sunday.', 'Library operating hours'),
        'directions': ('At the corner of Main St. and Martin Luther King Blvd.', 'Library location')
    }

    # Keep track of ongoing conversations with guests.
    # Key is a bare guest JID. Value is a list containing conversation ID
    # and an authorization token for transfers.
    conversations = {}

    def __init__(self, username, domain, password, log, queue = None):
        sleekxmpp.ClientXMPP.__init__(self, '{}@{}'.format(username, domain), password)

        self.domain         = domain
        self.transfer_queue = queue
        self.log            = log

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler('session_start', self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler('chatstate_active', self.guest_message)
        self.add_event_handler('message', self.message)
        self.add_event_handler('roster_update', self.roster_update)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

    def roster_update(self, iq):
        """
        Keep track of which guests we've chatted with.
        """
        for guest_jid, item in iq['roster']['items'].items():
            if item['subscription'] == 'both':
                self.log.debug('roster update: {}'.format(guest_jid))
                self['xep_0054'].get_vcard(guest_jid.bare, block = False, callback = self.handle_vcard)

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the message's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        self.log.debug("message: {}".format(msg["body"]))

        if msg['type'] in ('chat', 'normal'):
            if 'this is a transfer' in msg['body']:
                self.introduce_myself(msg['from'])

    def guest_message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        self.log.debug('guest message: {}'.format(msg['body']))

        if msg['type'] in ('chat', 'normal') and msg['body']:
            reply = self.process_command(msg)
            if reply:
                msg.reply(reply).send()

    def handle_vcard(self, iq):
        """
        VCards for guests include a chat management URL which contains a
        conversation ID and token.  The conversation ID and token can later be
        used for transfers.
        """
        vcard = iq['vcard_temp']
        chat_management = getattr(vcard.xml.find('{vcard-temp}X-CHAT-MANAGEMENT'), 'text', None)
        if not chat_management:
            return; # Not a guest

        self.log.debug('Received guest vcard: {}'.format(vcard))

        guest_jid = iq['from']
        chat_id = chat_management.split('/')[-1].split('?')[0]
        token = chat_management.split('?t=')[-1]
        self.conversations[guest_jid] = (chat_id, token)

        self.log.debug('Adding conversation for {}: {}, {}'.format(guest_jid, chat_id, token))

    def introduce_myself(self, guest_jid):
        """
        Self-identify and let guests know what commands the bot knows.
        """
        commands = self.get_valid_commands()
        intro = 'Hi! I am a library bot and respond to the following commands:<br/>{}'.format(commands)
        self.send_message(mto = guest_jid, mbody = intro)

    def get_valid_commands(self):
        """
        Lets vistors know the commands a bot understands. If we allow
        for the possibility of transfer to a librarian, we need to make
        sure someone is around before getting a guest's hopes up.
        """
        valid_commands = '<br/>'

        for (command, (response, help_text)) in self.commands.iteritems():
            valid_commands += '{} - {}<br/>'.format(command, help_text)

        if self.transfer_queue:
            result = requests.get('https://{}/presence/jid/{}/chat.{}/text'.format(self.domain, self.transfer_queue, self.domain))
            status = result.text
            if status == 'chat' or status == 'available':
                valid_commands += 'librarian - Chat with a real librarian instead'

        return valid_commands

    def process_command(self, msg):
        """
        Tries to figure out what a guests wants and delivers an
        answer or action the request to the best of the bot's ability.
        """
        user_request = msg['body'].lower()

        for (command, (response, _)) in self.commands.iteritems():
            if command in user_request:
                return response

        if 'librarian' in user_request:
            if self.transfer(msg['from']):
                return None
            else:
                return 'Sorry, no librarians are available for chat.'

        return 'Sorry, I do not understand your request. Try one of these keywords: {}'.format(self.get_valid_commands())

    def transfer(self, guest_jid):
        """
        Attempts to transfer a guest to a librarian. The target of the
        transfer is a queue (presumably) staffed by librarians.
        """
        success = False

        if self.conversations.has_key(guest_jid.bare):
            conversation_id, token = self.conversations[guest_jid.bare]
            url = 'https://{}/2013-07-21/chats/{}/transfer'.format(self.domain, conversation_id)
            target = '{}@chat.{}'.format(self.transfer_queue, self.domain)

            self.log.debug('Transferring Guest to {}: {}'.format(target, url))
            result = requests.get(url, params = {'target': target, 't': token})
            success = result.status_code == 200

        return success

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-b', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # bot options.
    optp.add_option('-u', '--username', dest='username',
                    help='username for your bot')
    optp.add_option('-p', '--password', dest='password',
                    help='password for your bot')
    optp.add_option('-t', '--transfer', dest='queue',
                    help='queue name to use for transfers to humans')
    optp.add_option('-d', '--domain', dest='domain',
                    help='chat domain')

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')
    log = logging.getLogger(__name__)

    if opts.username is None:
        opts.username = raw_input('Bot Username: ')
    if opts.password is None:
        opts.password = getpass.getpass('Bot Password: ')
    if opts.queue is None:
        opts.queue = raw_input('Transfer Queue: ')

    opts.domain = opts.domain or 'libraryh3lp.com'

    # Setup the bot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = AnswerBot(opts.username, opts.domain, opts.password, log, opts.queue)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0054') # VCard Temp
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0085') # Chat state notifications
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print('Done')
    else:
        print('Unable to connect.')
