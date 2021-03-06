from Bio import Entrez
from sqlalchemy import create_engine, desc
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from twisted.internet.task import LoopingCall
from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from subprocess import Popen
from sqlalchemy.ext.automap import automap_base
import time


class GenomeBrowser(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.init()

    def init(self):
        engine = create_engine("mysql+pymysql://root:mysqlroot@localhost/hgcentral")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        self.db = Session()
        self.Genome = Base.classes.defaultDb
        Entrez.email = 'nicholas.roberts.au@gmail.com'
        pass


    @inlineCallbacks
    def onJoin(self, details):
        print "Session attached"

        def upload_ref_genome(file_payload):
            size = file_payload['size']
            name = file_payload['name']
            binary_payload = file_payload['file_string'].decode('base64')
            save_path = reduce(os.path.join, [upload_path, str(last_modified) + "_" + name])
            with open(save_path, "wb") as f:
                f.write(binary_payload)

        def upload_bed(file_payload):
            pass

        def ping(id):
            return 'pinging' + str(id)

        def fetch_taxon_id(taxonomy_name):
            handle = Entrez.esearch(db="taxonomy", term=taxonomy_name)
            record = Entrez.read(handle)
            if len(record['IdList']) != 0:
                return record['IdList'][0]
            else:
                return -1

        def fetch_genomes():
            genomes = map(lambda x: {'name': x.name, 'abbrev': x.genome}, self.db.query(self.Genome).all())
            return genomes
        
        def process_genome(form_data):
            print form_data
            out_string = '"description";"organism";"defaultPos";"genome";"scientificName";"sourceName";"taxId"\n"{}";'.format(form_data['description'])
            out_string += '"{}";"{}";"{}";"{}";"{}";{}'.format(form_data['organism'], form_data['defaultPos'], form_data['genome'], form_data['scientificName'], form_data['sourceName'], str(form_data['taxId']))
            with open('naming.csv', 'w') as f:
                f.write(out_string)
                
            p = Popen('./genome_dep.py')
        
        def process_annotation(form_data):
            ra_string = 'track {}\ntype bed {}\nshortLabel {}\nlongLabel {}'.format(form_data['name'], form_data['b_version'], form_data['short'], form_data['long'])
            ra_filename = '{}{}.ra'.format(time.time(), form_data['name'])
            with open(ra_filename, 'w') as f:
                f.write(ra_string)
                
            p = Popen('annotation_dep.py {} {} {} {}'.format(form_data['genome'], form_data['name'], form_data['bed_filename'], ra_filename))

        self.register(fetch_genomes, 'com.gb.fetch_genomes')
        self.register(fetch_taxon_id, 'com.gb.taxon_search')
        self.register(ping, 'com.gb.ping')
        self.register(process_genome, 'com.gb.submit_genome')
	while True:
		yield sleep(1)
