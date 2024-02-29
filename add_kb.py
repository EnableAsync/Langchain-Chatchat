kb_name = "kb_200_and_500_strip"
from server.knowledge_base.utils import KnowledgeFile, get_kb_path, get_vs_path


if __name__ == '__main__':
    from pprint import pprint
    from server.knowledge_base.kb_service import faiss_kb_service
    faissService = faiss_kb_service.FaissKBService(kb_name)
    faissService.add_doc(KnowledgeFile("csv_data.csv", kb_name))
    faissService.add_doc(KnowledgeFile("机床维修案例_200.csv", kb_name))
    print(faissService.exist_doc("csv_data.csv"))
    print(faissService.exist_doc("机床维修案例_200.csv"))