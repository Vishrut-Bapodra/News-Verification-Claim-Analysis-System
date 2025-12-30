from typing import Dict
from workflow import run_workflow
from utils import setup_logger

logger = setup_logger()

def verify_article(article_url: str) -> Dict:
    logger.info(f"Starting verification for URL: {article_url}")

    try:
        result = run_workflow(article_url)
        logger.info("Verification completed successfully")
        return result

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return {
            "error": "Verification failed",
            "details": str(e)
        }
    
if __name__ == "__main__":
    url = input("Enter article URL: ").strip()
    output = verify_article(url)
    print(output)