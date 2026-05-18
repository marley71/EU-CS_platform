from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import TopBar
from django.db import connection
import requests
import json
from projects.models import Topic
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed dati principali'
    SPARQL_ENDPOINT = 'https://showvoc.op.europa.eu/semanticturkey/it.uniroma2.art.semanticturkey/st-core-services/SPARQL/evaluateQuery'
    BACKUP_URL = '/euroscivoc-backup.json'

    SPARQL_QUERY = """
            PREFIX : <http://data.europa.eu/8mn/euroscivoc/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT DISTINCT ?concept ?broader ?label_it ?label_en WHERE {
              { ?concept a skos:Concept . FILTER NOT EXISTS { ?concept skos:broader ?any } }
              UNION
              { ?concept skos:broader ?broader . FILTER NOT EXISTS { ?broader skos:broader ?any } }
              UNION
              { ?concept skos:broader ?broader . ?broader skos:broader ?broader2 . FILTER NOT EXISTS { ?broader2 skos:broader ?any } }
              OPTIONAL { ?concept skos:prefLabel ?label_it . FILTER (lang(?label_it) = "it") }
              OPTIONAL { ?concept skos:prefLabel ?label_en . FILTER (lang(?label_en) = "en") }
            }
            """

    def handle(self, *args, **options):
        try:
            data = self.query_sparql()
            #print(json.dumps(data))
            self.save(data)
            self.writeJsonTree()
        except Exception as e:
            print(e)

    def query_sparql(self):
        response = requests.post(self.SPARQL_ENDPOINT,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={
                                     'ctx_project': 'OP_European_Science_Vocabulary_(EuroSciVoc)',
                                     'query': self.SPARQL_QUERY
                                 }
                                 )

        # Verifica se la risposta ha avuto successo
        if not response.ok:
            print('Status:', response.status_code)
            print('Reason:', response.reason)
            print('URL:', response.url)
            print('Headers:')
            for k, v in response.headers.items():
                print(f'  {k}: {v}')
            print('Cookies:', response.cookies.get_dict())
            print('History:', [h.status_code for h in response.history])
            print('Encoding:', response.encoding)
            print('Content (bytes):', response.content)        # attenzione: carica tutto in memoria
            print('Text (str):', response.text)       
            raise Exception(f"SPARQL error: {response.status_code}")

        # Restituisce il contenuto JSON della risposta
        return response.json()

    def save(self, data):
        self.stdout.write("Eseguo il comando save ...")
        try:
            for item in data['result']['sparql']['results']['bindings']:

                if 'broader' in item:
                    broader = item['broader']['value']
                    topic = Topic.objects.filter(concept=item['concept']['value'],broader=broader).first()
                else:
                    topic = Topic.objects.filter(concept=item['concept']['value']).first()

                if topic:
                    topic.label_it = item['label_it']['value']
                    topic.label_en = item['label_en']['value']
                    topic.save()
                else:
                    concept = item['concept']['value']
                    label_it = item['label_it']['value']
                    label_en = item['label_en']['value']
                    broader = ""
                    if 'broader' in item:
                        broader = item['broader']['value']
                    print('Creo record ' + concept + ' it ' + label_it + ' en ' + label_en + ' broader ' + str(broader) )

                    Topic.objects.create(
                        #topic = "pippo " + str(i),  #concept,
                        topic_it = label_it,
                        topic_en = label_en,
                        broader = broader,
                        concept = concept,
                    )
        except Exception as e:
            print(e)

    def build_tree(self,nodes, parent=''):
        tree = []
        for node in nodes:
            if node['broader'] == parent:
                children = self.build_tree(nodes, node['concept'])
                subtree = {'id': node['id'], 'concept': node['concept'], 'nome': node['topic_it'], 'title': node['topic_it']}
                if children:
                    subtree['children'] = children
                tree.append(subtree)
        return tree

    def writeJsonTree(self):
        records = list(Topic.objects.all().values('id','concept', 'topic_it', 'broader'))
        tree = self.build_tree(records,'')
        print(json.dumps(tree))
        nomefile = str(settings.BASE_DIR) + '/../resources/tassonomie.json'
        with open(nomefile, 'w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=2)