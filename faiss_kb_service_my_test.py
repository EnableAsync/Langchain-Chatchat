import os
import shutil

from configs import (
    KB_ROOT_PATH,
    SCORE_THRESHOLD,
    logger, log_verbose,
)
from server.knowledge_base.kb_service.base import KBService, SupportedVSType
from server.knowledge_base.kb_cache.faiss_cache import kb_faiss_pool, ThreadSafeFaiss
from server.knowledge_base.utils import KnowledgeFile
from langchain.embeddings.base import Embeddings
from typing import List, Dict, Optional
from langchain.docstore.document import Document
from server.utils import torch_gc


class FaissKBService(KBService):
    vs_path: str
    kb_path: str
    vector_name: str = "vector_store"

    def vs_type(self) -> str:
        return SupportedVSType.FAISS

    def get_vs_path(self):
        return os.path.join(self.get_kb_path(), self.vector_name)

    def get_kb_path(self):
        return os.path.join(KB_ROOT_PATH, self.kb_name)

    def load_vector_store(self) -> ThreadSafeFaiss:
        return kb_faiss_pool.load_vector_store(kb_name=self.kb_name,
                                               vector_name=self.vector_name,
                                               embed_model=self.embed_model)

    def save_vector_store(self):
        self.load_vector_store().save(self.vs_path)

    def get_doc_by_id(self, id: str) -> Optional[Document]:
        with self.load_vector_store().acquire() as vs:
            return vs.docstore._dict.get(id)

    def do_init(self):
        self.kb_path = self.get_kb_path()
        self.vs_path = self.get_vs_path()

    def do_create_kb(self):
        if not os.path.exists(self.vs_path):
            os.makedirs(self.vs_path)
        self.load_vector_store()

    def do_drop_kb(self):
        self.clear_vs()
        shutil.rmtree(self.kb_path)

    def do_search(self,
                  query: str,
                  top_k: int,
                  score_threshold: float = SCORE_THRESHOLD,
                  embeddings: Embeddings = None,
                  ) -> List[Document]:
        with self.load_vector_store().acquire() as vs:
            docs = vs.similarity_search_with_score(query, k=top_k, score_threshold=score_threshold)
        return docs

    def do_add_doc(self,
                   docs: List[Document],
                   **kwargs,
                   ) -> List[Dict]:
        with self.load_vector_store().acquire() as vs:
            ids = vs.add_documents(docs)
            if not kwargs.get("not_refresh_vs_cache"):
                vs.save_local(self.vs_path)
        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]
        torch_gc()
        return doc_infos

    def do_delete_doc(self,
                      kb_file: KnowledgeFile,
                      **kwargs):
        with self.load_vector_store().acquire() as vs:
            ids = [k for k, v in vs.docstore._dict.items() if v.metadata.get("source") == kb_file.filepath]
            if len(ids) > 0:
                vs.delete(ids)
            if not kwargs.get("not_refresh_vs_cache"):
                vs.save_local(self.vs_path)
        return ids

    def do_clear_vs(self):
        with kb_faiss_pool.atomic:
            kb_faiss_pool.pop((self.kb_name, self.vector_name))
        shutil.rmtree(self.vs_path)
        os.makedirs(self.vs_path)

    def exist_doc(self, file_name: str):
        if super().exist_doc(file_name):
            return "in_db"

        content_path = os.path.join(self.kb_path, "content")
        if os.path.isfile(os.path.join(content_path, file_name)):
            return "in_folder"
        else:
            return False


if __name__ == '__main__':
    from pprint import pprint
    # faissService = FaissKBService("fault")
    from server.knowledge_base.kb_service import faiss_kb_service
    # faissService = faiss_kb_service.FaissKBService("kb_200_and_500_strip")
    faissService = faiss_kb_service.FaissKBService("test_book_data")
    print(faissService.exist_doc("csv_data.csv"))
    print(faissService.exist_doc("机床维修案例_200.csv"))

    TOP_K = 5

    import pandas as pd
    # csv_data = pd.read_csv("/home/kdzlys/data-disk/sjj/Langchain-Chatchat/knowledge_base/fault/content/csv_data.csv")
    csv_data = pd.read_csv("/home/kdzlys/data-disk/sjj/Langchain-Chatchat/knowledge_base/test_book_data/content/200-机床维修例子_output.csv")

    # 用于计算平均第几个是正确答案
    total_index = 0

    # 用于计算查全率（召回率）
    total_search = 0

    # 用于计算平均距离
    total_distance = 0.0

    row_id = 0

    for index, row in csv_data.iterrows():
        # content = row['content'].strip()
        content = row['questions'].strip()
        pprint(content)
        # answer = row['分析过程']
        # answer = row['answers']
        # row_id = row['id']
        # print(content)
        docs = faissService.search_docs(content, TOP_K, 1.0)
        exist = False
        # print(docs)
        # break
        for index, doc in enumerate(docs):
            # print(doc)
            l2_distance = doc[1]
            doc = doc[0]
            if not "row" in doc.metadata:
                break
            if doc.metadata['row'] == row_id:
                total_index += (index + 1)
                total_search += 1
                total_distance += l2_distance
                exist = True
                break
        if not exist:
            total_index += TOP_K
            total_distance += 1
            print(content)
            pprint(docs)
        row_id += 1
        # if row_id == 5:
        #     break
    
    print(f"召回率：{total_search / len(csv_data)}")
    print(f"平均 top：{total_index / len(csv_data)}")
    print(f"平均距离：{total_distance / len(csv_data)}")

# TOP_K = 10
# 召回率：0.9694656488549618
# 平均 top：1.133587786259542

# TOP_K = 5
# 召回率：0.9694656488549618
# 平均 top：1.2881679389312977
# 平均距离：0.5779193880903812

# TOP_K = 4
# 召回率：0.9656488549618321
# 平均 top：1.1145038167938932

# TOP_K = 3
# 召回率：0.9580152671755725
# 平均 top：1.083969465648855

# TOP_K = 2
# 召回率：0.9446564885496184
# 平均 top：1.0438931297709924

# TOP_K = 1
# 召回率：0.8454198473282443
# 平均 top：0.8454198473282443


# 200+500 中的 200 条
# 召回率：0.995
# 平均 top：1.34
# 平均距离：0.1928387996030506

# 200+500 中的 500 条
# 召回率：1.0
# 平均 top：1.015267175572519
# 平均距离：0.03619958298860246

# 200 + 500 + 所有书中的 200 条
# 召回率：0.9948979591836735
# 平均 top：1.316326530612245
# 平均距离：0.19947207336580114