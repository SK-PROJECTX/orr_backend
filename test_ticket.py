from admin_portal.models import Ticket
from django.db import connection

def run():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, ticket_id FROM admin_portal_ticket WHERE ticket_id = ''")
        rows = cursor.fetchall()
        print("ROWS WITH EMPTY TICKET_ID:", rows)

if __name__ == '__main__':
    run()
