from logger import FileLogger
from document_parser import parse_document, get_contents_for_files, validate_document_fields

# def get_field(key, look_up):
#     return look_up.get(key.lower())

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
