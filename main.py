from logger import FileLogger
from pathlib import Path

REQUIRED_FIELDS = [
    "requester",
    "department",
    "resource",
    "access",
    "duration",
    "business justification"]

def parse_document(file_name, logger):
    keyVal = {}
    with open(file_name, encoding="utf-8") as file:
        count = 0
        for line in file:
            count +=1
            key, separator,value = line.partition(":")
            if separator and key.strip():
                keyVal[key.strip().lower()] =  value.strip() or ""
            elif line.strip():
                logger.warning(document_filename=file_name, line_number=count)           
                
    return keyVal
        

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


logger = FileLogger("warnings.log")

for file_path in Path("documents").glob("*.txt"):
    document = parse_document(str(file_path), logger)
    print(f"{file_path.name}, {document}\n")
    print(f"{validate_document_fields(document)}\n")


# print(get_field("Requester", access_request))
# print(get_field("Unknown", access_request))
# print(get_field("Request Time", access_request))
# print(get_field("Requester", access_request_1))
