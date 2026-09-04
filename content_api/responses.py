from flask import jsonify
from models_api.publication.publication_model import Publication
from models_api.article.article_model import Article
from models_api.images.image_model import Images
from models_api.text_analysis.text_analysis_model import TrendingEntityDTO
class ApiError(Exception):
    """ Custom exception that can work with Flask's errorhandler() """

    def __init__(self, code: str, status: int, detail: str | None = None):

        # Flask expects specific values for "code"
        #   ex: "not_found" "internal" "validation_failed"

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def list_publication_envelope(publications: list[Publication]):
         return jsonify([p.model_dump(mode="json") for p in publications])

def single_publication_envelope(publication: Publication):
        return jsonify(publication.model_dump(mode="json"))
 
def list_article_envelope(articles: list[Article]):
        return jsonify([a.model_dump(mode="json") for a in articles])

def single_article_envelope(article: Article):
        return jsonify(article.model_dump(mode="json")) 
   
def list_image_envelope(images: list[Images]):
        return jsonify([i.model_dump(mode="json") for i in images])

def single_image_envelope(image: Images):
        return jsonify(image.model_dump(mode="json")) 

def list_text_envelope(tags: list[TrendingEntityDTO]):
        return jsonify([t.model_dump(mode="json") for t in tags])

def single_text_envelope(tag: TrendingEntityDTO):
        return jsonify(tag.model_dump(mode="json")) 
     
def error_response(code: str, status: int, detail: str | None = None):
        return jsonify(error=code, detail=detail), status
    