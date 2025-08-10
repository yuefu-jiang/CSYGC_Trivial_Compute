import csv
import io
import math

def csv_to_json(file_obj):
    """
    Converts a question file in CSV format to a dict used in format of questions.json file
    Assumes the first row contains headers.
    """
    # Ensure we're reading text, not bytes
    if isinstance(file_obj, bytes):
        file_obj = io.StringIO(file_obj.decode('utf-8'))
    elif hasattr(file_obj, 'read'):
        file_obj = io.StringIO(file_obj.read().decode('utf-8'))
    #count no. of lines
    count = sum(1 for _ in file_obj)
    #set the number of padding zeros in the question id
    pad = int(math.ceil(math.log10(count)))

    # Reset pointer to beginning
    file_obj.seek(0)
    
    reader = csv.DictReader(file_obj)

    skip = 'category'
    temp=dict()
    for row in reader:
        if row[skip] not in temp:
            newid = f"Q{1:{"0"+str(pad)}}"
            temp.update({row[skip]:{}})
            temp[row[skip]].update({newid:{}})
            temp[row[skip]][newid].update({k: v for k, v in row.items() if k !=skip})
            temp[row[skip]][newid]["used"]='false'
        else:
            #newid=f"Q{len(temp[row[skip]])+1:{str(pad)}}"
            newid = f"Q{len(temp[row[skip]])+1:{"0" + str(pad)}}"
            temp[row[skip]].update({newid:{}})
            temp[row[skip]][newid].update({k: v for k, v in row.items() if k !=skip})
            temp[row[skip]][newid]["used"]='false'
    return temp
