import requests
import json

def find(args):
    search = '%20'.join(args)
    query = f'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&cselibv=a57bc5975bc720b0&cx=26533ab1e170a00d7&q={search}&safe=off&cse_tok=AJvRUv0bp2NHp-k8cmmQKflDb_wQ:1612183669486&sort=&exp=csqr,cc&oq={search}&gs_l=partner-generic.3...68531.87020.0.128587.5.5.0.0.0.0.281.596.2j2j1.5.0.csems%2Cnrl%3D13...0.18501j324128851j5...1.34.partner-generic..5.0.0.TYhf-zuS2uU&callback=google.search.cse.api19501'
    lines = requests.get(query).text.splitlines()
    lines = lines[2:-1]
    lines.insert(0, '{')
    lines.append('}')
    data = json.loads('\n'.join(lines))
    return data['results']
