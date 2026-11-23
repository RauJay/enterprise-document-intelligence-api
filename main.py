from logger import FileLogger
from document_parser import parse_document, get_contents_for_files

REQUIRED_FIELDS = [
    "requester",
    "department",
    "resource",
    "access",
    "duration",
    "business justification"]

def get_field(key, look_up):
    return look_up.get(key.lower())

def validate_document_fields(document):
    missing_fields = [
       field for field in REQUIRED_FIELDS
       if field not in document
    ]

    if missing_fields:
        return f"Fields {", ".join(missing_fields)} are missing"
    missing_details = [
        field for field in REQUIRED_FIELDS
        if not document[field].strip()
    ]

    if missing_details:
        return f"Field details for {", ".join(missing_details)} are missing"

    return "Document is complete"


def main():
    logger = FileLogger("warnings.log")
    documents = []
    contents_dict = get_contents_for_files("documents")
    for content in contents_dict:
        document = parse_document(contents_dict[content].split("\n"), content, logger)
        print(f"{content}, {document}\n")
        print(f"{validate_document_fields(document)}\n")
        documents.append(document)

if __name__ == '__main__':
    main()  

# print(get_field("Requester", access_request))
# print(get_field("Unknown", access_request))
# print(get_field("Request Time", access_request))
# print(get_field("Requester", access_request_1))
