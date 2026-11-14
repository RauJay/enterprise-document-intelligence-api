while(True):
    request_id = input("enter an access request ID:\n")

    if not request_id.strip():
        continue
    if request_id.lower() == "exit":
        break

    print(f"Request confirmed: {request_id}")