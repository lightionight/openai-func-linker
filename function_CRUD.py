import pinecone
import datetime
import uuid
class EmbeddingMemory:
    def __init__(self):
        self.api_key = '90a607a0-13f8-4482-8fe1-e24ba6976197'
        self.env = 'us-central1-gcp'
        self.embedding_dimension = 1536
        self.index_name = 'funclib'
        pinecone.init(api_key = self.api_key, environment = self.env)
        self.connect(self.index_name)
    # connect database
    def connect(self, index_name):
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension = self.embedding_dimension,
                metric = 'cosine',
                metadata_config = {
                    'indexed' : ['name', 'keyword']
                }
            )
        self.index = pinecone.Index(index_name)
    
    def query(self, query_vector, namespace):
        index_name = self.index_name
        #self.remove_dup(query_vector, index_name, namespace)
        result = self.index.query(
            namespace = namespace, 
            vector = query_vector, 
            top_k = 10, 
            include_metadata=True
        )
        context = []
        try:
            for item in result['matches']:
                print(item['score'])
                #if item['score'] < 0.95 and item['score'] > 0.9 :   # 将上下文加入对话的判断标准
                if item['score'] > 0.8 :   # 将上下文加入对话的判断标准
                    context.append(item["metadata"])
                else:
                    pass
        except Exception as e:
            print(e)
        return context

    def insert(self, embedding_vector, context, namespace):
        self.connect(self.index_name)
        item = [{
            'id': str(uuid.uuid4()),
            'values': embedding_vector,
            'metadata': context
        }]
        self.index.upsert(item,namespace=namespace)
    

    def remove_dup(self, query_vector, index_name, namespace):
        self.connect(index_name)
        result = self.index.query(
            vector = query_vector, 
            top_k = 10, 
            namespace = namespace
        )
        for item in result['matches']:
            if item['score'] >= 0.97:
                self.index.delete(item['id'])