import json
import requests
import xml.etree.ElementTree as ET

plantcyc_api = 'http://pmn.plantcyc.org/apixml?'

def search(args):
    pwy_id = args['pwy'].upper()
    org_id = args['org'].upper()
    
    query_object = 'genes-of-pathway'
    query_id = org_id + ':' + pwy_id
    query_detail = 'none'
    
    plantcyc_url = plantcyc_api + 'fn=' + query_object + '&id=' + query_id + '&detail=' + query_detail
    
    r = requests.get(plantcyc_url)

    # Raise exception on bad HTTP status
    r.raise_for_status()
    
    result = {}
    result.setdefault('query', {})
    result['query'].setdefault('pathway', pwy_id)
    result['query'].setdefault('organism', org_id)
    result.setdefault('genes', [])
    try:
        root = ET.fromstring(r.text)
        for gene in root.findall('./Gene'):
            try:
                gene_id = gene.attrib['frameid']
                gene_org = gene.attrib['orgid']
                result['genes'].append({'gene_id' : gene_id, 'organism_id' : gene_org})
            except KeyError:
                continue
        print(json.dumps(result, indent=3))
    except TypeError:
        raise Exception('Unable to handle response '.format(r.text))
    
