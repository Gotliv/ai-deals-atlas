#!/usr/bin/env python3
"""Compile the reviewed source records into the portable public dataset."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUESTED = {'amazon','google','meta','microsoft','apple','applied-materials','nvidia','tsmc','tesla','spacex','openai','anthropic','intel','oracle'}
CORE = REQUESTED | {'amd','broadcom','samsung','sk-hynix','micron','asml','coreweave','nebius','nscale','oracle','softbank','mistral','xai','stargate','terawulf','midjourney','fluidstack'}
# id: English brand, Hebrew alias, sector, public website, Hebrew description.
COMPANIES = {
 'amazon': ('Amazon','אמזון','cloud','amazon.com','קבוצת מסחר וטכנולוגיה. פעילות הענן והמחשוב במפה כוללת את AWS.'),
 'google': ('Google','גוגל אלפבית','cloud','google.com','חלק מקבוצת Alphabet. מודלי Gemini, תשתיות Google Cloud ומאיצי TPU.'),
 'meta': ('Meta','מטא פייסבוק','cloud','meta.com','מפתחת Llama, מוצרי רשתות חברתיות ותשתיות AI בקנה מידה גדול.'),
 'microsoft': ('Microsoft','מיקרוסופט','cloud','microsoft.com','ספקית Azure, מוצרי Copilot ותוכנה ארגונית. משקיעה ושותפה בחברות AI.'),
 'apple': ('Apple','אפל','cloud','apple.com','מפתחת מכשירים, מערכות הפעלה ו-Apple Intelligence, כולל תשתית Private Cloud Compute.'),
 'applied-materials': ('Applied Materials','אפלייד מטיריאלס','chips','appliedmaterials.com','מפתחת ציוד ותהליכי ייצור לשבבים, זיכרונות ואריזה מתקדמת.'),
 'nvidia': ('NVIDIA','אנבידיה נבידיה','chips','nvidia.com','מפתחת מאיצים, מעבדים, רשתות ותוכנת מחשוב מואץ. גם משקיעה בלקוחות ובשותפות.'),
 'tsmc': ('TSMC','טי אס אם סי','chips','tsmc.com','יצרנית שבבים עבור לקוחות חיצוניים, עם טכנולוגיות ייצור ואריזה מתקדמת.'),
 'tesla': ('Tesla','טסלה','physical','tesla.com','מפתחת כלי רכב, מערכות אגירת אנרגיה, נהיגה אוטונומית ורובוטיקה.'),
 'spacex': ('SpaceX','ספייס איקס','physical','spacex.com','קבוצת חלל ותקשורת הכוללת גם פעילות AI לאחר רכישת xAI. חלק מההסכמים נוגעים למחשוב קרקעי.'),
 'openai': ('OpenAI','אופן איי איי','labs','openai.com','מפתחת ChatGPT, מודלים וסוכני AI, ורוכשת קיבולת מחשוב ממספר ספקיות.'),
 'anthropic': ('Anthropic','אנתרופיק אנתרופי','labs','anthropic.com','מפתחת Claude, כלי פיתוח וסוכני AI. קשריה כוללים ענן, השקעות ותשתיות.'),
 'intel': ('Intel','אינטל','chips','intel.com','מפתחת מעבדים, טכנולוגיות ייצור שבבים ושירותי ייצור ללקוחות.'),
 'amd': ('AMD','איי אם די','chips','amd.com','מפתחת מעבדי EPYC ומאיצי Instinct לתשתיות מחשוב ו-AI.'),
 'broadcom': ('Broadcom','ברודקום','chips','broadcom.com','מפתחת מאיצים מותאמים, שבבי רשת ותשתיות קישוריות. משתתפת גם במבני מימון לתשתיות AI.'),
 'samsung': ('Samsung','סמסונג','chips','samsung.com','מייצרת זיכרונות ושבבים, מספקת שירותי ייצור ומפתחת מכשירי קצה. הרשומות מתייחסות לישות המפורטת במקור.'),
 'sk-hynix': ('SK hynix','אס קיי הייניקס','chips','skhynix.com','יצרנית זיכרונות, כולל HBM למאיצי AI.'),
 'micron': ('Micron','מיקרון','chips','micron.com','מפתחת ומייצרת זיכרונות ואחסון, כולל HBM לתשתיות AI.'),
 'asml': ('ASML','איי אס אם אל','chips','asml.com','מפתחת מערכות ליתוגרפיה לייצור שבבים. גם משקיעה ושותפה ב-Mistral.'),
 'coreweave': ('CoreWeave','קורוויב','infrastructure','coreweave.com','ספקית ענן ותשתיות מחשוב מואץ ללקוחות AI.'),
 'nebius': ('Nebius','נביוס','infrastructure','nebius.com','ספקית תשתיות ענן ומחשוב ל-AI ומפעילת מרכזי נתונים.'),
 'nscale': ('Nscale','אנסקייל','infrastructure','nscale.com','מפתחת תשתיות מרכזי נתונים ושירותי מחשוב מואץ.'),
 'oracle': ('Oracle','אורקל','cloud','oracle.com','ספקית Oracle Cloud Infrastructure, בסיסי נתונים ותוכנה ארגונית.'),
 'softbank': ('SoftBank','סופטבנק','capital','group.softbank','קבוצת השקעות וטכנולוגיה, משקיעה ב-OpenAI ושותפה במיזם Stargate.'),
 'mistral': ('Mistral AI','מיסטרל','labs','mistral.ai','מפתחת מודלים, Le Chat ותשתיות AI, בדגש על פריסה וגישה אירופית.'),
 'xai': ('xAI','אקס איי','labs','x.ai','מפתחת Grok ומערכי המחשוב Colossus. נרכשה בידי SpaceX בפברואר 2026.'),
 'stargate': ('Stargate','סטארגייט','infrastructure','openai.com','מיזם תשתיות AI נפרד מ-OpenAI. זהות משקיע מייסד אינה מעידה שכל הון היעד כבר הוזרם.'),
 'adobe': ('Adobe','אדובי','enterprise','adobe.com','תוכנה ליצירה, מסמכים, שיווק ומוצרי AI.'),
 'advantest': ('Advantest','אדוונטסט','chips','advantest.com','מפתחת מערכות בדיקה ומדידה לשבבים.'),
 'apollo': ('Apollo','אפולו','capital','apollo.com','מנהלת השקעות ונכסים המשתתפת במימון תשתיות AI.'),
 'asmpt': ('ASMPT','אס אם פי טי','chips','asmpt.com','ספקית ציוד לייצור, הרכבה ואריזה של רכיבים אלקטרוניים.'),
 'besi': ('Besi','בסי','chips','besi.com','ספקית ציוד להרכבה ולאריזה מתקדמת של שבבים.'),
 'blackrock': ('BlackRock','בלאקרוק','capital','blackrock.com','מנהלת נכסים המשתתפת ביוזמות מימון תשתיות.'),
 'blackstone': ('Blackstone','בלקסטון','capital','blackstone.com','מנהלת השקעות בתחומי תשתיות, אשראי ונכסים פרטיים.'),
 'blue-owl': ('Blue Owl','בלו אול','capital','blueowl.com','מנהלת השקעות. הקשרים במפה עשויים להיות דרך קרנות וחברות ייעודיות.'),
 'brookfield': ('Brookfield','ברוקפילד','capital','brookfield.com','מנהלת השקעות בתשתיות ובנכסים ריאליים.'),
 'celestica': ('Celestica','סלסטיקה','chips','celestica.com','מתכננת ומייצרת מערכות מחשוב וקישוריות ללקוחות טכנולוגיה.'),
 'citi': ('Citi','סיטי','capital','citigroup.com','קבוצה בנקאית, עם פעילות אשראי ומימון תשתיות.'),
 'cohere': ('Cohere','קוהיר','labs','cohere.com','מפתחת מודלים ופתרונות AI לארגונים.'),
 'coherent': ('Coherent','קוהירנט','chips','coherent.com','ספקית טכנולוגיות אופטיקה ופוטוניקה לקישוריות ולייצור.'),
 'databricks': ('Databricks','דאטהבריקס','enterprise','databricks.com','פלטפורמת נתונים, אנליטיקה ופיתוח יישומי AI.'),
 'dell': ('Dell','דל','chips','dell.com','ספקית שרתים, מערכות אחסון ותשתיות למחשוב מואץ.'),
 'essilorluxottica': ('EssilorLuxottica','אסילור לוקסוטיקה','enterprise','essilorluxottica.com','קבוצת משקפיים ואופטיקה, שותפת Meta במשקפיים חכמים.'),
 'goldman-sachs': ('Goldman Sachs','גולדמן זאקס','capital','goldmansachs.com','קבוצת בנקאות והשקעות המשתתפת במימון תשתיות.'),
 'helix': ('Helix','הליקס','infrastructure','helixdi.com','פלטפורמת תשתיות דיגיטליות ומרכזי נתונים. זהות המשקיעים וההיקף מפורטים בכרטיסי העסקאות.'),
 'hugging-face': ('Hugging Face','האגינג פייס','enterprise','huggingface.co','פלטפורמת מודלים, נתונים וכלים לקהילת למידת המכונה.'),
 'ibm': ('IBM','איי בי אם','enterprise','ibm.com','ספקית תוכנה, שירותים ופתרונות AI ארגוניים, כולל watsonx.'),
 'inflection': ('Inflection','אינפלקשן','labs','inflection.ai','מפתחת מודלים. העסקה עם Microsoft כללה כוח אדם ורישוי, ולא רכישה מלאה של החברה.'),
 'iren': ('IREN','איירן','infrastructure','iren.com','מפתחת מרכזי נתונים ושירותי מחשוב מואץ.'),
 'jane-street': ('Jane Street','ג׳יין סטריט','capital','janestreet.com','חברת מסחר כמותי המשתתפת גם ברכישת מחשוב ובהשקעות בתשתיות.'),
 'kioxia': ('KIOXIA','קיוקסיה','chips','kioxia.com','מפתחת ומייצרת זיכרונות הבזק ומוצרי אחסון.'),
 'kkr': ('KKR','קיי קיי אר','capital','kkr.com','מנהלת השקעות גלובלית, כולל אשראי ותשתיות.'),
 'lumentum': ('Lumentum','לומנטום','chips','lumentum.com','ספקית רכיבי אופטיקה ופוטוניקה לתקשורת ולמרכזי נתונים.'),
 'manus': ('Manus','מאנוס','labs','manus.im','מפתחת סוכני AI. העסקה ההיסטורית עם Meta מסומנת כקשר שהסתיים.'),
 'marvell': ('Marvell','מארוול','chips','marvell.com','מפתחת שבבים מותאמים, קישוריות אופטית ורשתות למרכזי נתונים.'),
 'mgx': ('MGX','אם ג׳י אקס','capital','mgx.ae','חברת השקעות המתמקדת ב-AI, תשתיות וטכנולוגיות נלוות.'),
 'palantir': ('Palantir','פלנטיר','enterprise','palantir.com','מפתחת פלטפורמות נתונים, תוכנה וסוכני AI לארגונים.'),
 'perplexity': ('Perplexity','פרפלקסיטי','labs','perplexity.ai','מפתחת מנוע תשובות, חיפוש וכלי AI לצרכנים ולארגונים.'),
 'reliance': ('Reliance','רילאיינס','infrastructure','ril.com','קבוצת תעשייה וטכנולוגיה הודית. הרשומות במפה כוללות שותפויות AI ותשתיות.'),
 'salesforce': ('Salesforce','סיילספורס','enterprise','salesforce.com','ספקית מערכות קשרי לקוחות, נתונים וסוכני AI.'),
 'sap': ('SAP','סאפ','enterprise','sap.com','ספקית תוכנה ארגונית, מערכות ERP ו-Business AI.'),
 'sb-energy': ('SB Energy','אס בי אנרג׳י','infrastructure','sbenergy.com','מפתחת תשתיות אנרגיה ומרכזי נתונים. ערבויות לקיבולת אינן השקעות הון.'),
 'scale-ai': ('Scale AI','סקייל איי איי','enterprise','scale.com','מספקת נתונים, הערכה ותשתיות לפיתוח מודלי AI.'),
 'screen': ('SCREEN','סקרין','chips','screen.co.jp','ספקית ציוד לתהליכי ייצור וניקוי פרוסות סיליקון.'),
 'servicenow': ('ServiceNow','סרוויסנאו','enterprise','servicenow.com','פלטפורמת תהליכי עבודה ארגוניים וסוכני AI.'),
 'snowflake': ('Snowflake','סנופלייק','enterprise','snowflake.com','פלטפורמת נתונים ויישומי AI בענן.'),
 'synopsys': ('Synopsys','סינופסיס','chips','synopsys.com','מפתחת כלי תכנון שבבים, קניין רוחני וסימולציות הנדסיות.'),
 'thinking-machines': ('Thinking Machines','תינקינג משינס','labs','thinkingmachines.ai','מעבדת AI המפתחת מודלים ותשתיות מחקר.'),
 'terawulf': ('TeraWulf','טרהוולף','infrastructure','terawulf.com','מפתחת ומפעילה מרכזי נתונים. קשרי החכירה והמימון במפה כוללים חברות ייעודיות המפורטות במקורות.'),
 'midjourney': ('Midjourney','מידג׳רני','labs','midjourney.com','מפתחת מודלים ליצירת תמונות ווידאו. עסקאות המבוססות על דיווחים תקשורתיים מסומנות במפורש.'),
 'fluidstack': ('Fluidstack','פלואידסטאק','infrastructure','fluidstack.io','מפתחת ומפעילה תשתיות ענן ומחשוב מואץ למעבדות AI.'),
}

def main():
    size_path=ROOT/'research/company_sizes.json'
    sizes=json.loads(size_path.read_text()) if size_path.exists() else {'companies':{}}
    records=[]
    for path in sorted((ROOT/'research').glob('*.json')):
        content=json.loads(path.read_text())
        if isinstance(content,list) and content and all('source' in x and 'target' in x for x in content):
            records.extend(content)
    # Merge the initial SpaceX launch description into the current SEC-backed aggregate.
    original=next(d for d in records if d['id']=='hws-anthropic-spacex-compute')
    current=next(d for d in records if d['id']=='anthropic-spacex-compute-current-2026')
    current['sources'] += [s for s in original['sources'] if s['url'] not in {z['url'] for z in current['sources']}]
    records=[d for d in records if d['id']!='hws-anthropic-spacex-compute']
    for d in records:
        if d['id']=='nv-openai-loi-2025':
            d.update(historical=True,default_visible=False,superseded_by='nv-openai-investment-2026')
        if d['id']=='meta-blueowl-hyperion-2025':
            d['indirect']=True
        if d['id']=='microsoft-coreweave-customer-2026':
            d['date_basis_he']='מועד הדיווח המאמת את הקשר, ולא תאריך תחילת החוזה.'
        for s in d['sources']:
            assert s['url'].startswith('https://'), (d['id'],s['url'])
    ids=sorted({d[k] for d in records for k in ('source','target')})
    unknown=set(ids)-set(COMPANIES)
    assert not unknown, f'Missing company metadata: {unknown}'
    companies=[]
    for id in ids:
        n,he,sector,domain,desc=COMPANIES[id]
        companies.append(dict(id=id,name=n,name_he=he,sector=sector,domain=domain,description_he=desc,logo=f'assets/logos/{id}.svg',core=id in CORE,requested=id in REQUESTED,node_type='project' if id=='stargate' else 'company',size=sizes['companies'].get(id,{'usd_billion':None,'kind':'unknown'})))
    companies.sort(key=lambda c:(not c['requested'],c['name'].lower()))
    records.sort(key=lambda d:(d['announced_at'],d['id']),reverse=True)
    data={'meta':{'title':'AI ATLAS','as_of':'2026-11-10','verified_at':'2026-11-06','language':'he','timezone':'Asia/Jerusalem','repository_url':'https://github.com/Gotliv/ai-deals-atlas','update_mode':'manually reviewed research snapshot; selected updates on 2026-11-10','coverage_he':'קשרים פומביים שנמצאו ונבדקו; אין התחייבות למיצוי כלל ההסכמים. היעדר קשר במפה אינו הוכחה להיעדר קשר במציאות.','amounts_he':'אין לסכום השקעות, ערבויות, התחייבויות, אופציות והרחבות חופפות.','schema_version':'1.0'},'companies':companies,'deals':records}
    out=ROOT/'public/data/atlas.json'
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'deals':len(records),'companies':len(companies),'sources':len({s['url'] for d in records for s in d['sources']}),'output':str(out)}))

if __name__=='__main__':main()
