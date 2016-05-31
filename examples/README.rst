Chat
----

AnswerBot.py
    Simple chat bot that responds to basic queries (no AI) and can transfer
    guests to a human upon request.

check-service.py
    Look to see if your services are online and, if not, why not.  Also
    reports if you have too few operators staffing.

csv-transcripts.py
    Flatten and escape transcripts suitable for inclusion in a csv file
    and import into excel.

current-activity.py
    Count the number of active chats and the number of librarians that
    are staffing services.

daily-transcripts.py
    Each morning, forward all of yesterday's chats to the inbox.

kill-switch.py
    Somebody forgot to log out.  Take the queue offline so patrons don't
    mistakenly think you're available.

one-shot.py
    Send a guest-initiated a call-out to a queue or user. When someone answers
    the call-out, the guest is notified and the response is shown to the guest.

rolling-transcript-deletion.py
    Each morning, delete the transcripts from a month ago.

scheduled-reports.py
    Automatically summarize last week's activity.

scheduled-service-hours.py
    Opt users into and out of queues on a schedule.  Opting a user out
    of a queue will not interrupt chats in progress.

Email
-----

biff.py
    Poll 3mail for new messages and send notifications to the terminal.

FAQ
---

edit-question.py
    Edit your FAQ in the console.  Because consoles rock.

edit-template.py
    Edit your FAQ templates in the console.  Because consoles rock.

export-faq.py
    Bulk export of all questions and answers in a LibraryH3lp FAQ.
    Produces a CSV file with columns corresponding to question, answer, 
    list of topic tags, views, likes, and dislikes.

import-faq.py
    Bulk import a list of questions and answers into a LibraryH3lp FAQ.
    Expects a CSV file with columns corresponding to question, answer,
    expiration date (may be empty), and a list of topic tags.

faq-usage.py
    Download a record of FAQ views and searches.

search-and-replace.py
    Perform a search and replace operation across all your FAQs.

General
-------

in-out-board.py
    Who's around?

new-user-alert.py
    Get notified of new users.

new-user-setup.py
    Create a new user, automatically adding it to queues, conference
    rooms, canned message pools, and setting up buddy relationships.

SMS
---

sms-alerts.py
    LibraryH3lp SMS integrates with Twilio.  You can either send staff
    alerts by SMS, or you can send notices to patrons.  Patron replies
    will automatically be routed in chat or 3mail.
