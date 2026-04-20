import psycopg2
import json

def extract_for_translation():
    db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    data = {
        "page_content": [],
        "steps": []
    }
    
    # Extract Page Content
    cur.execute("SELECT id, hero_title_en, meta_title_en, meta_description_en FROM admin_portal_howweoperatepagecontent")
    for row in cur.fetchall():
        data["page_content"].append({
            "id": row[0],
            "hero_title": row[1].get('content') if row[1] else "",
            "meta_title": row[2].get('content') if row[2] else "",
            "meta_description": row[3].get('content') if row[3] else ""
        })
        
    # Extract Steps
    fields = ['title_en', 'subtitle_en', 'description_en', 'bullet1_en', 'bullet2_en', 'bullet3_en', 'bullet4_en', 'bullet5_en', 'bullet6_en', 'bullet7_en', 'bullet8_en', 'bullet9_en', 'description1_en', 'description2_en', 'description3_en', 'description4_en', 'wordbreak_en', 'button_text_en', 'button_text2_en', 'button_text3_en']
    query = f"SELECT id, {', '.join(fields)} FROM admin_portal_processstep ORDER BY id"
    cur.execute(query)
    
    for row in cur.fetchall():
        step = {"id": row[0]}
        for i, field in enumerate(fields):
            clean_name = field.replace('_en', '')
            val = row[i+1]
            step[clean_name] = val.get('content') if (val and isinstance(val, dict)) else ""
        data["steps"].append(step)
        
    with open('how_we_operate_en.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    conn.close()
    print("Extracted English content to how_we_operate_en.json")

if __name__ == "__main__":
    extract_for_translation()
