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
    # Set used to track duplicates
    # In this case it could be avoided by using key not in keyVal
    # in the condition below 
    field_tracker = set()
    with open(file_name, encoding="utf-8") as file:
        count = 0
        for line in file:
            count +=1
            # partition divides the string also retains the 
            # divider symbol which aids in condition below unlike split
            # where it's not retained
            key, separator,value = line.partition(":")
            key = key.strip().lower()
            if separator and key and key not in field_tracker:
                keyVal[key] =  value.strip() or ""
                field_tracker.add(key)
            elif separator and key and key in field_tracker:
                logger.warning(file_name, count, duplicate=True)
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
documents = []
for file_path in Path("documents").glob("*.txt"):    
    document = parse_document(str(file_path), logger)
    print(f"{file_path.name}, {document}\n")
    print(f"{validate_document_fields(document)}\n")
    documents.append(document)

# print(get_field("Requester", access_request))
# print(get_field("Unknown", access_request))
# print(get_field("Request Time", access_request))
# print(get_field("Requester", access_request_1))
