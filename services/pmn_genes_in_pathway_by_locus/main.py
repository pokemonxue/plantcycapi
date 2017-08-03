import json
import requests
import xml.etree.ElementTree as ET

# biocyc_api = 'http://websvc.biocyc.org/apixml?'
plantcyc_api = 'http://pmn.plantcyc.org/apixml?'


def get_genes_from_pathway(org_id, pwy_id):
    
    query_fn_pathway = 'genes-of-pathway'
    query_id_pathway = org_id + ':' + pwy_id
    query_detail = 'none'
    
    plantcyc_url = plantcyc_api + 'fn=' + query_fn_pathway + '&id=' + query_id_pathway + '&detail=' + query_detail
    
    r_plantcyc = requests.get(plantcyc_url)
    
    # Raise exception on bad HTTP status
    r_plantcyc.raise_for_status()
    
    genes = []
    
    try:
        root = ET.fromstring(r_plantcyc.text)
        for gene in root.findall('./Gene'):
            try:
                gene_id = gene.attrib['frameid']
                gene_org = gene.attrib['orgid']
                genes.append({'gene_id' : gene_id, 'organism_id' : gene_org})
            except KeyError:
                continue
        return genes
    except TypeError:
        raise Exception('Unable to handle response from plantcyc '.format(r.text))


def search(args):
    locus_id = args['locus'].upper()
    org_id = args['org'].upper()
    
    query_fn_locus = 'pathways-of-gene'
    query_id_locus = org_id + ':' + locus_id
    
    query_detail = 'none'
    
    # biocyc_url = biocyc_api + 'fn=' + query_fn_locus + '&id=' + query_id_locus + '&detail=' + query_detail
    biocyc_url = plantcyc_api + 'fn=' + query_fn_locus + '&id=' + query_id_locus + '&detail=' + query_detail
    
    r_biocyc = requests.get(biocyc_url)

    # Raise exception on bad HTTP status
    r_biocyc.raise_for_status()
    
    result = {}
    result.setdefault('query', {})
    result['query'].setdefault('locus', locus_id)
    result['query'].setdefault('organism_id', org_id)
    result.setdefault('pathways', [])
    try:
        root = ET.fromstring(r_biocyc.text)
        for pwy in root.findall('./Pathway'):
            try:
                pwy_id = pwy.attrib['frameid'].upper()
                pwy_org = pwy.attrib['orgid'].upper()
                pwy_genes = get_genes_from_pathway(pwy_org, pwy_id)
                result['pathways'].append({'pathway_id' : pwy_id, 'organism_id' : pwy_org, 'genes' : pwy_genes})
            except KeyError:
                continue
        print(json.dumps(result, indent=3))
    except TypeError:
        raise Exception('Unable to handle response from biocyc '.format(r.text))
    
