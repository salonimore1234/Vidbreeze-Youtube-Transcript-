from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class TextSummarizer:
    def __init__(self, endpoint, key):
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def summarize(self, text):
        try:
            poller = self.client.begin_analyze_actions(
                documents=[text],
                actions=[{"extract_summary_action": {}}],
            )
            result = poller.result()
            summary = ""

            for page in result:
                for action_result in page:
                    if action_result.is_error:
                        print(f"Error: {action_result.code} - {action_result.message}")
                    else:
                        # Assuming there is only one document in the result, we take the first one
                        for sentence in action_result.result.sentences:
                            summary += sentence.text + " "
            return summary.strip()  # Remove any trailing space
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return None
