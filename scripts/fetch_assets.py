#!/usr/bin/env python3
"""Cache brand favicon images as SVG wrappers; no remote images at runtime."""
import base64, concurrent.futures, hashlib, json, re, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'public/data/atlas.json').read_text())
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
OVERRIDES={
    'softbank':'https://upload.wikimedia.org/wikipedia/commons/a/a7/SoftBank_Group_logo.svg',
    'screen':'https://www.google.com/s2/favicons?domain=screen-spe.com&sz=128',
    'synopsys':'https://svgbrand.com/uploads/images/webp/202311/SVG_Brand_synopsys.webp',
}

def fetch(company):
    id,domain=company['id'],company['domain']
    path=ROOT/'public/assets/logos'/f'{id}.svg'
    url=OVERRIDES.get(id,f'https://www.google.com/s2/favicons?domain={domain}&sz=128')
    if path.exists():return {'id':id,'url':url,'cached':True}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':UA})
        with urllib.request.urlopen(request,timeout=25) as r:
            content=r.read();mime=r.headers.get_content_type()
        if not mime.startswith('image/') or len(content)<100:raise ValueError('Not an image')
        data=base64.b64encode(content).decode()
        path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><image width="128" height="128" href="data:{mime};base64,{data}"/></svg>\n')
        return {'id':id,'url':url,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
    except Exception as e:
        return {'id':id,'url':url,'error':str(e)}

def main():
    (ROOT/'public/assets/logos').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:results=list(executor.map(fetch,DATA['companies']))
    (ROOT/'public/assets/brand-sources.json').write_text(json.dumps({'note':'Brand imagery is used for identification. Marks belong to their respective owners. Google favicon cache supplies site icons.','logos':results},indent=2)+'\n')
    errors=[r for r in results if 'error' in r]
    for r in errors:print(json.dumps(r))
    print(f'Logos cached: {len(results)-len(errors)}/{len(results)}')
    # Request one variable font subset with Hebrew, Latin and punctuation.
    fontpath=ROOT/'public/assets/font.css'
    if not fontpath.exists():
        url='https://fonts.googleapis.com/css2?family=Heebo:wght@100..900&display=swap'
        css=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=25).read().decode()
        chunks=css.split('@font-face')
        declarations=[]
        for i,chunk in enumerate(chunks[1:]):
            match=re.search(r'url\((https:[^)]+)\)',chunk)
            if not match:continue
            u=match.group(1);b=urllib.request.urlopen(u,timeout=25).read()
            suffix='woff2' if 'woff2' in u else 'ttf'
            filename=f'hebrew-{i}.{suffix}'
            (ROOT/'public/assets'/filename).write_bytes(b)
            # Embedded base64 keeps the GitHub source tree text-only and portable.
            mime='font/woff2' if suffix=='woff2' else 'font/ttf'
            declaration='@font-face'+chunk[:chunk.index('}')+1]
            declaration=declaration.replace("font-family: 'Heebo'","font-family: AtlasHebrew").replace(u,'data:'+mime+';base64,'+base64.b64encode(b).decode())
            declarations.append(declaration)
            (ROOT/'public/assets'/filename).unlink()
        (ROOT/'public/assets/font.css').write_text('\n'.join(declarations)+'\n')
        print('Font declarations',len(declarations))

if __name__=='__main__':main()
