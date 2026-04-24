import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.models import FAQ

faqs = FAQ.objects.all()
for faq in faqs:
    q_en = str(faq.question).upper()
    
    if "WHAT DOES IT MEAN" in q_en or "BUSINESS GP" in q_en:
        faq.question_it = {"format": "html", "content": "Cosa significa che ORR è un Medico di Medicina Generale (GP) aziendale?"}
        faq.answer_it = {"format": "html", "content": "Lavoriamo come un medico di base per la vostra organizzazione. Iniziamo ascoltando, comprendiamo il vostro contesto e i vostri vincoli, quindi introduciamo il giusto mix di competenze in ambito di consulenza, sistemi, IA e natura per trattare le cause profonde — sempre ancorati a ciò che conta di più per voi e per i vostri clienti."}
    elif "FIRST MEETING" in q_en:
        faq.question_it = {"format": "html", "content": "Cosa succede nel primo incontro?"}
        faq.answer_it = {"format": "html", "content": "Nel nostro primo incontro, ci concentriamo sulla comprensione della vostra situazione attuale, delle sfide e degli obiettivi. Discuteremo il vostro contesto aziendale, identificheremo i principali punti critici ed esploreremo come appare il successo per voi. Questo ci aiuta a creare un rapporto ORR su misura con raccomandazioni attuabili."}
    elif "ORR REPORT" in q_en:
        faq.question_it = {"format": "html", "content": "Cos'è il rapporto ORR?"}
        faq.answer_it = {"format": "html", "content": "Il rapporto ORR è un'analisi completa che forniamo dopo il nostro primo incontro. Delinea i problemi chiave che interessano il vostro business, propone soluzioni rapide e miglioramenti a lungo termine, e mostra dove il nostro lavoro di consulenza, sui sistemi digitali o sui sistemi viventi avrà il maggior impatto sulla vostra organizzazione."}
    elif "COST" in q_en or "HOW MUCH" in q_en:
        faq.question_it = {"format": "html", "content": "Quanto costano gli incontri e il rapporto?"}
        faq.answer_it = {"format": "html", "content": "I nostri incontri sono fatturati a €45/ora su base pro-rata, progettati per essere brevi, mirati e densi di valore. Il costo del rapporto ORR parte da €220, sebbene il costo finale dipenda dalla complessità della vostra situazione e dei vostri requisiti."}
    elif "KEEP WORKING" in q_en or "AFTER THE REPORT" in q_en:
        faq.question_it = {"format": "html", "content": "Devo continuare a lavorare con ORR dopo il rapporto?"}
        faq.answer_it = {"format": "html", "content": "Niente affatto. Il rapporto ORR è progettato per fornire valore sia che continuiate a lavorare con noi o meno. Include raccomandazioni attuabili che potete implementare in autonomia. Tuttavia, siamo disponibili a supportare l'implementazione se sceglierete di continuare la nostra collaborazione."}
    faq.save()
print("Successfully synced FAQs for Production DB!")
