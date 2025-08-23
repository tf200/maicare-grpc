



from config.logging_config import get_logger
import generated.spelling_service_pb2 as pb2
from spelling_check.corrector import correct_spelling_llm


logger = get_logger(__name__)



class SpellingCheckService:
    def CorrectSpelling(self, request: pb2.CorrectSpellingRequest, context):
        try: 
            corrected_text = correct_spelling_llm(request.initial_text)
            response = pb2.CorrectSpellingResponse(
                corrected_text=corrected_text.corrected_text
            )
            return response
        except Exception as e:
            logger.error(f"Error in CorrectSpelling: {e}")
            raise e
        