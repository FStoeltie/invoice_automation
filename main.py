from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os
import pandas as pd
endpoint = "https://westeurope.api.cognitive.microsoft.com"
credential = AzureKeyCredential("")
document_analysis_client = DocumentAnalysisClient(endpoint, credential)

with open(f"{os.getcwd()}/documents/invoice128998568.pdf", "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", document=f
    )
result = poller.result()

def createSublists(elements, columns):
    n = len(columns)
    sublists = []
    print(f"range: {range(n)}")
    for i in range(0, len(elements), n):
        sublists.append([cell.content for cell in elements[i:i+n]])

    print(f"sublists: {sublists}")
    return sublists


def findFees(tables):
    for table in tables:
        columns = [cell.content for cell in table.cells[0:table.column_count]]
        print(f"columns: {columns}")
        values = createSublists(table.cells[table.column_count:-table.column_count], columns)
        totalDf = pd.DataFrame(values, columns=columns)

        print(totalDf)

findFees(result.tables[1:])

print("----------------------------------------")