import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production' if '--prod' in sys.argv else 'core.settings.local')
django.setup()

from admin_portal.models_cms import StrategicAdvisoryPageContent

def fix_network_cards():
    print("Fixing Network Cards schema...")
    st = StrategicAdvisoryPageContent.objects.first()
    if not st:
        print("Error: StrategicAdvisoryPageContent not found.")
        return

    st.network_cards_en = [
        {
            "title": "Legal & Regulatory Experts",
            "description": "Specialized attorneys and compliance professionals across multiple jurisdictions",
            "icon": "M12 3c-1.1 0-2 .9-2 2v2H7c-1.1 0-2 .9-2 2v2h14v-2c0-1.1-.9-2-2-2h-3V5c0-1.1-.9-2-2-2zm0 2h-1v2h2V5h-1zm9 6H3v2h18v-2zm-9 3c-2.8 0-5 2.2-5 5v3h10v-3c0-2.8-2.2-5-5-5z",
            "ctaText": "Apply as Legal Expert"
        },
        {
            "title": "Scientific Advisors",
            "description": "PhDs and researchers in biotechnology, environmental and computer science, and related fields",
            "icon": "M10 2v2h4V2h-4z M12 5c-3.9 0-7 3.1-7 7v7H3v2h18v-2h-2v-7c0-3.9-3.1-7-7-7z M12 18c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z",
            "ctaText": "Join as Scientific Advisor"
        },
        {
            "title": "Industry Specialists",
            "description": "Sector-specific consultants with deep regulatory knowledge",
            "icon": "M22 10v12H2V10l7-5 4 3 6-5 3 3zM12 17v5h4v-5h-4z M4 12v2h2v-2H4z M4 16v2h2v-2H4z",
            "ctaText": "Become an Industry Specialist"
        },
        {
            "title": "Technical Auditors",
            "description": "Certification professionals for ISO, GMP, and other standards",
            "icon": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-2h2v2zm0-4H7v-2h2v2zm0-4H7V7h2v2zm8 8h-6v-2h6v2zm0-4h-6v-2h6v2zm0-4h-6V7h6v2z",
            "ctaText": "Collaborate as an Auditor"
        },
        {
            "title": "ESG Consultants",
            "description": "Sustainability experts and carbon accounting specialists",
            "icon": "M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22L6.66 19.7C7.14 19.87 7.64 20 8 20C19 20 22 3 22 3C21 5 14 5.25 9 6.25C4 7.25 2 11.5 2 13.5C2 15.5 3.75 17.25 3.75 17.25C7.5 13.5 12.5 13.5 15.5 13.5C15.5 13.5 16 13.75 16 14.25C16 14.75 15.5 15 15.5 15C12.5 15 7.5 15 3.75 18.75C3.75 18.75 5.25 20.5 8 20.5C11.5 20.5 17 16 17 8Z",
            "ctaText": "Partner as ESG Consultant"
        }
    ]

    st.network_cards_it = [
        {
            "title": "Esperti Legali e Normativi",
            "description": "Avvocati specializzati e professionisti della conformità",
            "icon": "M12 3c-1.1 0-2 .9-2 2v2H7c-1.1 0-2 .9-2 2v2h14v-2c0-1.1-.9-2-2-2h-3V5c0-1.1-.9-2-2-2zm0 2h-1v2h2V5h-1zm9 6H3v2h18v-2zm-9 3c-2.8 0-5 2.2-5 5v3h10v-3c0-2.8-2.2-5-5-5z",
            "ctaText": "Candidati come Esperto Legale"
        },
        {
            "title": "Consulenti Scientifici",
            "description": "Ricercatori in biotecnologie, scienze ambientali e informatiche",
            "icon": "M10 2v2h4V2h-4z M12 5c-3.9 0-7 3.1-7 7v7H3v2h18v-2h-2v-7c0-3.9-3.1-7-7-7z M12 18c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z",
            "ctaText": "Partecipa come Consulente Scientifico"
        },
        {
            "title": "Specialisti di Settore",
            "description": "Consulenti con profonda conoscenza normativa",
            "icon": "M22 10v12H2V10l7-5 4 3 6-5 3 3zM12 17v5h4v-5h-4z M4 12v2h2v-2H4z M4 16v2h2v-2H4z",
            "ctaText": "Diventa Specialista di Settore"
        },
        {
            "title": "Revisori Tecnici",
            "description": "Professionisti della certificazione per ISO, GMP e altri",
            "icon": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-2h2v2zm0-4H7v-2h2v2zm0-4H7V7h2v2zm8 8h-6v-2h6v2zm0-4h-6v-2h6v2zm0-4h-6V7h6v2z",
            "ctaText": "Collabora come Revisore"
        },
        {
            "title": "Consulenti ESG",
            "description": "Esperti in sostenibilità e specialisti in contabilità emissioni",
            "icon": "M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22L6.66 19.7C7.14 19.87 7.64 20 8 20C19 20 22 3 22 3C21 5 14 5.25 9 6.25C4 7.25 2 11.5 2 13.5C2 15.5 3.75 17.25 3.75 17.25C7.5 13.5 12.5 13.5 15.5 13.5C15.5 13.5 16 13.75 16 14.25C16 14.75 15.5 15 15.5 15C12.5 15 7.5 15 3.75 18.75C3.75 18.75 5.25 20.5 8 20.5C11.5 20.5 17 16 17 8Z",
            "ctaText": "Diventa Consulente ESG"
        }
    ]
    st.save()
    print("[SUCCESS] Fixed network cards schema.")

if __name__ == '__main__':
    fix_network_cards()
