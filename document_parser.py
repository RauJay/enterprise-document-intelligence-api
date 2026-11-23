from errors import DocumentReadError
from pathlib import Path

REQUIRED_FIELDS = [
    "requester",
    "department",
    "resource",
    "access",
    "duration",
    "business justification"]

def read_document_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        return content
    except (OSError, UnicodeError) as exc:
        raise DocumentReadError(f"Could not read document '{file_path}': {exc}")  \
        from exc

def get_contents_for_files(dir_path):
    contents_dic = {}
    for file_path in Path(dir_path).glob("*.txt"):
        try:
            content = read_document_file(file_path)
            contents_dic[file_path.name] = content
        except DocumentReadError as ex:
            print(f"{ex} was raised while processing {file_path.name}")
            continue
    return contents_dic

def parse_document(content, file_name, logger):
    keyVal = {}
    # Set used to track duplicates
    # In this case it could be avoided by using key not in keyVal
    # in the condition below
    field_tracker = set()
    count = 0
    for line in content:
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